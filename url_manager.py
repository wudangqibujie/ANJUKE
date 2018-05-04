import redis
import logging
logging.basicConfig(level=logging.INFO)

class UrlMana(object):
    def __init__(self,spider_name):
        self.r = redis.Redis()
        self.spider_name = spider_name
    def init_task(self,urls):
        for i in urls:
            self.r.sadd(self.spider_name+"_new_master_task",i)
    def new_task(self,url):
        self.r.sadd(self.spider_name+"_new_master_task",url)
    def old_task(self,url):
        self.r.sadd(self.spider_name+"_old_master_task",url)
    def task_create_filter(self,task_num):
        raw = [self.r.spop(self.spider_name+"_new_master_task") for _ in range(task_num)]
        flesh_task = [i.decode("utf-8") for i in raw if not self.r.sismember(self.spider_name+"_old_master_task",i) and i != None]
        return flesh_task



