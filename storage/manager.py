import logging
import json
import pymssql
from storage.database import ZMZDBConnect, RedisConnect
from urllib import request


class ZMZManager(ZMZDBConnect):
    def get_channel_list(self):
        sql = """select * from ChannelList where status = 0"""
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    _rows = cur.fetchall()
                    columns = [col[0] for col in cur.description]
                    return [ { k:v for k,v in zip(columns, row) } for row in _rows]
        except Exception as e:
            logging.error(e)
            return []

    def get_resource(self, pageSize):
        sql = """select top {size} * from Resource where status = 0""".format(size=pageSize)
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    _rows = cur.fetchall()
                    columns = [col[0] for col in cur.description]
                    return [ { k:v for k,v in zip(columns, row) } for row in _rows]
        except Exception as e:
            logging.error(e)
            return []
            
    def update_resource_status(self, id):
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('update Resource set status=1,updatetime=getdate() where id=%s', (id,))
        except Exception as e:
            logging.error(e)

    def is_exist_resource(self, id):
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT TOP 1 Id FROM Resource WHERE Id = %s', (id,))
                    _row = cur.fetchone()
                    if _row is None:
                        return False
                    else:
                        return True
        except Exception as e:
            logging.error(e)
            return True

    def update_channel_list(self, id):
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('update ChannelList set status=1 where id=%s', (id,))
        except Exception as e:
            logging.error(e)

    def insert_resource(self, item):
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder: """IF NOT EXISTS (SELECT TOP 1 Id FROM Resource WHERE id = {id}) insert into Resource ({col}) values ({placeholder})""".format(id=item['Id'],col=col,placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys))), args)
        except Exception as e:
            logging.error(e)
        
    def insert_character(self, item):
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder: """IF NOT EXISTS (SELECT TOP 1 Id FROM Character WHERE id = {id}) insert into Character ({col}) values ({placeholder})""".format(id=item['Id'],col=col,placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys))), args)
        except Exception as e:
            logging.error(e)

        
    def insert_resource_prop(self, item):
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder: """IF NOT EXISTS (SELECT TOP 1 Id FROM ResourceProp WHERE ResourceId = {resourceId} and PropName = '{propname}' and PropValue = '{propvalue}') insert into ResourceProp ({col}) values ({placeholder})""".format(resourceId=item['ResourceId'],propname=item['PropName'].replace("'", "''").replace("@", "@@"),propvalue=item['PropValue'].replace("'", "''").replace("@", "@@"),col=col,placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys))), args)
        except Exception as e:
            logging.error(e)
        
    def insert_resource_character(self, item):
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder: """IF NOT EXISTS (SELECT TOP 1 Id FROM ResourceCharacter WHERE ResourceId = {ResourceId} and CharacterId = {CharacterId} and CharacterType = '{CharacterType}') insert into ResourceCharacter ({col}) values ({placeholder})""".format(ResourceId=item['ResourceId'],CharacterId=item['CharacterId'],CharacterType=item['CharacterType'].replace("'", "''").replace("@", "@@"),col=col,placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys))), args)
        except Exception as e:
            logging.error(e)
            
    def insert_resource_link(self, item):
        try:
            with self.open_connection() as conn :
                with conn.cursor() as cur:
                    sql = lambda col, placeholder: """insert into ResourceLink ({col}) values ({placeholder})""".format(col=col,placeholder=placeholder)
                    keys = list(item.keys())
                    args= tuple([item[key] for key in keys])
                    cur.execute(sql(','.join(keys), ','.join(['%s ']*len(keys))), args)
        except Exception as e:
            logging.error(e)
            
    def get_one_resource_link(self, resourceId, linkId):
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT TOP 1 * FROM ResourceLink WHERE ResourceId = {rid} and LinkId = {lid} '.format(rid=resourceId, lid=linkId))
                    _rows = cur.fetchall()
                    columns = [col[0] for col in cur.description]
                    result = [ { k:v for k,v in zip(columns, row) } for row in _rows]
                    return result[0]
        except Exception as e:
            #logging.error(e)
            return None
            
    def update_resource_link(self, item):
        try:
            with self.open_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""update ResourceLink set Title='{title}', MagnetUrl='{m}', Ed2kUrl='{e}' where id={id}""".format(title=item['Title'].replace("'", "''").replace("@", "@@"), m=item['MagnetUrl'].replace("'", "''").replace("@", "@@"), e=item['Ed2kUrl'].replace("'", "''").replace("@", "@@"), id=item['Id']))
        except Exception as e:
            #logging.error(e)
            pass


class RedisManager(RedisConnect):
    def Sismember(self,key: str, val: str):
        return self.conn.sismember(key,val)
    def LPUSH(self,key:str,val:str):
        return self.conn.lpush(key,val)
    def RPUSH(self,key:str,val:str):
        return self.conn.rpush(key,val)
    def SADD(self,key:str,val:str):
        return self.conn.sadd(key,val)
    
