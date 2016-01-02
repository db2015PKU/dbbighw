#encoding:utf8
#import MySQLdb
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
import sqlite3
import json

# Create your views here.

#方便使用with语句以免除冗余的创建关闭连接语句
class getConCur:

    def __enter__(self):
        self._con = sqlite3.connect("mycinema.db")
        self._cur = self._con.cursor()
        return (self._con,self._cur)

    def __exit__(self,type, value, trace):
        self._cur.close()
        self._con.close()
        

def sqlRead(sql_str):
    with getConCur() as (con,cur):
        cur.execute(sql_str)
        values = cur.fetchall()
    return values

def sqlWrite(sql_str):
    try:
        with getConCur() as (con,cur):
            cur.execute(sql_str)
            con.commit()
        return True
    except Exception as e:
        with open('log.txt','w') as f:
            f.write(str(e))
            print (e)
        return False

def login(request):#拿到正确返回值后前端似乎应该自己再重定向到首页？
    if request.method == 'GET':
        if not request.session.has_key('logined') or not request.session['logined']:
            return render(request, 'login.html')
        else:
            return HttpResponseRedirect('/')
    elif request.method == 'POST':
        user_email=request.POST['user_email']
        user_password=request.POST['user_password']
        sql="select user_email,user_password,user_id from userAccount where user_email = '%s'" % user_email
        print sql
        dbRes=sqlRead(sql)
        if dbRes:
            if dbRes[0][1]==user_password:
                request.session['logined']=True
                request.session['user_id']=dbRes[0][2]
                request.session['user_email']=dbRes[0][0]
                
            else:
                request.session['logined']=False
        else:
            request.session['logined']=False
        print dbRes
        return HttpResponseRedirect("/")

def sign(request):#前端的值似乎没传好，user_email这个字段获取不到
    if request.method == 'GET':
        if not request.session.has_key('logined') or not request.session['logined']:
             return render(request, 'signup.html')
        else:
            return HttpResponseRedirect('/')
    elif request.method == 'POST':
        user_email=request.POST['user_email']
        user_password=request.POST['user_password']
        sql="insert into userAccount (user_email,user_password,user_permissions) values ('%s','%s','normal')" % (user_email,user_password)
        if sqlWrite(sql):
            request.session['logined']=True
            sql="select user_id,user_email from userAccount where user_email = '%s'" % user_email
            dbRes=sqlRead(sql)
            request.session['user_id']=dbRes[0][0]
            request.session['user_email']=dbRes[0][1]
          
        else:
            request.session['logined']=False
         
        
        return HttpResponseRedirect("/")
        
def exit(request):#tested
    del request.session['logined']
    return render(request, 'signup.html')

def user_ticket_history(request):#complete但没有数据可以测试
    sql='''select cinema_name,movie_name,room_no,sellTickets.show_date,sellTickets.show_time,sellTickets.cinema_id from (sellTickets left outer join cinema on sellTickets.cinema_id = cinema.cinema_id) left outer join movie on sellTickets.movie_id = movie.movie_id where user_id = %s''' % request.session['user_id']
    dbRes=sqlRead(sql)
    data=[
        {
            "cinema_name": x[0],
            "movie_name": x[1],
            "room_no":x[2],
            "show_date":x[3],
            "show_time":x[4],
            "url":'/cinema/'+str(x[5])
            
        }
        for x in dbRes
    ]
    for row in data:
        sql='''select seatx,seaty from sellTickets where room_no = %s and show_date = '%s' and show_time = '%s' and user_id = %s''' % (row['room_no'],row['show_date'],row['show_time'],request.session['user_id'])
        dbRes=sqlRead(sql)
        row['seats']=[{'x':x[0],'y':x[1]} for x in dbRes]
    '''返回示例
    data = [
        {
            "cinema_name": "影院1",
            "movie_name": "电影名",
            "room_no": 1,
            "show_date":'2015-10-10',
            "show_time":'20:00:00',
            "seats": [
                {
                    'x': 1,
                    'y': 2
                },
                {
                    'x': 1,
                    'y': 3
                }
            ]
        },
        {
            'cinema_name': '影院1',
            'movie_name': '电影名',
            'room_no': 1,
            "show_date":'2015-10-10',
            "show_time":'20:00:00',
            'seats': [
                {
                    'x': 1,
                    'y': 2
                },
                {
                    'x': 1,
                    'y': 3
                }
            ]
        }

    ]'''
    # return HttpResponse(json.dumps(result), content_type="application/json")
    return render(request, 'history.html', {'data': data, 'user_email': request.session['user_email']})



