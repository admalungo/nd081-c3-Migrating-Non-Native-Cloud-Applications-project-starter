import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="ndproj3pgsqldb.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="pgadmin@ndproj3pgsqldb" #TODO: Update value
    POSTGRES_PW="ndproj3db!"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://ndproj3sb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+NxQdEsq8gNuhttk3Y71pgwaTnou46OG207sEI0611M=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'admalungo@hotmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False