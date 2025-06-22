from django.db import models
from django.utils import timezone


class Organization(models.Model):
    name = models.TextField(max_length=40)
    inn = models.TextField(max_length=12)
    balance = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'({self.id})\n' \
               f'name: {self.name}\n' \
               f'inn: {self.inn}\n' \
               f'balance: {self.balance}'


class Payment(models.Model):
    operation_id = models.UUIDField(primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payer_inn = models.TextField(max_length=12)
    document_number = models.TextField(max_length=255)
    document_date = models.DateTimeField()
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)


class PaymentTransaction(models.Model):
    operation_id = models.UUIDField(primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payer_inn = models.TextField(max_length=12)
    payment_date = models.DateTimeField()
    status = models.TextField(max_length=30)
