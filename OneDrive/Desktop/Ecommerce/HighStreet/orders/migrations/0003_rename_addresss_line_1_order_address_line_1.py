# Generated by Django 4.2.4 on 2023-09-17 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_first_number_order_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='addresss_line_1',
            new_name='address_line_1',
        ),
    ]
