CREATE TABLE toutiao (
id integer primary key autoincrement,
info json,
created_at datetime default (datetime('now','localtime')),
updated_at datetime default (datetime('now','localtime'))
);