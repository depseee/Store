from django.db import models
from users.models import User


class ProductCategory(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель информации о товаре"""
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    """Переопределение класса objects"""

    def total_sum(self):
        """Сумма всех товаров"""
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        """Количество всех товаров"""
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    """Модель корзины товаров"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    """Переопределение класса objects"""
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.name}'

    def sum(self):
        return self.product.price * self.quantity
