# Generated by Django 4.2.5 on 2023-10-31 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0001_initial'),
        ('items', '0016_alter_item_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='balance.promocode', verbose_name='Промокод'),
        ),
    ]