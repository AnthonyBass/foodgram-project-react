from django.contrib import admin

from .models import AmountIngredientRecipe, Cart, Favorites, Ingredient, Recipe, Tag


class AmountIngredientInRecipeAdmin(admin.TabularInline):
    model = AmountIngredientRecipe
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        "count_favorites",
    )
    search_fields = ("author", "name", "tags")
    list_filter = ("author", "name", "tags")
    inlines = [AmountIngredientInRecipeAdmin]

    @staticmethod
    def count_favorites(obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(AmountIngredientRecipe)
class AmountIngredientRecipeAdmin(admin.ModelAdmin):
    pass
