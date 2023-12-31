# Generated by Django 4.2.1 on 2023-08-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Return', 'Return'), ('Processing', 'Processing'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.FloatField(max_length=150),
        ),
    ]
