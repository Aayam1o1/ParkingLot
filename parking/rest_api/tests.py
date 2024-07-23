from celery import shared_task
from django.test import TestCase


# Create your tests here.
@shared_task
def add(x, y):
    return x + y
