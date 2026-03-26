from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from inventory.models import Product, Transaction, Stock, Location, Category
from sales.models import Customer, SalesOrder

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **options):
        groups = {
            'Super Admin': [],  # superuser gets all anyway
            'Warehouse Manager': [
                'add_product', 'change_product', 'delete_product', 'view_product',
                'add_transaction', 'view_transaction',
                'view_stock', 'change_stock',
                'view_location',
                'view_report',
                'add_customer', 'change_customer', 'view_customer',
                'add_salesorder', 'change_salesorder', 'view_salesorder',
            ],
            'Staff': [
                'view_product', 'add_transaction', 'view_transaction',
                'view_stock',
                'view_customer', 'view_salesorder',
            ],
            'Auditor': [
                'view_product', 'view_transaction', 'view_stock',
                'view_customer', 'view_salesorder', 'view_report',
            ],
        }

        models = [Product, Transaction, Stock, Location, Category, Customer, SalesOrder]
        for group_name, perm_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Created group {group_name}')
            group.permissions.clear()
            for codename in perm_codenames:
                perm = Permission.objects.filter(codename=codename).first()
                if perm:
                    group.permissions.add(perm)
                else:
                    self.stdout.write(self.style.WARNING(f'Permission {codename} not found'))
            self.stdout.write(self.style.SUCCESS(f'Assigned permissions to {group_name}'))