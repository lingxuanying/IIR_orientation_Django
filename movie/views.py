from django.shortcuts import render
from pandas.core.base import DataError
from movie import models
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from movie.models import RatingsSmall
import pickle
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from django_pandas.io import read_frame
from sklearn.model_selection import train_test_split
import csv
import MySQLdb
import pandas as pd
from django.http import HttpResponseRedirect
'''
def import_csv(request):
    mydb = MySQLdb.connect(host='db',
        user='root',
        passwd='123',
        db='iir_orientation_hw7')
    cursor = mydb.cursor()
    sql = """LOAD DATA INFILE './model/ratings_small.csv'
    INTO TABLE ratings_small
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;"""
    cursor.execute(sql)

    #close the connection to the database.
    cursor.close()
    return HttpResponse('Import csv complete')

'''
def import_csv(request):
    try:
        data = pd.read_csv('./model/ratings_small_2.csv', nrows=1000)
        df_records = data.to_dict('records')
        RatingsSmall.objects.bulk_create(
            RatingsSmall(**vals) for vals in data.to_dict('records')
        )
        return HttpResponse("Table already exist!")
    except:
        return HttpResponse("Table already exist!")




# Create your views here.
def hello_view(request):
    return render(request, 'info.html', {
        'data': "Hello Django ",
    })

def info(request):
    articles = RatingsSmall.objects.all()
    paginator = Paginator(articles, 20)  # Show 10 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    context = {'contacts': contacts}
    return render(request, "info.html",{'contacts': contacts}) #必须用这个return

# POST
@csrf_exempt
def show_post(request):
    if 'ok' in request.POST:
        try:
            userid = request.POST['userid']
            movieid = request.POST['movieid']
            print(userid, movieid)
            RatingsSmall.objects.filter(userid=userid, movieid=movieid).delete()
            #return JsonResponse({"userid": userid, "movieid": movieid, "rating": rating, "timestamp": timestamp})
            return render(request, "index.html")
        except:
            #return JsonResponse({"status": 1})
            return HttpResponse('ERROR')



def index(request):
    return render(request, "index.html") #必须用这个return

def search(request, num):
    articles = RatingsSmall.objects.filter(userid=num)
    return render(request, "search.html",{'articles': articles}) #必须用这个return\

def update(request, user, movie, rating):
    try:
        RatingsSmall.objects.filter(userid=user, movieid=movie).update(rating=rating)
        articles = RatingsSmall.objects.filter(userid=user, movieid=movie)
        if(len(articles)==0):
            return HttpResponse("此user, movie組合不存在")
        else:
            return render(request, "search.html",{'articles': articles})
    except:
        return HttpResponse("此user, movie組合不存在")

# POST
@csrf_exempt
def model(request):
    if 'ok2' in request.POST:
        try:
            userid2 = request.POST['userid2']
            qs = RatingsSmall.objects.all()
            data = read_frame(qs)
            data['rating'] = data['rating'].astype(float)
            data['rating'] = data['rating'] / data['rating'].max()
            target = data['rating']
            del data['rating']
            x_train, x_test, y_train, y_test = train_test_split(data, target, train_size=0.8, random_state=5)

            qs = RatingsSmall.objects.filter(userid=userid2)
            df = read_frame(qs)
            del df['rating']
            del df['index']
            
            clf = xgb.XGBClassifier()
            booster = xgb.Booster()
            booster.load_model('./model/xgb.model')
            clf._Booster = booster
            clf._le = LabelEncoder().fit(y_test)
            
            y_pred = clf.predict(df)
            
            max_2 = []
            max_2.append(list(y_pred).index(max(y_pred)))
            y_pred[max_2[0]] = 0
            max_2.append(list(y_pred).index(max(y_pred)))
            
            articles = RatingsSmall.objects.filter(userid=userid2, movieid=df['movieid'][max_2[0]]) | RatingsSmall.objects.filter(userid=userid2, movieid=df['movieid'][max_2[1]])
            return render(request, "info.html", {'contacts': articles}) #必须用这个return\
            #return HttpResponseRedirect("info.html",{'articles': articles})
            #return y_pred
            #return JsonResponse({"USER": userid2, "first_movie": df['movieid'][max_2[0]], "second_movie": df['movieid'][max_2[1]]})
            #return JsonResponse({"status": 0})
        except:
            return JsonResponse({"status": 1})