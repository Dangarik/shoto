# Generated by Django 5.2.4 on 2025-07-04 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Чоловік'), ('FEMALE', 'Жінка'), ('UNDIFINED', 'Не визначено')], max_length=10, verbose_name='Стать'),
        ),
    ]