District_dict={
    '1':"东城区",
    '2':"西城区",
    '3':"朝阳区",
    '4':"海淀区",
    '5':"丰台区",
    '6':"石景山区",
    '7':"门头沟区",
    '8':"房山区",
    '9':"大兴区",
    '10':"通州区",
    '11':"顺义区",
    '12':"昌平区",
    '13':"平谷区",
    '14':"怀柔区",
    '15':"密云县",
    '16':"延庆县",
    }
def search_cinema_by_district(request):#3种按行政区搜索电影院
    '''
    "district_no":"行政区编号,0表示全部，1~16为北京的16个行政区",
    "method": "排序方法，0为按综合排序（评分），且不返回空位数；1为按照空位，即 method为0时按综合排序给出普通搜索的结果，如果method为1  再根据abovemean是0还是1定",
    "abovemean":"在method为1的情况下，0返回空位最高的，1返回空位高于平均"
    '''
    district_no=request.GET['district_no']
    district=District_dict[district_no]

    method=int(request.GET['method'])
   
    if method==0:#tested
        sql="select cinema_name,district,road,busStation,businessHoursBegin,businessHoursEnd,estimate,cinema_id  from cinema where district = '%s' order by estimate" % district
        dbRes=sqlRead(sql)
        result={"data":[
        {
            "cinema_name":x[0],
            "district":x[1],
            "road":x[2],
            "busStation":x[3],
            "businessHoursBegin":x[4],
            "businessHoursEnd":x[5],
            "estimate":x[6],
            "url": "/cinema/"+str(x[7]),
        } 
            for x in dbRes]
        }


        '''result={
        "data":[
        {
            "cinema_name":"影院名1",
            "district": "行政区2",
            "road": "海淀南路",
            "busStation": "所在公交站",
            "estimate":1.5,
            "businessHoursBegin":"10:00",
            "businessHoursEnd":"12:00"

        },
        {
            "cinema_name":"影院名2",
            "district": "行政区2",
            "road": "海淀南路",
            "busStation": "所在公交站",
            "estimate":1.5,
            "businessHoursBegin":"10:00",
            "businessHoursEnd":"12:00"

        }
        ]
    }'''
    else:#买票数据部分因为没有数据无法测试，其他测试正常
        #空位计算方式：先看某个电影院放映的电影场次有哪些，每个场次在哪个放映厅放映，根据放映厅最大座位数与现已出售票的数目只差确定空位数
        sql="select cinema_name,district,road,busStation,businessHoursBegin,businessHoursEnd,estimate,cinema_id from cinema where district = '%s'" % district
        dbRes=sqlRead(sql)
        result={
        "data":[
            {
                "cinema_name":x[0],
                "district":x[1],
                "road":x[2],
                "busStation":x[3],
                "businessHoursBegin":x[4],
                "businessHoursEnd":x[5],
                "estimate":x[6],
                "cinema_id":x[7],
                "url": "/cinema/"+str(x[7]),
            }
            for x in dbRes]
        }
        for row in result['data']:
            sql='''select room_no,show_date,show_time from movieShow where cinema_id = %d''' % row['cinema_id']
            dbRes=sqlRead(sql)
            availableTotal=0
            for subrow in dbRes:
                room_no=subrow[0]
                show_date=subrow[1]
                show_time=subrow[2]
                sql='''select seatx_max,seaty_max from room where room_no = %s''' % room_no
                roomRes=sqlRead(sql)
                availableTotal+=int(roomRes[0][0])*int(roomRes[0][1])
                sql='''select count(*) from sellTickets where room_no = %s and show_date = '%s' and show_time = '%s' ''' % (room_no,show_date,show_time)
                countRes=sqlRead(sql)
                availableTotal-=countRes[0][0]
            row["seatsAvailTotal"]=availableTotal
        result['data']=sorted(result['data'],lambda x,y:cmp(x['seatsAvailTotal'],y['seatsAvailTotal']),reverse=True)
        if method==1:#tested
            result['data']=[result['data'][0]]
            '''result={
        "data":[
            {
                "cinema_name":"影院名",
                "district":"行政区2",
                "road":"所在街道",
                "busStation":"所在公交车站",
                "businessHoursBegin":"10:00",
                "businessHoursEnd":"12:00",
                "seatsAvailTotal":20
            }
        ]
    }'''
        elif method==2:#tested
            mean=sum(map(lambda x:x['seatsAvailTotal'],result['data']))/float(len(result['data']))
            result['data']=[x for x in result['data'] if x['seatsAvailTotal']>=mean]
            result['mean']=mean
            '''result={
        "data":[
            {
                "cinema_name":"影院名",
                "district":"行政区2",
                "road":"所在街道",
                "busStation":"所在公交车站",
                "businessHoursBegin":"10:00",
                "businessHoursEnd":"12:00",
                "seatsAvailTotal":20
            }
        ],
        "mean":53
    }'''
        
    
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_movie(request):#返回的字典数值tested，render未测试
    movie_name=request.GET['filmname']
    sql="select cinema.cinema_name,cinema.cinema_id,cinema.district,cinema.road,cinema.busStation,cinema.estimate,cinema.businessHoursBegin,cinema.businessHoursEnd,movieShow.room_no,movieShow.show_date,movieShow.show_time from (movieShow inner join movie on movieShow.movie_id = movie.movie_id) inner join cinema on movieShow.cinema_id = cinema.cinema_id  where movie.movie_name like '%"+movie_name+"%' order by cinema.estimate"
    dbRes=sqlRead(sql)
    data = [
    {
        "cinema_name":x[0],
        "url": "/cinema/"+str(x[1]),
        "district":x[2],
        "road":x[3],
        "busStation":x[4],
        "estimate":x[5],
        "businessHoursBegin":x[6],
        "businessHoursEnd":x[7],
        "room_no":x[8],
        "show_date":x[9],
        "show_time":x[10]

    } for x in dbRes
    ]
    for row in data:
        sql='''select seatx_max,seaty_max from room where room_no = %s''' % row['room_no']
        dbRes=sqlRead(sql)
        availableTotal=int(dbRes[0][0])*int(dbRes[0][1])
        sql='''select count(*) from sellTickets where room_no = %s and show_date = '%s' and show_time = '%s' ''' % (row['room_no'],row['show_date'],row['show_time'])
        countRes=sqlRead(sql)
        availableTotal-=countRes[0][0]
        row["availableTotal"]=availableTotal
    data=sorted(data,lambda x,y:cmp(x['estimate']*10+x['availableTotal'],y['estimate']*10+y['availableTotal']),reverse=True)#综合排名依据：x['estimate']*10+x['availableTotal']




    #return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'search.html', {'data':data, 'movie_name':movie_name, 'user_email': request.session['user_email']})

