# Generated by Django 4.1.6 on 2023-04-07 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fingerpaint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby_name', models.CharField(max_length=50)),
            ],
        ),
    ]
