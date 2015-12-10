#encoding:utf8
import MySQLdb
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json

# Create your views here.


def login(request):
    #user_name=request.GET['user_name']
    #user_password=request.GET['user_password']
    result={'logined':True,'info':'success','user_permissions':'normal','user_id':'1c80'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def sign(request):
    #user_name=request.GET['user_name']
    #user_password=request.GET['user_password']
    result={'signed':True,'info':'success','user_id':'1c80'}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_str(request):
    #search_str=request.GET['search_str']
    result={"data":[{"cinema_name":"影院名1"},
    {"cinema_name":"影院名2"}]}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_district(request):
    #district=request.GET['district']
    result={
    "data":[
    {
        "cinema_name":"影院名1",
        "address":"地址2",
        "estimate":1.5,
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00"

    },
    {
        "cinema_name":"影院名2",
        "address":"地址2",
        "estimate":1.2,
        "businessHoursBegin":"11:00",
        "businessHoursEnd":"12:00"

    }
    ]
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_movie(request):
    #movie_name=request.GET['movie_name']
    result={
    "data":[
    {
        "cinema_name":"影院名1",
        "address":"地址2",
        "estimate":1.5,
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00",
        "availableTotal":12

    },
    {
        "cinema_name":"影院名2",
        "address":"地址2",
        "estimate":1.2,
        "businessHoursBegin":"11:00",
        "businessHoursEnd":"12:00",
        "availableTotal":15
    }
    ]
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_max_available_seat_by_district(request):
    #distinct=request.GET['distinct']
    result={
        "cinema_name":"影院名",
        "address":"地址",
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00",
        "seatsAvailTotal":20
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_greater_avg_seat_by_district(request):
    #distinct=request.GET['distinct']
    result={
    "data":[
    {
        "cinema_name":"影院名1",
        "address":"地址2",
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00",
        "seatsTotal":12

    },
    {
        "cinema_name":"影院名2",
        "address":"地址2",
        "businessHoursBegin":"11:00",
        "businessHoursEnd":"12:00",
        "seatsTotal":15
    }
    ]
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_movie_total(request):
    result={
    "data":[
       { 
        "movie_name":"电影名1",
        "sold_rate":0.55,
        "max_price":100,
        "min_price":50
        
    },
    { 
        "movie_name":"电影名2",
        "sold_rate":0.7,
        "max_price":90,
        "min_price":40
        
    }
  
    ]   
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def ticket(request):
    #ticket_id=request.GET['ticket_id']
    result={
   "info":"success"
}
    return HttpResponse(json.dumps(result), content_type="application/json")




