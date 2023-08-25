import os
########    ENV VARIABLE    ########
MYSQL_ADDRESS=os.environ.get("MYSQL_HOST","localhost")
MYSQL_USER=os.environ.get("MYSQL_USER","DefaultMysqlUser")
MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD","DefaultMysqlPassword")
MYSQL_DB=os.environ.get("MYSQL_DB","DefaultMysqlDb")

REDIS_ADDRESS=os.environ.get("REDIS_HOST","localhost")+":"+os.environ.get("REDIS_PORT","6379")
REDIS_HOST=os.environ.get("REDIS_HOST","localhost")
REDIS_PORT=os.environ.get("REDIS_PORT","6379")
REDIS_PASSWORD=os.environ.get("REDIS_PASSWORD","")
REDIS_DB=os.environ.get("REDIS_DB","0")

MAIL_USER=os.environ.get("MAIL_USER","Default@default.com")
MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD","DefaultMailPassword")
