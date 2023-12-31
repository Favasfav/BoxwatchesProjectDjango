# Generated by Django 4.2.1 on 2023-07-26 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(default=None, max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Description', models.TextField(default=None, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('specification', models.TextField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('img1', models.ImageField(upload_to='products/')),
                ('img2', models.ImageField(upload_to='products/')),
                ('img3', models.ImageField(upload_to='products/')),
                ('img4', models.ImageField(upload_to='products/')),
                ('stock', models.PositiveIntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_category', models.CharField(choices=[('color', 'Color'), ('item_type', 'Item Type')], default='color', max_length=255)),
                ('variation_value', models.CharField(default=None, max_length=25)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.product')),
            ],
        ),
    ]
