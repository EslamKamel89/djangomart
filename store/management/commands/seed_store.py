from decimal import Decimal
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from store.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with initial categories and products."
    data = [
        {
            "name": "Laptops & Computers",
            "products": [
                {
                    "title": 'Ultrabook 14" i5 · 16GB RAM · 512GB SSD',
                    "brand": "TechPro",
                    "description": (
                        "Lightweight 14-inch ultrabook with Intel Core i5, 16GB RAM, "
                        "512GB NVMe SSD, and all-day battery. Perfect for work and study."
                    ),
                    "price": Decimal("899.99"),
                },
                {
                    "title": 'Gaming Laptop 15.6" RTX 4060 · 16GB RAM',
                    "brand": "RedDragon",
                    "description": (
                        "15.6-inch gaming laptop with RTX 4060, 16GB RAM, 1TB SSD, "
                        "and 144Hz display. Built for smooth 1080p gaming."
                    ),
                    "price": Decimal("1399.00"),
                },
                {
                    "title": 'Everyday Laptop 15" i3 · 8GB RAM · 256GB SSD',
                    "brand": "EverydayTech",
                    "description": (
                        "Affordable 15-inch laptop ideal for browsing, office work, "
                        "and online learning."
                    ),
                    "price": Decimal("499.00"),
                },
                {
                    "title": '27" 2K IPS Monitor · 75Hz',
                    "brand": "ViewLine",
                    "description": (
                        "27-inch QHD IPS monitor with thin bezels and 75Hz refresh rate, "
                        "great for productivity and casual gaming."
                    ),
                    "price": Decimal("279.50"),
                },
            ],
        },
        {
            "name": "Home & Kitchen",
            "products": [
                {
                    "title": "Stainless Steel Electric Kettle · 1.7L",
                    "brand": "KitchenFlow",
                    "description": (
                        "Fast-boil 1.7L kettle with auto shut-off and boil-dry protection. "
                        "Brushed stainless steel finish."
                    ),
                    "price": Decimal("39.99"),
                },
                {
                    "title": "Non-Stick Cookware Set · 8 Pieces",
                    "brand": "HomeChef",
                    "description": (
                        "Durable non-stick cookware set including pans, pots, and lids. "
                        "Suitable for gas and electric stoves."
                    ),
                    "price": Decimal("129.00"),
                },
                {
                    "title": "Air Fryer · 4.5L Family Size",
                    "brand": "CrispyBite",
                    "description": (
                        "Healthier frying with up to 90% less oil. 4.5L basket, "
                        "digital controls, and presets for fries, chicken, and more."
                    ),
                    "price": Decimal("159.99"),
                },
                {
                    "title": "Glass Food Storage Containers · Set of 10",
                    "brand": "FreshBox",
                    "description": (
                        "Airtight glass containers with locking lids, safe for fridge, "
                        "freezer, oven, and microwave."
                    ),
                    "price": Decimal("54.50"),
                },
            ],
        },
        {
            "name": "Sports & Outdoors",
            "products": [
                {
                    "title": "Adjustable Dumbbell Set · 20kg",
                    "brand": "FitStrong",
                    "description": (
                        "Adjustable dumbbell set with plates and spinlock collars, "
                        "ideal for home workouts."
                    ),
                    "price": Decimal("89.99"),
                },
                {
                    "title": "Yoga Mat · 6mm Non-Slip",
                    "brand": "ZenFlex",
                    "description": (
                        "Comfortable 6mm yoga mat with textured, non-slip surface. "
                        "Includes carrying strap."
                    ),
                    "price": Decimal("24.99"),
                },
                {
                    "title": "Insulated Stainless Steel Water Bottle · 1L",
                    "brand": "TrailHydro",
                    "description": (
                        "Double-wall insulated bottle keeps drinks cold for 24 hours "
                        "or hot for 12 hours."
                    ),
                    "price": Decimal("29.50"),
                },
                {
                    "title": "Camping Tent · 3-Person",
                    "brand": "OutdoorHaven",
                    "description": (
                        "Lightweight 3-person dome tent with waterproof flysheet and "
                        "easy setup. Great for weekend camping trips."
                    ),
                    "price": Decimal("179.00"),
                },
            ],
        },
    ]

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write(
            self.style.WARNING("Clearing existing products and categories...")
        )
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Existing data cleared."))
        created_categories = 0
        created_products = 0
        for category_data in self.data:
            category_name = category_data["name"]
            category_slug = slugify(category_name)
            category = Category.objects.create(name=category_name, slug=category_slug)
            created_categories += 1
            for product_data in category_data["products"]:
                product_slug = slugify(product_data["title"])
                Product.objects.create(
                    title=product_data["title"],
                    brand=product_data["brand"],
                    description=product_data["description"],
                    slug=product_slug,
                    price=product_data["price"],
                    category=category,
                )
                created_products += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding completed: {created_categories} categories, "
                f"{created_products} products created."
            )
        )
