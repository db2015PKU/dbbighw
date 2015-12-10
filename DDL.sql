create database MyCinema;

create table cinema
	(cinema_name	varchar(40) not null,    
    district	varchar(20) not null,         
    road	varchar(20) not null,             
    busStation	varchar(20) not null, 		  
    phone	varchar(50) not null,			  
    businessHours time not null,
    estimate numeric(2,1) check(estimate > 0 and estimate < 10),
    movie_name		varchar(40),
    room		varchar(10),
    primary key(cinema_name));
    
create table movie
	(movie_name		varchar(40) not null,
    show_date		date not null,
    show_time		time not null,
    runtime			varchar(20) not null,
    director		varchar(40),
    actors          varchar(40),
    movie_type	    varchar(40) check(movie_type in ("literary","horror","action","comedy","pornographic","thriller")),
	movie_language		varchar(20) check(movie_language in ("Chinese","English")),
    price			numeric(4,2) not null,
    /*room			varchar(10),*/
    tickets_left    int,
    primary key(movie_name),
    /*foreign key(room) references cinema
					on delete set null);*/
                    
create table userAccount
	(user_id		varchar(30) not null,
    user_name		varchar(30) not null,
    user_password 		varchar(30) not null,
    user_phone      varchar(20),
    user_permissions	varchar(15) check (user_permissions in("admin","normal")),
    primary key(user_id));
    
create table ticket
	(ticket_id		varchar(20) not null,
	movie_name		varchar(40) not null,
    cinema_name     varchar(40) not null,
    show_date		date not null,
    show_time		time not null,
    room			varchar(2) not null,
    seatno			int(3) not null,
    primary key(ticket_id),
    foreign key(movie_name) references movie
					on delete cascade,
	foreign key(cinema_name) references cinema
					on delete cascade,
    foreign key(room) references cinema
					on delete set null
    );

create table movieShow
	(cinema_name 	varchar(40) not null,
    show_date		date not null,
    show_time		time not null,
    room			varchar(2) not null,
    price			numeric(4,2) not null,
    primary key(cinema, show_date, show_time, room, price),
    foreign key(cinema_name,room) references cinema
					on delete cascade,
    foreign key(show_date, show_time, price) references movie
					on delete cascade);
 
 create table sellTickets
	(ticket_id		varchar(20) not null,
    movie_name		varchar(40) not null,
    show_date		date not null,
    show_time		time not null,
    room			varchar(2) not null,
    seatno			int(3) not null,
    primary key(ticket_id),
    foreign key(ticket_id, seatno) references ticket
					on delete cascade,
	foreign key(room) references cinema
					on delete cascade);
 
