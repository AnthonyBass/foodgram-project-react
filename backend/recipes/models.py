from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
	name = models.CharField('Название ингредиента', max_length = 50)
	measurement_unit = models.CharField('Единица измерения', max_length = 50)

	class Meta:
		verbose_name = 'Ингредиент'
		verbose_name_plural = 'Ингредиенты'

	def __str__(self):
		return f'{self.name} - {self.measurement_unit}.'


class Tag(models.Model):
	name = models.CharField('Название тега', max_length = 50, unique = True)
	color = models.CharField('Цвет', max_length = 50, unique = True)
	slug = models.SlugField('Slug', unique = True)

	class Meta:
		verbose_name = 'Тег'
		verbose_name_plural = 'Теги'

	def __str__(self):
		return self.name


class Recipe(models.Model):
	publication_date = models.DateTimeField('Дата публикации',
											auto_now_add = True)

	author = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		related_name = 'recipes',
		verbose_name = 'Автор')
	name = models.CharField('Название', max_length = 200)
	image = models.ImageField(
		'Изображение',
		upload_to = 'photo/',
		null = False,
		default = None
	)
	text = models.TextField('Описание')

	ingredients = models.ManyToManyField(
		Ingredient,
		related_name = 'recipes',
		through = 'AmountIngredientRecipe',
		verbose_name = 'Ингредиенты'
	)
	tags = models.ManyToManyField(
		Tag,
		related_name = 'recipes',
		verbose_name = 'Теги')

	cooking_time = models.PositiveIntegerField(
		'Время приготовления (в минутах)',
		validators = (
			MinValueValidator(1, message = 'Введите значение от 1 минуты'),
		)
	)

	class Meta:
		verbose_name = 'Рецепт'
		verbose_name_plural = 'Рецепты'
		ordering = ['-publication_date']

	def __str__(self):
		return self.name


class AmountIngredientRecipe(models.Model):
	recipe = models.ForeignKey(
		Recipe,
		on_delete = models.CASCADE,
		related_name = 'amount',
		verbose_name = 'Рецепт'
	)
	ingredient = models.ForeignKey(
		Ingredient,
		on_delete = models.CASCADE,
		related_name = 'amount',
		verbose_name = 'Ингредиент'
	)
	amount = models.SmallIntegerField(
		'Количество',
		validators = (
			MinValueValidator(1, message = 'Введите значение от 1'),
		)
	)

	class Meta:
		verbose_name = 'Количество ингредиента'
		verbose_name_plural = 'Количество ингредиентов'
		constraints = (
			models.UniqueConstraint(
				fields = (
					'recipe',
					'ingredient',
				),
				name = 'unique_recipe_amount_ingredient',
			),
		)

	def __str__(self):
		return f"""В рецепте: {self.recipe}, ингередиент {(str(self.ingredient)).split('-')[0]} в количестве {self.amount} {(str(self.ingredient)).split('-')[1]}"""


class Favorites(models.Model):
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		related_name = 'favorites',
		verbose_name = 'Пользователь')

	recipe = models.ForeignKey(
		Recipe,
		on_delete = models.CASCADE,
		related_name = 'favorites',
		verbose_name = 'Рецепт')

	class Meta:
		verbose_name = 'Избранное'
		verbose_name_plural = 'Избранные'
		constraints = [
			models.UniqueConstraint(
				fields = ('user', 'recipe'),
				name = 'unique_favorites_user_recipe')
		]

	def __str__(self):
		return f'Рецепт {self.recipe} в избранном у пользователя {self.user}.'


class Cart(models.Model):
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		related_name = 'cart',
		verbose_name = 'Пользователь', )
	recipe = models.ForeignKey(
		Recipe,
		on_delete = models.CASCADE,
		related_name = 'cart',
		verbose_name = 'Рецепт', )

	class Meta:
		verbose_name = 'Корзина'
		verbose_name_plural = 'Корзины'
		constraints = [
			models.UniqueConstraint(
				fields = ('user', 'recipe'),
				name = 'unique_cart_user_recipe'),
		]

	def __str__(self):
		return f'Рецепт {self.recipe} в корзине у пользователя {self.user}.'
