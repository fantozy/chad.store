import random
from faker import Faker

from django.core.management.base import BaseCommand

from products.models import Product

fake = Faker()

class Command(BaseCommand):
    help = "Generate 500 random products"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting product generation...'))

        products = []
        currencies = ["GEL", "USD", "EUR"]

        for _ in range(500):
            name = fake.word().capitalize() + " " + fake.word().capitalize()
            description = fake.sentence()
            price = round(random.uniform(10, 5000), 2)  # Random price between 10 and 5000
            currency = random.choice(currencies)
            quantity = random.randint(1, 100)

            product = Product(
                name=name,
                description=description,
                price=price,
                currency=currency,
                quantity=quantity,
            )
            products.append(product)

        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS('Successfully created 500 products!'))
