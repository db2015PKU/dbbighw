#encoding:utf8
#import MySQLdb
from django.shortcuts import render
from django.shortcuts import render_to_response
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
        return False

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_email="fdffdf@qq.com"#request.POST['user_email']
        user_password="qerere"#request.POST['user_password']
        sql="select user_email,user_password,user_permissions from userAccount where user_email = '%s'" % user_email
        print sql
        dbRes=sqlRead(sql)
        if dbRes:
            if dbRes[0][1]==user_password:
                result={'logined':True,'info':'success'}
                result['user_permissions']=dbRes[0][2]
                print 'success'
            else:
                result={'logined':False,'info':'password_error','user_permissions':'normal'}
                print 'pswd error'
        else:
            result={'logined':False,'info':'no_such_user','user_permissions':'normal'}

        #result={'logined':True,'info':'success','user_permissions':'normal'}
        request.session['logined'] = result['logined']#初始化session
        return HttpResponse(json.dumps(result), content_type="application/json")

def sign(request):
    #user_name=request.GET['user_name']
    #user_password=request.GET['user_password']
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        user_email="fdffdf@qq.com"#request.POST['user_email']
        user_password="qeree"#request.POST['user_password']
        sql="insert into userAccount (user_email,user_password) values (%s,%s)" % (user_email,user_password)
        if sqlWrite(sql):
            result={'signed':True,'info':'success'}
            print 'success'
        else:
            result={'signed':True,'info':'user_email_have_been_used'}
            print 'eamil exist'
        #result={'signed':True,'info':'success'}
        return HttpResponse(json.dumps(result), content_type="application/json")
        
def exit(request):
    del request.session['logined']

