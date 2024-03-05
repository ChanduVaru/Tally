from django.db import models

class TallyTransaction(models.Model):
    date = models.DateField()
    party = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    voucher_type = models.CharField(max_length=50)