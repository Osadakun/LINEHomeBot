import pymysql
import pymysql.cursors
 
connection = pymysql.connect(
        host='ホスト',
        user='ユーザー名',
        password='パスワード',
        db='データベース名',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()               
    finally:
        cursor.close()
        connection.close()
 

