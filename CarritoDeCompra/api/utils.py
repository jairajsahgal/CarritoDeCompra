from math import prod
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
from api.models import Gorras, Camiseta


def update_stock():
    for product in Gorras.objects.all():
        product.current_stock = calculate_new_stock_value()
        product.save()

    for product in Camiseta.objects.all():
        product.current_stock = calculate_new_stock_value()
        product.save()


def calculate_new_stock_value():
    return 5