def search_movie_total(request): #tested
#找出今日所有电影院上映的不同电影，显示每部电影的上座率,影票的最高、最低价格。 
    #等空位和票价信息增加
    sql='''select distinct movieShow.movie_id,movie_name from movieShow left outer join movie on movieShow.movie_id = movie.movie_id'''
    dbRes=sqlRead(sql)
    data=[
        {
            "movie_id":x[0],
            "movie_name":x[1],
            
        }
        for x in dbRes
    ]
    for row in data:
        sql='''select max(price),min(price) from movieShow where movie_id = %s ''' % row['movie_id']
        dbRes=sqlRead(sql)
        row['max_price']=dbRes[0][0]
        row['min_price']=dbRes[0][1]
        sql='''select room_no,show_date,show_time from movieShow where movie_id = %s ''' % row['movie_id']
        total=0
        sold=0
        Res=sqlRead(sql)
        for subrow in Res:
            room_no=subrow[0]
            show_date=subrow[1]
            show_time=subrow[2]
            sql='''select seatx_max,seaty_max from room where room_no = %s''' % room_no
            roomRes=sqlRead(sql)
            total+=int(roomRes[0][0])*int(roomRes[0][1])
            sql='''select count(*) from sellTickets where room_no = %s and show_date = '%s' and show_time = '%s' ''' % (room_no,show_date,show_time)
            soldRes=sqlRead(sql)
            sold+=soldRes[0][0]
        row['sold_rate']=float(sold)/total




    #data = [{"movie_name":"电影名1","sold_rate":0.55,"max_price":100,"min_price":50},{"movie_name":"电影名2","sold_rate":0.7,"max_price":90,"min_price":40}]
    return render(request, 'hottoday.html', {'data': data, 'datastr': str(data), 'user_email': request.session['user_email']})

