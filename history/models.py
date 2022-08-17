from django.contrib.auth.models import User
from django.db import models

from account.models import Liability

TRANSACTION_KIND = ((1, 'Income'), (2, 'Expense'), (3, 'Transfer'))


class Transaction(models.Model):
    timestamp = models.DateField()
    category = models.CharField(max_length=50)
    note = models.CharField(blank=True, max_length=150, null=True)
    kind = models.IntegerField(choices=TRANSACTION_KIND, default=1)

    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)

        Liability.objects.record(
            reference=self,
            amount=self.amount,
            user_id=self.user_id,
            account_id=self.account_id,
            kind='credit' if self.kind == 'Income' or (self.kind == 'Transfer' and self.amount > 0) else 'debit',
        )

        if self.account:
            self.account.update_legacy_balance()
