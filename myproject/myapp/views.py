from ast import literal_eval
import email
from django.shortcuts import redirect, render
from django.http import HttpResponse
from requests import request
from .models import Movie, movies,  similarity
from django.contrib.auth.models import User, auth
from django.contrib import messages
# import json
# import urllib.request
import requests
# Create your views here.

def index(request):
    movies_class = Movie.objects.all()
    movie_list = movies['title'].values
    if request.method == 'POST':
        recomd = request.POST['search']
        if recomd == "":
            return render(request,'index.html',{'movies' : movies_class, 'movies_list': movie_list})
        else:
            # Gợi ý dựa trên nội dung Heroku
            # lấy áp phích movie
            index = movies[movies['title'] == recomd].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_movie_names = []
            recommended_movie_posters = []
            recommended_movie_votes = []
            recommended_movie_dates = []
            recommended_movie_genres = []
            for i in distances[1:8]:
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)
                recommended_movie_votes.append(movies.iloc[i[0]].vote_average)
                recommended_movie_dates.append(movies.iloc[i[0]].release_date)
                recommended_movie_genres.append(movies.iloc[i[0]].genres)
                for x in recommended_movie_genres:
                    mystring = ', '.join(x)
                    print(mystring)
                lists = zip(recommended_movie_posters,recommended_movie_names,recommended_movie_votes,recommended_movie_dates,recommended_movie_genres)
            return render(request, 'index.html', {'lists':lists})
    else:
        return render(request,'index.html',{'movies' : movies_class, 'movies_list': movie_list})

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def login_register(request):
    if 'login' in request.POST:
        # Đăng nhập
        username1 = request.POST['username']
        password1 = request.POST['password']

        user = auth.authenticate(username = username1, password = password1)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credential Invalid')
            return redirect('login_register')   
    elif 'register' in request.POST:
        username = request.POST['userName']
        email = request.POST['eMail']
        password = request.POST['passWord']
        password2 = request.POST['rePassword']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email đã được sử dụng') 
                return redirect('login_register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username đã được sử dụng') 
                return redirect('login_register')
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save();
                return redirect('/')
        else:
            messages.info(request, 'Password không giống')
            return redirect('login_register')
    else:
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')