def ticket(request):#complete but without test
    user_id=request.session['user_id']
    #with open('POST.txt','w') as f:
        #f.write(str(request.POST['cinema_id']))
    cinema_id=request.GET['cinema_id']
    movie_id=request.GET['movie_id']
    show_date=request.GET['show_date']
    show_time=request.GET['show_time']
    room_no=request.GET['room_no']
    seatx=request.GET['seatx']
    seaty=request.GET['seaty']
    price=request.GET['price']
    sql='''insert into sellTickets (user_id,cinema_id,movie_id,show_date,show_time,room_no,seatx,seaty,price) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (user_id,cinema_id,movie_id,show_date,show_time,room_no,seatx,seaty,price)
    with open('POST.txt','w') as f:
        f.write(sql)
    if(sqlWrite(sql)):
        result={
        "info":"success",
        "seatx":seatx,
        "seaty":seaty
    }
    else:
        result={
        "info":"fail",
        "seatx":seatx,
        "seaty":seaty
        }


    
    return HttpResponse(json.dumps(result), content_type="application/json")


def index(request):
    if not request.session.has_key('logined') or not request.session['logined']:
        return render(request, 'signup.html')
    return render(request, 'index.html', {'user_email': request.session['user_email']})

def cinema(request,cinema_id):#tested
    if not request.session.has_key('logined') or not request.session['logined']:
        return render(request, 'signup.html')
    url = '/cinema_xml/'+cinema_id
    return render(request, 'cinema.html', {'url': url, 'user_email': request.session['user_email']})

def hall(request,room_no,show_date,show_time):#tested
    if not request.session.has_key('logined') or not request.session['logined']:
        return render(request, 'signup.html')
    # 座位映射表，a表示available座位，u表示unavailable座位
    sql='''select seatx_max,seaty_max from room where room_no = %s''' % room_no
    dbRes=sqlRead(sql)
    maxX=dbRes[0][0]
    maxY=dbRes[0][1]
    data=[['a' for col in range(maxX)] for row in range(maxY)]
    sql='''select seaty,seatx from sellTickets where room_no = %s and show_date = '%s' and show_time = '%s' ''' % (room_no,show_date,show_time)
    
    dbRes=sqlRead(sql)
    for row in dbRes:
        data[row[0]-1][row[1]-1]='u'
    

    #最终data形式 ： ['aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa', 'aaaaaaaaaa']
    for index,i in enumerate(data):
        data[index]=''.join(i)
    with open('testlog.txt','w') as f:
        f.write(str(data))

    sql='''select price,cinema_id,movie_id from movieShow where room_no = %s and show_date = '%s' and show_time = '%s' ''' % (room_no,show_date,show_time)
    dbRes=sqlRead(sql)
    price = dbRes[0][0] #单价
    return render(request, 'hall.html', {'seatmap': data, 'price': price, 'user_email': request.session['user_email'],'cinema_id':dbRes[0][1],'movie_id':dbRes[0][2],'show_date':show_date,'show_time':show_time,'room_no':room_no})

def cinema_xml(request,cinema_id):#tested
    if not request.session.has_key('logined') or not request.session['logined']:
        return render(request, 'signup.html')
    # XML中Movie里添加放映厅url信息
    #cinema_id="1"
    sql='''select cinema_name,district,road,busStation,phone,businessHoursBegin,businessHoursEnd,estimate from cinema where cinema_id = %d''' % int(cinema_id)
    dbRes=sqlRead(sql)
    data = {
    "cinema":{
        "cinema_name":dbRes[0][0],
        "district":dbRes[0][1],
        "road":dbRes[0][2],
        "busStation":dbRes[0][3],
        "phone":dbRes[0][4],
        "businessHours":dbRes[0][5]+'-'+dbRes[0][6],
        "estimate":dbRes[0][7]
        }
    }
    
    sql='''select movie_name,movieShow.show_date,movieShow.show_time,runtime,director,actors,movie_type,movie_language,movieShow.room_no,movieShow.price from (movie left outer join movieShow on movie.movie_id = movieShow.movie_id)  where cinema_id = %d''' % int(cinema_id)
    dbRes=sqlRead(sql)
    data['movies']=[
        {
            "Name":x[0],
            "Date":x[1],
            "Time":x[2],
            "Runtime":x[3],
            "Director":x[4],
            "Actors":x[5],
            "Type":x[6],
            "Language":x[7],
            "Room":x[8],
            "RoomUrl":'/'.join(["/hall",str(x[8]),str(x[1]),str(x[2])]),#,str(x[2])]
            "Price":x[9]

        }
        for x in dbRes
    ]


    return render(request,'cinema_info.xml',data,content_type="application/xml")  



def create_db(request):
    cx = sqlite3.connect("mycinema.db")
    cu=cx.cursor()
    sql_str='''


