import webcolors
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (AmountIngredientRecipe, Cart, Favorites,
                            Ingredient, Recipe, Tag)
from users.models import Follow

User = get_user_model()


class Hex2NameColor(serializers.Field):
    """Для представления цвета в формате HEX"""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("Для этого цвета нет имени")
        return data


class IngredientSerializer(serializers.ModelSerializer):
    """Для получения одного или более ингредиентов"""

    class Meta:
        model = Ingredient
        fields = "__all__"


class AddingIngredientAmountSerializer(serializers.ModelSerializer):
    """Для добавления одного или более ингредиентов
    с информацией о количестве"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredientRecipe
        fields = ("id", "amount")


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Для представления одного или более ингредиентов
    с информацией о количестве"""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = AmountIngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    """Для представления одного или более тегов"""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = "__all__"


class CreateUserSerializer(UserCreateSerializer):
    """Для создания пользователя"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserCustomSerializer(UserSerializer):
    """Для представления автора с
    указанием наличия подписки на него"""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Для представления одного или более рецептов"""

    image = Base64ImageField()

    author = UserCustomSerializer(read_only=True, many=False)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_ingredients(self, obj):
        queryset = AmountIngredientRecipe.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(user=request.user, recipe=obj).exists()


class RecipeSerializerShort(serializers.ModelSerializer):
    """Серилизатор для частичной выдачи полей рецепта"""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для создания рецепта"""

    image = Base64ImageField(required=True, use_url=False)

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddingIngredientAmountSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "ingredients",
            "name",
            "text",
            "cooking_time",
            "image",
        )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    @staticmethod
    def create_ingredients(ingredients, recipe):
        ingredients_list = [
            AmountIngredientRecipe(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
        AmountIngredientRecipe.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return RecipeSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        AmountIngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop("tags"), instance)
        self.create_ingredients(validated_data.pop("ingredients"), instance)
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок"""

    class Meta:
        model = Cart
        fields = (
            "user",
            "recipe",
        )

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return RecipeSerializerShort(instance.recipe, context=context).data


class FavoritesSerializer(serializers.ModelSerializer):
    """Серилизатор для добавления в избранные"""

    class Meta:
        model = Favorites
        fields = "__all__"


class FollowCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для работы с подписками"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = Recipe.objects.filter(author=obj)
        if limit:
            recipes = recipes[: int(limit)]
        return RecipeSerializerShort(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
