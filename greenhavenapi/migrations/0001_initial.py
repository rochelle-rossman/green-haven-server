# Generated by Django 4.1.6 on 2023-02-14 22:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import greenhavenapi.models.payment_method


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(choices=[('living_room', 'Living Room'), ('bedroom', 'Bedroom'), ('office', 'Office'), ('bathroom', 'Bathroom')], max_length=15)),
                ('style', models.CharField(choices=[('modern', 'Modern'), ('industrial', 'Industrial'), ('bohemian', 'Bohemian'), ('farmhouse', 'Farmhouse'), ('traditional', 'Traditional'), ('midcentury_modern', 'Midcentury Modern')], max_length=25)),
                ('image_url', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_on', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image_url', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(99999.99)])),
                ('inventory', models.IntegerField()),
                ('product_type', models.CharField(choices=[('houseplant', 'Houseplant'), ('home_decor', 'Home/Decor'), ('plant_care', 'Plant Care'), ('planters_stands', 'Planters/Stands')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=25, unique=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=40)),
                ('street_address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField()),
                ('created_on', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='HomeDecor',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='greenhavenapi.product')),
                ('style', models.CharField(choices=[('modern', 'Modern'), ('industrial', 'Industrial'), ('bohemian', 'Bohemian'), ('farmhouse', 'Farmhouse'), ('traditional', 'Traditional'), ('midcentury_modern', 'Midcentury Modern')], max_length=20)),
            ],
            bases=('greenhavenapi.product',),
        ),
        migrations.CreateModel(
            name='Houseplant',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='greenhavenapi.product')),
                ('light_level', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('water_needs', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('care_level', models.CharField(choices=[('novice', 'Novice'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], max_length=20)),
                ('pet_friendly', models.BooleanField(default=False)),
            ],
            bases=('greenhavenapi.product',),
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.design')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.product')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('card_number', models.CharField(max_length=16, validators=[greenhavenapi.models.payment_method.validate_card_number])),
                ('expiration_date', models.CharField(max_length=5, validators=[greenhavenapi.models.payment_method.validate_expiration_date])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.user')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='greenhavenapi.paymentmethod'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='greenhavenapi.ProductOrder', to='greenhavenapi.product'),
        ),
    ]
