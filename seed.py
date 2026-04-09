import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_project.settings')
django.setup()

from products.models import Product, Category, Brand

Category.objects.all().delete()
Brand.objects.all().delete()
Product.objects.all().delete()

cat = Category.objects.create(name='Eletrônicos')
brand = Brand.objects.create(name='Generica')

Product.objects.create(title='Notebook', category=cat, brand=brand, quantity=3, selling_price=1000.00)
Product.objects.create(title='Teclado', category=cat, brand=brand, quantity=5, selling_price=100.00)
Product.objects.create(title='Monitor', category=cat, brand=brand, quantity=8, selling_price=500.00)
Product.objects.create(title='Mouse', category=cat, brand=brand, quantity=15, selling_price=50.00)

print("Dados inseridos com sucesso!")
