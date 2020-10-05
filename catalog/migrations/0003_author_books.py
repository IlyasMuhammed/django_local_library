# Generated by Django 3.1.1 on 2020-09-19 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200913_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(help_text='select a book', related_name='author_book', to='catalog.Book'),
        ),
    ]