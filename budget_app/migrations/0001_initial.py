# Generated by Django 2.2 on 2020-02-28 11:41

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
            name='UserIncome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_name', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField()),
                ('income', models.FloatField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_income', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_name', models.CharField(max_length=255)),
                ('cost', models.FloatField()),
                ('date_added', models.DateTimeField()),
                ('category', models.CharField(choices=[('rent', 'Rent'), ('grocery', 'Grocery'), ('shopping', 'Shopping'), ('gym', 'Gym'), ('phone', 'Phone'), ('freetime', 'Freetime'), ('other', 'Other')], max_length=25)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_spending', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