drop table if exists cinema;
CREATE TABLE cinema (
    cinema_id INT(10) NOT NULL,
    cinema_name VARCHAR(40) NOT NULL,
    district VARCHAR(20) NOT NULL,
    road VARCHAR(20) NOT NULL,
    busStation VARCHAR(20) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    businessHoursBegin TIME NOT NULL,
    businessHoursEnd TIME NOT NULL,
    estimate NUMERIC(2 , 1 ) CHECK (estimate > 0 AND estimate < 10),
    PRIMARY KEY (cinema_id)
);

insert into cinema values ('1', '美嘉欢乐影城', '海淀区', '中关村大街', '中关村北站', '36370000', '08:30', '23:30', '7.0');
insert into cinema values ('2', '金逸国际影城', '海淀区', '中关村大街', '中关村北站', '36370001', '08:30', '23:30', '7.1');
insert into cinema values ('3', '工人文化宫', '石景山区', '万柳北街', '华府站', '36370002', '08:30', '23:30', '7.2');
insert into cinema values ('4', 'UME国际影城', '海淀区', '科学院南路', '双安站', '36370003', '08:30', '23:30', '7.3');
insert into cinema values ('5', '星美影城', '海淀区', '远大路', '金源站', '36370004', '08:30', '23:30', '7.4');
insert into cinema values ('6', '五道口影院', '海淀区', '成府路', '五道口站', '36370005', '08:30', '23:30', '7.5');
insert into cinema values ('7', '新华影城', '海淀区', '成府路', '大钟寺站', '36370006', '08:30', '23:30', '7.6');
insert into cinema values ('8', '橙天嘉禾影城', '海淀区', '农大南路', '农大站', '36370007', '08:30', '23:30', '7.7');
insert into cinema values ('9', '嘉华影城', '海淀区', '学清路', '圣熙站', '36370008', '08:30', '23:30', '7.8');
insert into cinema values ('10', '17.5影城', '海淀区', '四道口路', '四道口站', '36370009', '08:30', '23:30', '7.9');
insert into cinema values ('11', '四季青影城', '海淀区', '西四环北路', '四季青桥站', '36370010', '08:30', '23:30', '8.0');
insert into cinema values ('12', '星汇聚影城', '海淀区', '海淀中街', '华润站', '36370011', '08:30', '23:30', '8.1');
insert into cinema values ('13', '万画影城', '海淀区', '西四环北路', '四清站', '36370012', '08:30', '23:30', '8.2');
insert into cinema values ('14', '天幕影城', '海淀区', '北三环中路', '中视站', '36370013', '08:30', '23:30', '8.3');
insert into cinema values ('15', '天宝国际影城', '朝阳区', '祁连街', '健翔站', '36370014', '08:30', '23:30', '8.4');
insert into cinema values ('16', '中影国际影城', '海淀区', '外大街', '新街口站', '36370015', '09:30', '23:00', '8.5');
insert into cinema values ('17', '大地影院', '海淀区', '越秀路', '同厦站', '36370016', '09:30', '23:00', '8.6');

