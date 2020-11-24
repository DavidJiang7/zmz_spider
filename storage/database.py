import pymssql
import redis
import logging,time,threading

class ZMZDBConnect:
    def __init__(self):
        self.server = '127.0.0.1'
        self.port = 1433
        self.user = 'sa'
        self.password = 'root'
        self.database = 'zmz'

    def open_connection(self):
        return pymssql.connect(self.server, self.user, self.password, self.database, port=self.port, autocommit=True)

    def insert_data(self,item:...,table_name:str):
        '''
        指定表插入数据
        '''
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder,tablename: """insert into {tablename} ({col}) values ({placeholder})""".format(tablename=tablename,col=col, placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys)),table_name), args)
        except Exception as e:
            logging.error(e)
            raise e

class RedisConnect:
    def __init__(self, *args, **kwargs):
        self.host = ''
        self.password = ''
        self.db = 1
        self.port = 63791
        self.pool = redis.ConnectionPool(host=self.host,port=self.port,db=self.db,password=self.password)
        self.conn = redis.Redis(connection_pool=self.pool)        
