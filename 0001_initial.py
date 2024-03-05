# Generated by Django 5.0.3 on 2024-03-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TallyTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('party', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('voucher_type', models.CharField(max_length=50)),
            ],
        ),
    ]
