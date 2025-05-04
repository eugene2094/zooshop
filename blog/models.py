from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категорія")
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts", verbose_name="Категорія")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="Короткий опис")
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True, verbose_name="Обкладинка")
    content = models.TextField(verbose_name="Зміст")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name="Опубліковано")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Публікація"
        verbose_name_plural = "Публікації"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