drop table if exists room;
CREATE TABLE room (
    room_no INT(10) NOT NULL,
    seatx_max INT(10) NOT NULL,
    seaty_max INT(10) NOT NULL,
    PRIMARY KEY (room_no)
);

insert into room values ('1', '10', '10');
insert into room values ('2', '10', '10');
insert into room values ('3', '10', '10');
insert into room values ('4', '10', '10');
insert into room values ('5', '10', '10');
insert into room values ('6', '10', '10');
insert into room values ('7', '10', '10');
insert into room values ('8', '10', '10');
insert into room values ('9', '10', '10');
insert into room values ('10', '10', '10');
insert into room values ('11', '10', '10');
insert into room values ('12', '10', '10');
insert into room values ('13', '10', '10');
insert into room values ('14', '10', '10');
insert into room values ('15', '10', '10');
insert into room values ('16', '10', '10');
insert into room values ('17', '10', '10');
insert into room values ('18', '10', '10');
insert into room values ('19', '10', '10');
insert into room values ('20', '10', '10');
insert into room values ('21', '10', '10');
insert into room values ('22', '10', '10');
insert into room values ('23', '10', '10');
insert into room values ('24', '10', '10');
insert into room values ('25', '10', '10');
insert into room values ('26', '10', '10');
insert into room values ('27', '10', '10');
insert into room values ('28', '10', '10');
insert into room values ('29', '10', '10');
insert into room values ('30', '10', '10');
insert into room values ('31', '10', '10');
insert into room values ('32', '10', '10');
insert into room values ('33', '10', '10');
insert into room values ('34', '10', '10');
insert into room values ('35', '10', '10');
insert into room values ('36', '10', '10');
insert into room values ('37', '10', '10');
insert into room values ('38', '10', '10');
insert into room values ('39', '10', '10');
insert into room values ('40', '10', '10');
insert into room values ('41', '10', '10');
insert into room values ('42', '10', '10');
insert into room values ('43', '10', '10');
insert into room values ('44', '10', '10');
insert into room values ('45', '10', '10');
insert into room values ('46', '10', '10');
insert into room values ('47', '10', '10');
insert into room values ('48', '10', '10');
insert into room values ('49', '10', '10');
insert into room values ('50', '10', '10');
insert into room values ('51', '10', '10');
insert into room values ('52', '10', '10');
insert into room values ('53', '10', '10');
insert into room values ('54', '10', '10');
insert into room values ('55', '10', '10');
insert into room values ('56', '10', '10');
insert into room values ('57', '10', '10');
insert into room values ('58', '10', '10');
insert into room values ('59', '10', '10');
insert into room values ('60', '10', '10');
insert into room values ('61', '10', '10');
insert into room values ('62', '10', '10');
insert into room values ('63', '10', '10');
insert into room values ('64', '10', '10');
insert into room values ('65', '10', '10');
insert into room values ('66', '10', '10');
insert into room values ('67', '10', '10');
insert into room values ('68', '10', '10');
insert into room values ('69', '10', '10');
insert into room values ('70', '10', '10');
insert into room values ('71', '10', '10');
insert into room values ('72', '10', '10');
insert into room values ('73', '10', '10');
insert into room values ('74', '10', '10');
insert into room values ('75', '10', '10');
insert into room values ('76', '10', '10');
insert into room values ('77', '10', '10');
insert into room values ('78', '10', '10');
insert into room values ('79', '10', '10');
insert into room values ('80', '10', '10');
insert into room values ('81', '10', '10');
insert into room values ('82', '10', '10');
insert into room values ('83', '10', '10');
insert into room values ('84', '10', '10');
insert into room values ('85', '10', '10');
insert into room values ('86', '10', '10');
insert into room values ('87', '10', '10');
insert into room values ('88', '10', '10');
insert into room values ('89', '10', '10');
insert into room values ('90', '10', '10');
insert into room values ('91', '10', '10');
insert into room values ('92', '10', '10');
insert into room values ('93', '10', '10');
insert into room values ('94', '10', '10');
insert into room values ('95', '10', '10');
insert into room values ('96', '10', '10');
insert into room values ('97', '10', '10');
insert into room values ('98', '10', '10');
insert into room values ('99', '10', '10');
insert into room values ('100', '10', '10');