def user_ticket_history(request):
    sql='''select '''
    result={
    "data":[
    {"cinema_name":"影院名1","movie_name":"电影名","room_no":"1","room_no":"2"},
    {"cinema_name":"影院名2","movie_name":"电影名","room_no":"4","room_no":"3"}
    ]
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

def index(request):
    return render(request, 'index.html')
    
def search_cinema_by_str(request):#按关键字搜索本地电影院
    search_str=u'美嘉'#request.GET['search_str']
    sql="select cinema_name from cinema where cinema_name like '%"+search_str+"%'"#差空位数
    dbRes=sqlRead(sql)
    result={"data":[{"cinema_name":x[0]} for x in dbRes]}
    #result={"data":[{"cinema_name":"影院名1"},
    #{"cinema_name":"影院名2"}]}
    return HttpResponse(json.dumps(result), content_type="application/json")

District_dict={'0':"海淀区"}
def search_cinema_by_district(request):
    '''
    "district_no":"行政区编号,0表示全部，1~16为北京的16个行政区",
    "method": "排序方法，0为按综合排序（空座位+评分），1为按照空位，即 method为0时按综合排序给出普通搜索的结果，如果method为1  再根据abovemean是0还是1定",
    "abovemean":"在method为1的情况下，0返回空位最高的，1返回空位高于平均"
    '''
    district_no='0'#request.POST['district_no']
    district=District_dict[district_no]

    method=0#int(request.POST['method'])
    abovemean=0#int(request.POST['abovemean'])
    if method==0:
        sql="select cinema_name,district,road,busStation,businessHoursBegin,businessHoursEnd,estimate  from cinema where district = '%s'" % district
        dbRes=sqlRead(sql)
        result={"data":[{"cinema_name":x[0],"district":x[1],"road":x[2],"busStation":x[3],"businessHoursBegin":x[4],"businessHoursBegin":x[5]} for x in dbRes]}
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
    elif method==1 and abovemean==0:
        sql="select cinema_name,district,road,busStation,businessHoursBegin,businessHoursEnd,estimate  from cinema where district = '%s'" % district
        dbRes=sqlRead(sql)#等空位
        result={
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
    }
    elif method==1 and abovemean==1:
        sql="select cinema_name,district,road,busStation,businessHoursBegin,businessHoursEnd,estimate  from cinema where district = '%s'" % district
        dbRes=sqlRead(sql)#等空位
        result={
    "data":[
    {
        "cinema_name":"影院名1",
        "district":"行政区1",
        "road":"所在街道",
        "busStation":"所在公交车站",
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00",
        "seatsTotal":12

    },
    {
        "cinema_name":"影院名2",
        "district":"行政区2",
        "road":"所在街道",
        "busStation":"所在公交车站",
        "businessHoursBegin":"11:00",
        "businessHoursEnd":"12:00",
        "seatsTotal":15
    }
    ]
}
    return HttpResponse(json.dumps(result), content_type="application/json")

def search_cinema_by_movie(request):
    movie_name="万万"#request.POST['movie_name']
    sql="select cinema.cinema_name,cinema.estimate,cinema.district,cinema.road,cinema.busStation,movie.movie_name from (movies_of_cinema inner join movie on movies_of_cinema.movie_id = movie.movie_id) inner join cinema on movies_of_cinema.cinema_name = cinema.cinema_name  where movie.movie_name like '%"+movie_name+"%' order by cinema.estimate"#差空位数
    dbRes=sqlRead(sql)#返回了空
    result={
    "data":[
    {
        "cinema_name":"影院名1",
        "district":"行政区",
        "road":"所在街道",
        "busStation":"所在公交车站",
        "estimate":1.5,
        "businessHoursBegin":"10:00",
        "businessHoursEnd":"12:00",
        "availableTotal":12

    },
    {
        "cinema_name":"影院名2",
        "district":"行政区",
        "road":"所在街道",
        "busStation":"所在公交车站",
        "estimate":1.2,
        "businessHoursBegin":"11:00",
        "businessHoursEnd":"12:00",
        "availableTotal":15
    }
    ]
}
    return HttpResponse(json.dumps(result), content_type="application/json")



def search_movie_total(request):#找出今日所有电影院上映的不同电影，显示每部电影的上座率,影票的最高、最低价格。 

    #等空位和票价信息增加
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
    #等触发器
    result={
        "info":"success"
    }
    return HttpResponse(json.dumps(result), content_type="application/json")


def index(request):
    return render(request, 'index.html')
    
def hottoday(request):
    return render(request, 'hottoday.html')

def cinema(request):
    return render(request, 'cinema.html')

def hall(request):
    return render(request, 'hall.html')

def cinema_xml(request):
    return render(request,'test.xml',content_type="application/xml")  


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

insert into cinema values ('美嘉欢乐影城', '海淀区', '中关村大街', '中关村北站', '36370000', '08:30', '23:30', '7.0');
insert into cinema values ('金逸国际影城', '海淀区', '中关村大街', '中关村北站', '36370001', '08:30', '23:30', '7.1');
insert into cinema values ('工人文化宫', '石景山区', '万柳北街', '华府站', '36370002', '08:30', '23:30', '7.2');
insert into cinema values ('UME国际影城', '海淀区', '科学院南路', '双安站', '36370003', '08:30', '23:30', '7.3');
insert into cinema values ('星美影城', '海淀区', '远大路', '金源站', '36370004', '08:30', '23:30', '7.4');
insert into cinema values ('五道口影院', '海淀区', '成府路', '五道口站', '36370005', '08:30', '23:30', '7.5');
insert into cinema values ('新华影城', '海淀区', '成府路', '大钟寺站', '36370006', '08:30', '23:30', '7.6');
insert into cinema values ('橙天嘉禾影城', '海淀区', '农大南路', '农大站', '36370007', '08:30', '23:30', '7.7');
insert into cinema values ('嘉华影城', '海淀区', '学清路', '圣熙站', '36370008', '08:30', '23:30', '7.8');
insert into cinema values ('17.5影城', '海淀区', '四道口路', '四道口站', '36370009', '08:30', '23:30', '7.9');
insert into cinema values ('四季青影城', '海淀区', '西四环北路', '四季青桥站', '36370010', '08:30', '23:30', '8.0');
insert into cinema values ('星汇聚影城', '海淀区', '海淀中街', '华润站', '36370011', '08:30', '23:30', '8.1');
insert into cinema values ('万画影城', '海淀区', '西四环北路', '四清站', '36370012', '08:30', '23:30', '8.2');
insert into cinema values ('天幕影城', '海淀区', '北三环中路', '中视站', '36370013', '08:30', '23:30', '8.3');
insert into cinema values ('天宝国际影城', '朝阳区', '祁连街', '健翔站', '36370014', '08:30', '23:30', '8.4');
insert into cinema values ('中影国际影城', '海淀区', '外大街', '新街口站', '36370015', '09:30', '23:00', '8.5');
insert into cinema values ('大地影院', '海淀区', '越秀路', '同厦站', '36370016', '09:30', '23:00', '8.6');

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

insert into room_of_cinema values ('美嘉欢乐影城', '1');
insert into room_of_cinema values ('美嘉欢乐影城', '2');
insert into room_of_cinema values ('美嘉欢乐影城', '3');
insert into room_of_cinema values ('美嘉欢乐影城', '4');
insert into room_of_cinema values ('美嘉欢乐影城', '5');
insert into room_of_cinema values ('金逸国际影城', '6');
insert into room_of_cinema values ('金逸国际影城', '7');
insert into room_of_cinema values ('金逸国际影城', '8');
insert into room_of_cinema values ('金逸国际影城', '9');
insert into room_of_cinema values ('金逸国际影城', '10');
insert into room_of_cinema values ('工人文化宫', '11');
insert into room_of_cinema values ('工人文化宫', '12');
insert into room_of_cinema values ('工人文化宫', '13');
insert into room_of_cinema values ('工人文化宫', '14');
insert into room_of_cinema values ('工人文化宫', '15');
insert into room_of_cinema values ('UME国际影城', '16');
insert into room_of_cinema values ('UME国际影城', '17');
insert into room_of_cinema values ('UME国际影城', '18');
insert into room_of_cinema values ('UME国际影城', '19');
insert into room_of_cinema values ('UME国际影城', '20');
insert into room_of_cinema values ('星美影城', '21');
insert into room_of_cinema values ('星美影城', '22');
insert into room_of_cinema values ('星美影城', '23');
insert into room_of_cinema values ('星美影城', '24');
insert into room_of_cinema values ('星美影城', '25');

 
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

insert into userAccount values ('jfdke@qq.com', '李易峰', '343ffdd', '12330001', 'admin');
insert into userAccount values ('fdkj@qq.com', '王郁祥', 'erreeee', '12330002', 'admin');
insert into userAccount values ('fdffdf@qq.com', '王伟子', 'qerere', '12330003',  'admin');
insert into userAccount values ('axxxx@163.com', '庄涌临', '22333333', '12330004', 'admin');
insert into userAccount values ('qwe@qq.com', '郭家桥', '232444d', '12330005', 'admin');
insert into userAccount values ('pokeid@pku.edu.cn', 'abc', 'abc', '12213233',  'normal');
insert into userAccount values ('ppppppoe@gmail.com', 'bcd', 'bcd', '12132423',  'normal');
insert into userAccount values ('fertttt@google.com', 'cde', 'cde', '12444444', 'normal');
insert into userAccount values ('wefienz@126.com', 'def', 'edf', '12333333', 'normal');
insert into userAccount values ('uhijjdz@qq.com', 'efg', 'fge', '12220001', 'normal');
insert into userAccount values ('naodongdakai1@qq.com', '张1', '000001','12306901','normal');
insert into userAccount values ('naodongdakai2@qq.com', '张2', '000002','12306902','normal');
insert into userAccount values ('naodongdakai3@qq.com', '张3', '000003','12306903','normal');
insert into userAccount values ('naodongdakai4@qq.com', '张4', '000004','12306904','normal');
insert into userAccount values ('naodongdakai5@qq.com', '张5', '000005','12306905','normal');
insert into userAccount values ('naodongdakai6@qq.com', '张6', '000006','12306906','normal');
insert into userAccount values ('naodongdakai7@qq.com', '张7', '000007','12306907','normal');
insert into userAccount values ('naodongdakai8@qq.com', '张8', '000008','12306908','normal');
insert into userAccount values ('naodongdakai9@qq.com', '张9', '000009','12306909','normal');
insert into userAccount values ('naodongdakai10@qq.com', '张10', '000010','12306910','normal');
insert into userAccount values ('naodongdakai11@qq.com', '张11', '000011','12306911','normal');
insert into userAccount values ('naodongdakai12@qq.com', '张12', '000012','12306912','normal');
insert into userAccount values ('naodongdakai13@qq.com', '张13', '000013','12306913','normal');
insert into userAccount values ('naodongdakai14@qq.com', '张14', '000014','12306914','normal');
insert into userAccount values ('naodongdakai15@qq.com', '张15', '000015','12306915','normal');
insert into userAccount values ('naodongdakai16@qq.com', '张16', '000016','12306916','normal');
insert into userAccount values ('naodongdakai17@qq.com', '张17', '000017','12306917','normal');
insert into userAccount values ('naodongdakai18@qq.com', '张18', '000018','12306918','normal');
insert into userAccount values ('naodongdakai19@qq.com', '张19', '000019','12306919','normal');
insert into userAccount values ('naodongdakai20@qq.com', '张20', '000020','12306920','normal');
insert into userAccount values ('naodongdakai21@qq.com', '张21', '000021','12306921','normal');
insert into userAccount values ('naodongdakai22@qq.com', '张22', '000022','12306922','normal');
insert into userAccount values ('naodongdakai23@qq.com', '张23', '000023','12306923','normal');
insert into userAccount values ('naodongdakai24@qq.com', '张24', '000024','12306924','normal');
insert into userAccount values ('naodongdakai25@qq.com', '张25', '000025','12306925','normal');
insert into userAccount values ('naodongdakai26@qq.com', '张26', '000026','12306926','normal');
insert into userAccount values ('naodongdakai27@qq.com', '张27', '000027','12306927','normal');
insert into userAccount values ('naodongdakai28@qq.com', '张28', '000028','12306928','normal');
insert into userAccount values ('naodongdakai29@qq.com', '张29', '000029','12306929','normal');
insert into userAccount values ('naodongdakai30@qq.com', '张30', '000030','12306930','normal');
insert into userAccount values ('naodongdakai31@qq.com', '张31', '000031','12306931','normal');
insert into userAccount values ('naodongdakai32@qq.com', '张32', '000032','12306932','normal');
insert into userAccount values ('naodongdakai33@qq.com', '张33', '000033','12306933','normal');
insert into userAccount values ('naodongdakai34@qq.com', '张34', '000034','12306934','normal');
insert into userAccount values ('naodongdakai35@qq.com', '张35', '000035','12306935','normal');
insert into userAccount values ('naodongdakai36@qq.com', '张36', '000036','12306936','normal');
insert into userAccount values ('naodongdakai37@qq.com', '张37', '000037','12306937','normal');
insert into userAccount values ('naodongdakai38@qq.com', '张38', '000038','12306938','normal');
insert into userAccount values ('naodongdakai39@qq.com', '张39', '000039','12306939','normal');
insert into userAccount values ('naodongdakai40@qq.com', '张40', '000040','12306940','normal');



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

insert into movieShow values ('美嘉欢乐影城', '1', '2015-12-20', '20:00:00', '1','48');
insert into movieShow values ('美嘉欢乐影城', '2', '2015-12-20', '20:00:00', '2','56');
insert into movieShow values ('金逸国际影城', '1', '2015-12-20', '20:00:00', '6','48');
insert into movieShow values ('金逸国际影城', '2', '2015-12-20', '20:00:00', '7','56');
insert into movieShow values ('工人文化宫', '1', '2015-12-20', '20:00:00', '11','48');
insert into movieShow values ('工人文化宫', '2', '2015-12-20', '20:00:00', '12','56');
insert into movieShow values ('UME国际影城', '1', '2015-12-20', '20:00:00', '16','48');
insert into movieShow values ('UME国际影城', '2', '2015-12-20', '20:00:00', '17','56');
insert into movieShow values ('星美影城', '1', '2015-12-20', '20:00:00', '21','48');
insert into movieShow values ('星美影城', '2', '2015-12-20', '20:00:00', '22','56');


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
   
);
'''
    cu.executescript(sql_str)
    cx.commit()
    cu.close()
    cx.close()
    result={'info':'done!'}
    return HttpResponse(json.dumps(result), content_type="application/json")