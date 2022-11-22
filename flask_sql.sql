
CREATE DATABASE IF NOT EXISTS geek_login DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE geek_login;

CREATE table if not exists accounts (
	id int(11) not null auto_increment,
    username varchar(50) unique not null,
    password varchar(255) not null,
    email varchar(100) not null,
    primary key(id)
)engine=InnoDB auto_increment=2 default charset=utf8;

CREATE table if not exists blogDetails (
	blog_id int(11) not null auto_increment,
    blog_title varchar(255),
    blog_content varchar(255),
    creation_time varchar(255),
    id int(11),
    foreign key(id) references accounts(id),
    primary key(blog_id)
)engine=InnoDB auto_increment=2 default charset=utf8;

select * from accounts;