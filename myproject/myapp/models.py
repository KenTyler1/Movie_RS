from datetime import datetime
from distutils.command.upload import upload
from django.db import models
import datetime
import os
import pickle

# Create your models here.
with open('./model/movie_list.pkl', 'rb') as m:
    movies = pickle.load(m)
with open('./model/similarity.pkl', 'rb') as s:
    similarity = pickle.load(s)


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('./static/assets/images/movies/', filename)

class Movie(models.Model):
    img = models.ImageField(upload_to = filepath, null = True, blank = True)
    rate = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    cate = models.CharField(max_length=500)
    year = models.CharField(max_length=100)