# Generated by Django 5.1.2 on 2024-10-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0008_order_paid_order_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='additional_info',
        ),
        migrations.AlterField(
            model_name='order',
            name='postcode',
            field=models.IntegerField(null=True),
        ),
    ]
