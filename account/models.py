from django.contrib.auth.models import User
from django.db import models

ACCOUNT_KIND = ((1, 'Cash'), (2, 'Account'), (3, 'Credit'), (4, 'Saving'), (5, 'Loan'))


class Account(models.Model):
    name = models.CharField(max_length=50)
    visible = models.BooleanField(default=True)
    kind = models.IntegerField(choices=ACCOUNT_KIND, default=1)
    settings = models.JSONField(blank=True, default=dict, null=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def update_legacy_balance(self):
        balance = self.liability_set.aggregate(credit=models.Sum('credit'), debit=models.Sum('debit'))
        self.balance = (balance['credit']) - (balance['debit'])
        self.save(update_fields=['balance'])


class LiabilityManager(models.Manager):
    def record(self, amount, kind, reference, account_id, user_id):
        liability, _ = self.get_or_create(reference_id=reference.id, reference_type='Transaction', user_id=user_id)

        liability.account_id = account_id
        liability.credit, liability.debit = (amount, 0) if kind == 'credit' else (0, amount)

        return liability.save(update_fields=['account_id', 'credit', 'debit'])


class Liability(models.Model):
    reference_id = models.IntegerField()
    reference_type = models.CharField(max_length=50)

    credit = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    debit = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, blank=True, null=True)

    objects = LiabilityManager()

    def __str__(self):
        return f'{self.reference_type}_{self.reference_id}'
