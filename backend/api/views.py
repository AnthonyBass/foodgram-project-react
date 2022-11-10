from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (
    AmountIngredientRecipe,
    Cart,
    Favorites,
    Ingredient,
    Recipe,
    Tag,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response
from users.models import Follow

from .filters import IngredientSearchFilter, RecipeFilter
from .paginator import CustomPaginationPageSize
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CartSerializer,
    FavoritesSerializer,
    FollowCreateSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPaginationPageSize
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        data = {"user": request.user.id, "recipe": pk}
        serializer = CartSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(Cart, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_dict = {}
        font = "Roboto-Regular"
        ingredients = AmountIngredientRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values_list(
            "ingredient__name",
            "ingredient__measurement_unit",
            "amount"
        )
        for item in ingredients:
            name, measurement_unit, amount = item
            if name not in shopping_dict:
                shopping_dict[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                shopping_dict[name]["amount"] += amount

        pdfmetrics.registerFont(TTFont(
            font,
            "data/Roboto-Regular.ttf",
            "UTF-8"
        ))
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = ("attachment; " 
                                           'filename="shopping_list.pdf"'
                                           )
        page = canvas.Canvas(response)
        page.setFont(font, size=24)
        page.drawString(180, 750, "Список покупок")
        page.setFont(font, size=16)
        height = 600
        for i, (name, data) in enumerate(shopping_dict.items(), 1):
            page.drawString(
                70,
                height,
                (
                    f"""{i}. {name} - {data["amount"]}"""
                    f"""{data["measurement_unit"]}"""
                ),
            )
            height -= 20
        page.showPage()
        page.save()
        return response

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        data = {"user": request.user.id, "recipe": pk}
        serializer = FavoritesSerializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(Favorites, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCustomViewSet(UserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if author == user:
            return Response(
                {"errors": "Попытка подписаться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance, created = Follow.objects.get_or_create(
            user=user,
            author=author
        )
        if not created:
            return Response(
                {"errors": "Подписка не была создана"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FollowCreateSerializer(
            instance.author, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        instance = Follow.objects.filter(user=user, author=author)
        if not instance.exists():
            return Response(
                {"errors": "Ошибка отписки"},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        following_authors = User.objects.filter(
            author_to_follow__user=self.request.user
        )

        page = self.paginate_queryset(following_authors)
        if page is not None:
            serializer = FollowCreateSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = FollowCreateSerializer(
            following_authors, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ("^name",)

    def get_paginated_response(self, data):
        return Response(data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_paginated_response(self, data):
        return Response(data)