drop table if exists room_of_cinema;
CREATE TABLE room_of_cinema (
    cinema_id int(10) NOT NULL,
    room_no INT(10) NOT NULL,
    PRIMARY KEY (cinema_id , room_no),
    CONSTRAINT cinema_id1 FOREIGN KEY (cinema_id)
        REFERENCES cinema (cinema_id)
        ON DELETE CASCADE,
    CONSTRAINT room_no1 FOREIGN KEY (room_no)
        REFERENCES room (room_no)
        ON DELETE CASCADE
);

insert into room_of_cinema values ('1', '1');
insert into room_of_cinema values ('1', '2');
insert into room_of_cinema values ('1', '3');
insert into room_of_cinema values ('1', '4');
insert into room_of_cinema values ('1', '5');
insert into room_of_cinema values ('2', '6');
insert into room_of_cinema values ('2', '7');
insert into room_of_cinema values ('2', '8');
insert into room_of_cinema values ('2', '9');
insert into room_of_cinema values ('2', '10');
insert into room_of_cinema values ('3', '11');
insert into room_of_cinema values ('3', '12');
insert into room_of_cinema values ('3', '13');
insert into room_of_cinema values ('3', '14');
insert into room_of_cinema values ('3', '15');
insert into room_of_cinema values ('4', '16');
insert into room_of_cinema values ('4', '17');
insert into room_of_cinema values ('4', '18');
insert into room_of_cinema values ('4', '19');
insert into room_of_cinema values ('4', '20');
insert into room_of_cinema values ('5', '21');
insert into room_of_cinema values ('5', '22');
insert into room_of_cinema values ('5', '23');
insert into room_of_cinema values ('5', '24');
insert into room_of_cinema values ('5', '25');

 
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

insert into movie values ('1', '万万没想到', '2015-12-18', '12:00:00', '98', '叫兽易小星', '白客/杨子珊/陈柏霖/马天宇', 'comedy', 'Chinese', '48');
insert into movie values ('2', '寻龙诀', '2015-12-18', '12:00:00', '125', '乌尔善', '陈坤/黄渤/舒淇/马杨颖', 'action', 'Chinese', '56');
insert into movie values ('3', '恶棍天使', '2015-12-24', '12:00:00', '124', '邓超', '邓超/孙俪', 'comedy', 'Chinese', '42.9');
insert into movie values ('4', '老炮儿', '2015-12-24', '12:00:00', '137', '冯小刚', '张涵予/李易峰/吴亦凡', 'action', 'Chinese', '72');
insert into movie values ('5', '极盗者', '2015-12-04', '12:00:00', '113', '埃里克松·科尔', '卢克·布雷西/泰丽莎·帕尔默', 'action', 'English', '52');
insert into movie values ('6', '师父', '2015-12-10', '12:00:00', '109', '徐皓峰', '廖凡/宋佳/蒋雯丽', 'action', 'Chinese', '48');
insert into movie values ('7', '海绵宝宝', '2015-12-01', '12:00:00', '92', '保罗·迪比特', '安东尼奥·班德拉斯/汤姆·肯尼', 'comedy', 'English', '48');
insert into movie values ('8', '火星救援', '2015-11-25', '12:00:00', '144', '雷德利·斯科特', '马特·达蒙/杰西卡·查斯坦/克里斯丁·韦格', 'action', 'English', '48');
insert into movie values ('9', '唐人街探案', '2015-12-31', '12:00:00', '135', '陈思诚', '王宝强/陈思诚/佟丽娅', 'comedy', 'Chinese', '48');
insert into movie values ('10', '杜拉拉追婚记', '2015-12-04', '12:00:00', '101', '安竹间', '周渝民/林依晨/陈柏霖', 'comedy', 'Chinese', '48');



