from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    delivery_time = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/')
    slug = models.SlugField(unique=True, blank=True)
    instock = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug}) 
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically set the 'instock' field based on the stock value
        self.instock = self.stock > 0
        if not self.slug:
            base_slug = slugify(self.name)
            new_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=new_slug).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = new_slug
        super().save(*args, **kwargs)