# Generated by Django 3.0.3 on 2021-12-02 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211202_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apidata',
            name='dates',
            field=models.CharField(max_length=256, null=True),
        ),
    ]