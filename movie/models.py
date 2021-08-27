from django.db import models

# Create your models here.
class RatingsSmall(models.Model):
    index = models.IntegerField(db_column='index', primary_key=True)
    userid = models.CharField(db_column='userId', max_length=10)  # Field name made lowercase.
    movieid = models.CharField(db_column='movieId', max_length=10)  # Field name made lowercase.
    rating = models.CharField(max_length=10)
    timestamp = models.CharField(max_length=16)

    class Meta:
        # managed = False
        db_table = 'ratings_small'
