# Generated by Django 4.2.3 on 2023-08-01 07:33

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
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_bills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('decimals', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_date', models.DateField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.bill')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bill.currency')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='display_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bill.currency'),
        ),
        migrations.AddField(
            model_name='bill',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='participating_bills', to=settings.AUTH_USER_MODEL),
        ),
    ]
