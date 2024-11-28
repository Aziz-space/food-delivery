# Generated by Django 5.1.3 on 2024-11-11 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_birth_date_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('client', 'Покупатель'), ('salesman', 'Продавец'), ('admin', 'Администратор')], default='client', max_length=15, null=True, verbose_name='роль'),
        ),
    ]