drop table if exists userAccount;
CREATE TABLE userAccount (
    user_id INTEGER PRIMARY KEY,
    user_email VARCHAR(40) NOT NULL,
    user_name VARCHAR(40) NOT NULL default '测试用户',
    user_password VARCHAR(30) NOT NULL,
    user_phone VARCHAR(20) NOT NULL default '123',
    user_permissions VARCHAR(15) CHECK (user_permissions IN ('admin' , 'normal'))
   
);





drop table if exists movieShow;
CREATE TABLE movieShow (
    cinema_id INT(10) NOT NULL,
    movie_id INT(30) NOT NULL,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    room_no INT(10) NOT NULL,
    price NUMERIC(4 , 2 ) NOT NULL,
    PRIMARY KEY (cinema_id , movie_id , show_date , show_time , room_no),
    CONSTRAINT cinema_id2 FOREIGN KEY (cinema_id)
        REFERENCES cinema (cinema_id),
    CONSTRAINT movie_id2 FOREIGN KEY (movie_id)
        REFERENCES movie (movie_id),
    CONSTRAINT roon_no2 FOREIGN KEY (room_no)
        REFERENCES room (room_no)
);

insert into movieShow values ('1', '1', '2015-12-20', '20:00:00', '1','48');
insert into movieShow values ('1', '2', '2015-12-20', '20:00:00', '2','56');
insert into movieShow values ('2', '1', '2015-12-20', '20:00:00', '6','48');
insert into movieShow values ('2', '2', '2015-12-20', '20:00:00', '7','56');
insert into movieShow values ('3', '1', '2015-12-20', '20:00:00', '11','48');
insert into movieShow values ('3', '2', '2015-12-20', '20:00:00', '12','56');
insert into movieShow values ('4', '1', '2015-12-20', '20:00:00', '16','48');
insert into movieShow values ('4', '2', '2015-12-20', '20:00:00', '17','56');
insert into movieShow values ('5', '1', '2015-12-20', '20:00:00', '21','48');
insert into movieShow values ('5', '2', '2015-12-20', '20:00:00', '22','56');


 drop table if exists sellTickets;
CREATE TABLE sellTickets (
    ticket_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    cinema_id INT(10) not NULL,
    movie_id INT(30) NOT NULL,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    room_no INT(10) NOT NULL,
    seatx INT(10) NOT NULL,
    seaty INT(10) NOT NULL,
    price NUMERIC(4 , 2 ) NOT NULL,
    
    
    unique(seatx,seaty,show_date,show_time,room_no)
);
drop trigger if exists seat_check1;
drop trigger if exists seat_check2;
create trigger seat_check1 before insert on sellTickets
    for each row
    begin
    select raise(rollback, '选座失败')
    where exists(select cinema_id, movie_id, show_date, show_time, room_no
                 from sellTickets
                 where cinema_id = new.cinema_id and movie_id = new.movie_id and show_date = new.show_date and show_time = new.show_time and room_no = new.room_no)
    and new.seatx > 2
    and exists(select seatx, seaty
         from sellTickets
         where seatx = new.seatx - 2 and seaty = new.seaty limit 1)
    and not exists(select seatx, seaty
         from sellTickets
         where seatx = new.seatx - 1 and seaty = new.seaty limit 1);
    
    end;
create trigger seat_check2 before insert on sellTickets
    for each row
    begin
    select raise(rollback, '选座失败')
    where exists(select cinema_id, movie_id, show_date, show_time, room_no
                 from sellTickets
                 where cinema_id = new.cinema_id and movie_id = new.movie_id and show_date = new.show_date and show_time = new.show_time and room_no = new.room_no)
    and new.seatx < 9
    and exists(select seatx, seaty
         from sellTickets
         where seatx = new.seatx + 2 and seaty = new.seaty)
    and not exists(select seatx, seaty
         from sellTickets
         where seatx = new.seatx + 1 and seaty = new.seaty);
    
    end;


    
        
 


'''
    cu.executescript(sql_str)
    cx.commit()
    cu.close()
    cx.close()
    result={'info':'done!'}
    return HttpResponse(json.dumps(result), content_type="application/json")