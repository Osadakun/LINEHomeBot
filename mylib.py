import psycopg2
import os
import homestatus

def SQL_fetch(DATABASE_URL,*SQL_order,UserID):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor() 
    vars = homestatus.UserID, detected_language['language'], str(post_id) # tuple
    cursor.execute(SQL_order,vars)
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
