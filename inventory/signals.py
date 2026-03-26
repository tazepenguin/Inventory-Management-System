from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Product

@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    if instance.is_low_stock():
        subject = f'Low Stock Alert: {instance.name}'
        message = f'Product {instance.name} (SKU: {instance.sku}) is low on stock.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER], fail_silently=True)