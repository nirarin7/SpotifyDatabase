from django.db import models

# Create your models here.

# class Track(models.Model):



class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_type = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_type

    class Meta:
        db_table = "genre"

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.country

    class Meta:
        db_table = "country"

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=650)
    followers = models.IntegerField()

    def __str__(self):
        return self.artist

    class Meta:
        db_table = "artist"


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=350)
    tracks_in_album = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "album"

class Track(models.Model):
    uri = models.CharField(max_length=60, primary_key=True)
    title = models.CharField(max_length=250)
    release_date = models.DateField()
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    key = models.IntegerField(null=True)
    loudness = models.FloatField(null=True)
    mode = models.BooleanField(null=True)
    speechiness = models.FloatField(null=True)
    acoustics = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    valence = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    duration = models.IntegerField(null=True)
    track_number_album = models.IntegerField(null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    country_track = models.ManyToManyField(Country, through="Popularity")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "track"

class Popularity(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    popularity = models.FloatField()

    def __str__(self):
        return f"Track: {self.track.title}, Country: {self.country.country}, Popularity: {str(self.popularity)}"

    class Meta:
        db_table = "popularity"
