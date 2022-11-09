from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


class Follow(models.Model):
	user = models.ForeignKey(
		MyUser,
		on_delete = models.CASCADE,
		related_name = 'follower',
		verbose_name = 'Подписчик', )
	author = models.ForeignKey(
		MyUser,
		on_delete = models.CASCADE,
		related_name = 'author_to_follow',
		verbose_name = 'Автор',

	)

	class Meta:
		verbose_name = 'Подписка'
		verbose_name_plural = 'Подписки'
		constraints = [
			models.UniqueConstraint(
				fields = ('user', 'author'),
				name = 'unique_follower_user_author'),
		]

	def __str__(self):
		return f'Подписка пользователя {self.user} на {self.author}.'
