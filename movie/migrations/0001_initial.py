# Generated by Django 3.2 on 2021-08-27 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RatingsSmall',
            fields=[
                ('index', models.IntegerField(db_column='index', primary_key=True, serialize=False)),
                ('userid', models.CharField(db_column='userId', max_length=10)),
                ('movieid', models.CharField(db_column='movieId', max_length=10)),
                ('rating', models.CharField(max_length=10)),
                ('timestamp', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'ratings_small',
            },
        ),
    ]
