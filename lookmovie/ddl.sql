
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
