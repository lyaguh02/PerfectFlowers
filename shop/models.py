from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Manufacturer(models.Model):
    """
    Модель производителей для товара
    """
    name = models.CharField(max_length=255, help_text='Введите название производителя')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категорий для товара
    """
    name = models.CharField(max_length=255, help_text='Введите название категории')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, help_text='Сокращение для ссылки')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Модель товара
    """
    name = models.CharField(max_length=255, db_index=True, help_text="Введите название товара")
    image = models.ImageField(upload_to=f'products/', null=True, blank=True,
                              help_text="Вставьте изображение товара")
    slug = models.SlugField(max_length=200, db_index=True, help_text='Сокращение для ссылки')
    price = models.DecimalField(default=1.0, max_digits=10, decimal_places=2,
                                help_text="Введите цену товара")  # DECIMAL точнее FLOAT
    width = models.IntegerField(help_text="Введите ширину букета в сантиметрах")
    height = models.IntegerField(help_text="Введите высоту в сантиметрах")
    description = models.CharField(max_length=1000, default='', blank=True, help_text="Введите описание товара")
    category = models.ForeignKey(Category, models.CASCADE, help_text="Введите категорию товара")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def get_view_count(self):
        """
        Возвращает количество просмотров для товара
        """
        return self.views.count()


class ViewCount(models.Model):
    """
    Модель просмотров для товара
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.product.name
