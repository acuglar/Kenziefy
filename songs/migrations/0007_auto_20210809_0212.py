# Generated by Django 3.2.4 on 2021-08-09 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0006_alter_playlist_songs'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='formed_in',
            field=models.IntegerField(default=2021),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='status',
            field=models.CharField(default='Active', max_length=255),
            preserve_default=False,
        ),
    ]
