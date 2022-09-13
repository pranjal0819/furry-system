# Generated by Django 4.1 on 2022-09-06 09:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hidden', models.BooleanField(default=False)),
                (
                    'kind',
                    models.IntegerField(
                        choices=[(1, 'Cash'), (2, 'Account'), (3, 'Credit'), (4, 'Saving'), (5, 'Loan')], default=1
                    ),
                ),
                ('settings', models.JSONField(blank=True, default=dict, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Liability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.IntegerField()),
                ('reference_type', models.CharField(max_length=50)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    'account',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.account'
                    ),
                ),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
