from django.contrib.auth.models import User
from django.db import models

ACCOUNT_KIND = ((1, 'Cash'), (2, 'Account'), (3, 'Credit'), (4, 'Saving'), (5, 'Loan'))


class Account(models.Model):
    name = models.CharField(max_length=50)
    hidden = models.BooleanField(default=False)
    kind = models.IntegerField(choices=ACCOUNT_KIND, default=1)
    settings = models.JSONField(blank=True, default=dict, null=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def update_legacy_balance(self):
        balance = self.liability_set.aggregate(credit=models.Sum('credit'), debit=models.Sum('debit'))
        self.balance = balance['credit'] or 0 - balance['debit'] or 0
        self.save(update_fields=['balance'])


class LiabilityManager(models.Manager):
    def record(self, amount, kind, reference, account_id, user_id):
        liability, _ = self.get_or_create(reference_id=reference.id, reference_type='Transaction', user_id=user_id)

        liability.account_id = account_id
        liability.credit = amount
        liability.debit = amount

        return liability.save(update_fields=['account_id', kind])


class Liability(models.Model):
    reference_id = models.IntegerField()
    reference_type = models.CharField(max_length=50)

    credit = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    debit = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, blank=True, null=True)

    objects = LiabilityManager()

    def __str__(self):
        return f'{self.reference_type}_{self.reference_id}'
