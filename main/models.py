from django.db import models
from slugify import slugify

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва товару")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL (Код товару)")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    available = models.BooleanField(default=True, verbose_name="В наявності")
    warranty_months = models.IntegerField(default=12, verbose_name="Гарантія (місяців)")
    nova_poshta = models.BooleanField(default=True, verbose_name="Нова пошта")
    ukr_poshta = models.BooleanField(default=True, verbose_name="Укрпошта")
    pickup = models.BooleanField(default=True, verbose_name="Самовивіз")
    other_delivery = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Інший спосіб доставки (текст)"
    )

    def get_delivery_list(self):
        methods = []
        if self.nova_poshta:
            methods.append("Новою поштою")
        if self.ukr_poshta:
            methods.append("Укрпоштою")
        if self.pickup:
            methods.append("Самовивіз")
        if self.other_delivery:
            methods.append(self.other_delivery)
        return ", ".join(methods)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
    image = models.ImageField(upload_to='products/', verbose_name="Зображення")

    def __str__(self):
        return f"Фото для {self.product.title}"

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова Пошта'),
        ('ukr_poshta', 'Укрпошта'),
        ('pickup', 'Самовивіз'), 
    ]

    first_name = models.CharField(max_length=250, verbose_name="Прізвище та ім'я")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    delivery_service = models.CharField(
        max_length=20, 
        choices=DELIVERY_CHOICES, 
        default='nova_poshta', 
        verbose_name="Служба доставки"
    )
    
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Місто")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Відділення / Адреса")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def __str__(self):
        return f"Замовлення #{self.id} — {self.first_name} ({self.delivery_service})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_title = models.CharField(max_length=200, verbose_name="Назва товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.product_title} x {self.quantity}"