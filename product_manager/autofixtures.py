""" This file creates test data for Product and Category using the autofixture class. """

from django.conf import settings
from django.db import models as models
from django.db.models import *
from .models import Product, Category
from autofixture import generators, register, AutoFixture



# быстрая генерация данных
class ProductAutoFixture(AutoFixture):
    field_values = {
        'name': generators.ChoicesGenerator(
            values=(
                "Iphone",
                "Sumsung",
                "Xiaomi",
                "Watches",
                "Honor",
                "Redmi",
            )
        ),
        'description': generators.ChoicesGenerator(
            values=(
                "Some phone",
                "Very good",
                "Best phone ever",
                "Now on sale!"
            )
        ),
        'price': generators.ChoicesGenerator(
            values=(
                '15.45',
                '2.00',
                '14.00',
                '10.05'
            )
        ),
    }


register(Product, ProductAutoFixture)


class CategoryAutoFixture(AutoFixture):
    field_values = {
        'name': generators.ChoicesGenerator(
            values=(
                "Phone",
                "Headphones",
                "Watches"
            )
        ),
    }


register(Category, CategoryAutoFixture)
