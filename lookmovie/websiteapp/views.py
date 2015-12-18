#encoding:utf8
#import MySQLdb
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
import sqlite3
import json

# Create your views here.


def login(request):
    #user_name=request.GET['user_name']
    #user_password=request.GET['user_password']
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        result={'logined':True,'info':'success','user_permissions':'normal','user_id':'1c80'}
        return HttpResponse(json.dumps(result), content_type="application/json")

def sign(request):
    #user_name=request.GET['user_name']
    #user_password=request.GET['user_password']
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        result={'signed':True,'info':'success','user_id':'1c80'}
        return HttpResponse(json.dumps(result), content_type="application/json")

def index(request):
    return render(request, 'index.html')
    
def search_cinema_by_str(request):
    #search_str=request.GET['search_str']
    result={"data":[{"cinema_name":"影院名1"},
    {"cinema_name":"影院名2"}]}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_district(request):
    #district_no=request.GET['district_no']
    method=int(request.GET['method'])
    abovemean=int(request.GET['abovemean'])
    if method==0:
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
    elif method==1 and abovemean==0:
        result={
        "data":[
            {
                "cinema_name":"影院名",
                "address":"地址",
                "businessHoursBegin":"10:00",
                "businessHoursEnd":"12:00",
                "seatsAvailTotal":20
            }
        ]
    }
    elif method==1 and abovemean==1:
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


def hottoday(request):
    return render(request, 'hottoday.html')

def cinema(request):
    return render(request, 'cinema.html')

def hall(request):
    return render(request, hall)


def create_db(request):
    cx = sqlite3.connect("mycinema.db")
    cu=cx.cursor()
    sql_str='''
drop table if exists cinema;
CREATE TABLE cinema (
cinema_name VARCHAR(40) NOT NULL,
district VARCHAR(20) NOT NULL,
road VARCHAR(20) NOT NULL,
busStation VARCHAR(20) NOT NULL,
phone VARCHAR(50) NOT NULL,
businessHoursBegin TIME NOT NULL,
businessHoursEnd TIME NOT NULL,
estimate NUMERIC(2 , 1 ) CHECK (estimate > 0 AND estimate < 10),
PRIMARY KEY (cinema_name)
);
drop table if exists room;
CREATE TABLE room (
room_no INT(10) NOT NULL,
seatx_max INT(10) NOT NULL,
seaty_max INT(10) NOT NULL,
PRIMARY KEY (room_no)
);
drop table if exists room_of_cinema;
CREATE TABLE room_of_cinema (
cinema_name VARCHAR(40) NOT NULL,
room_no INT(10) NOT NULL,
PRIMARY KEY (cinema_name , room_no),
constraint cinema_name1 FOREIGN KEY (cinema_name)
REFERENCES cinema (cinema_name)
on delete cascade,
constraint room_no1 foreign key (room_no)
REFERENCES room(room_no)
on delete cascade
);
drop table if exists movie;
CREATE TABLE movie (
movie_id INT(30) NOT NULL,
movie_name VARCHAR(40) NOT NULL,
show_date DATE NOT NULL,
show_time TIME NOT NULL,
runtime INT(20) NOT NULL,
director VARCHAR(40) NOT NULL,
actors VARCHAR(40) NOT NULL,
movie_type VARCHAR(40) CHECK (movie_type IN ('literary' , 'horror',
'action',
'comedy',
'pornographic',
'thriller')),
movie_language VARCHAR(20) CHECK (movie_language IN ('Chinese' , 'English')),
price NUMERIC(4 , 2 ) NOT NULL,
PRIMARY KEY (movie_id)
);
drop table if exists movies_of_cinema;
create table movies_of_cinema
(
cinema_name VARCHAR(40) NOT NULL,
movie_id INT(30) NOT NULL,
primary key(cinema_name, movie_id)
);
drop table if exists userAccount;
CREATE TABLE userAccount (
user_email VARCHAR(40) NOT NULL,
user_name VARCHAR(40) NOT NULL,
user_password VARCHAR(30) NOT NULL,
user_phone VARCHAR(20) NOT NULL,
user_permissions VARCHAR(15) CHECK (user_permissions IN ('admin' , 'normal')),
PRIMARY KEY (user_email)
);
drop table if exists ticket;
CREATE TABLE ticket (
ticket_id INT(30) NOT NULL,
movie_id INT(30) NOT NULL,
cinema_name VARCHAR(40) NOT NULL,
show_date DATE NOT NULL,
show_time TIME NOT NULL,
room_no INT(10) NOT NULL,
seatx INT(10) NOT NULL,
seaty INT(10) NOT NULL,
PRIMARY KEY (ticket_id),
constraint movie_id1 FOREIGN KEY (movie_id)
REFERENCES movie(movie_id),
FOREIGN KEY (cinema_name , room_no)
REFERENCES room_of_cinema(cinema_name, room_no)
);
drop table if exists movieShow;
CREATE TABLE movieShow (
cinema_name VARCHAR(40) NOT NULL,
movie_id INT(30) NOT NULL,
show_date DATE NOT NULL,
show_time TIME NOT NULL,
room_no INT(10) NOT NULL,
price NUMERIC(4 , 2 ) NOT NULL,
PRIMARY KEY (cinema_name , movie_id , show_date , show_time , room_no),
constraint cinema_name2 FOREIGN KEY (cinema_name)
REFERENCES cinema(cinema_name),
constraint movie_id2 FOREIGN KEY (movie_id)
REFERENCES movie(movie_id),
constraint roon_no2 FOREIGN KEY (room_no)
REFERENCES room(room_no)
);
drop table if exists sellTickets;
CREATE TABLE sellTickets (
ticket_id INT(30) NOT NULL,
cinema_name VARCHAR(40) NOT NULL,
movie_id INT(30) NOT NULL,
show_date DATE NOT NULL,
show_time TIME NOT NULL,
room_no INT(10) NOT NULL,
seatx INT(10) NOT NULL,
seaty INT(10) NOT NULL,
PRIMARY KEY (ticket_id , cinema_name , movie_id)
);'''
    cu.executescript(sql_str)
    cx.commit()
    cu.close()
    cx.close()
    result={'info':'done!'}
    return HttpResponse(json.dumps(result), content_type="application/json")