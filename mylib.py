import psycopg2
import os
import homestatus

def SQL_name(DATABASE_URL,*SQL_order):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor() 
    cursor.execute(SQL_order[0] + "'" + SQL_order[1] + "'"+ ";")
    conn.commit()
    message = ''
    first = True 
    while True:
        temp = cursor.fetchone()
        if temp:
            if first:
                if len(temp)==1:
                    message = message + str(temp[0])
                else:
                    message = message + str(temp)
                first = False
            else:
                if len(temp)==1:
                    message = message + '\n' + str(temp[0])
                else:
                    message = message + '\n' + str(temp)
        else:
            if first:
                message = None
                print('SQL_fetch empty')
            break
    cursor.close()
    conn.close()
    return message

def SQL_status(DATABASE_URL,*SQL_order):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(SQL_order[0] + SQL_order[1] + ' and ' + 'Family_Member.name = ' + "'" + SQL_order[2] +"'"+ ";")
    cursor.execute('SELECT * FROM Family_Member WHERE name = ' + "'" + SQL_order[2]+ "'" + ";")
    #print(cursor.fetchone())
    conn.commit()
    message = ''
    first = True
    while True:
        #temp = cursor.fetchone()
        temp = cursor.fetchone()
        if temp:
            if first:
                if len(temp)==1:
                    message = message + str(temp[0])
                else:
                    message = message + str(temp)
                first = False
            else:
                if len(temp)==1:
                    message = message + '\n' + str(temp[0])
                else:
                    message = message + '\n' + str(temp)
        else:
            if first:
                message = None
                print('SQL_fetch empty')
            break
    cursor.close()
    conn.close()
    return message
