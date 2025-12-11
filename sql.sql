INSERT INTO account_userprofile(first_name, last_name, middle_name, address, number, email, date_of_birth, age, gender,user_id, role)
VALUES ('Shubham','Sharma','Dayaram','Surat','9879703884','shubhu2960@gmail.com','2003-12-01',20,'male',9,'user')

UPDATE account_userprofile SET email='shubham216@gmail.com' WHERE user_id=8;

DELETE FROM account_userprofile WHERE id= 9;

SELECT * FROM home_blog WHERE user_id = 37;

