# Generated by Django 4.0.1 on 2022-02-12 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clickoh', '0006_alter_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='test',
        ),
    ]
