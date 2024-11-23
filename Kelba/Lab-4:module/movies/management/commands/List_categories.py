from django.core.management.base import BaseCommand
from movies.models import Category

class Command(BaseCommand):
    help = 'Вивести всі категорії'

    def handle(self, *args, **kwargs):
        
        categories_info = Category.objects.all()

        if categories_info.exists():
            for category in categories_info:
                self.stdout.write(f"Category: {category.name}")
                self.stdout.write('---')
        else:
            self.stdout.write("No categories found.")
