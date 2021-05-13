# セッション変数の取得
from setting import session
# Userモデルの取得
from user import *
from sqlalchemy import *

# DBにレコードの追加
user = User()
user.name = '太郎'
session.add(user)  
session.commit()

# Userテーブルのnameカラムをすべて取得
users = session.query(User).all()
for user in users:
    print(user.name)

