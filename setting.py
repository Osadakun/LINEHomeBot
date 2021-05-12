from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


ENGINE = create_engine(
    "postgres://ylcywgvpxrfldl:7f634f2f7881359957c4483720f765f28ef2e78677c230352f4868d05d156bc9@ec2-3-234-22-132.compute-1.amazonaws.com:5432/db7j7l1274gbnb",
    encoding = "utf-8",
    echo=True # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = ENGINE
        )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

