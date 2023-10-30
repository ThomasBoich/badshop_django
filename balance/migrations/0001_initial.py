# Generated by Django 4.2.5 on 2023-10-30 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Промокод')),
                ('valid_from', models.DateTimeField(blank=True, null=True, verbose_name='Действителен с')),
                ('valid_to', models.DateTimeField(blank=True, null=True, verbose_name='Действителен до')),
                ('seil', models.IntegerField(default=0, max_length=3, verbose_name='Скидка в %')),
            ],
            options={
                'verbose_name': 'Промокод',
                'verbose_name_plural': 'Промокоды',
            },
        ),
        migrations.CreateModel(
            name='BonusWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bonus_wallet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Бонусный кошелёк',
                'verbose_name_plural': 'Бонусные кошельки',
            },
        ),
    ]