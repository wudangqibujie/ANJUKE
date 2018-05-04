import parse
import req
import datadase
import pymongo
import time
import multiprocessing as mp
import logging
logging.basicConfig(level=logging.INFO)
import url_manager
from lxml import etree
class Master(object):
     def __init__(self,city_name,spider_name):
         self.city_name = city_name
         self.req = req.Req()
         self.ur_man = url_manager.UrlMana("SZ_"+"anjuke")
         self.parse = parse.Parse()
         self.spider_name = spider_name
         self.mongo = datadase.Data2Mongo(spider_name)
     def city_urls(self):
         url = "https://www.anjuke.com/sy-city.html"
         page_spurce = self.req.commen_req(url,self.req.headers)
         for i in self.parse.cityurls_parse(page_spurce):
             self.mongo.insert_data("city_urls", i)
     def sale_init_task(self):
         city_url = self.mongo.find_city_url(self.city_name)+r"/sale/"
         print(city_url)
         page_source1 = self.req.commen_req(city_url,headers=self.req.headers)
         zone_urls = self.parse.city_init_task(page_source1)
         for zone in zone_urls:
             page_source2 = self.req.commen_req(zone,headers=self.req.headers)
             domain_urls = self.parse.zone_init_task(etree.HTML(page_source2))
             print(domain_urls)
             self.ur_man.init_task(domain_urls)
def block_task_pro(block_queue):
    ur= url_manager.UrlMana("SZ_" + "anjuke")
    while True:
         try:
             logging.info("正在生成任务块")
             time.sleep(2.5)
             tasks = ur.task_create_filter(1)
             logging.info("任务块"+str(tasks))
             if tasks:
                 block_queue.put(tasks)
             else:
                 logging.info("任务队列已空")
                 break
         except Exception as e:
             logging.info(e)
             logging.info("生成任务块出错")
             break
def html_pro(block_queue,html_queue):
     req1 = req.Req()
     while True:
         try:
             tasks = block_queue.get()
             logging.info("获取到的任务块"+str(tasks))
             req1.thre_req(tasks,{"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"},html_queue)
         except Exception as e:
             logging.info(e)
             logging.info("生成HTML有误或者队列块已空！")
             break
def item_pro(html_queue,item_queue,new_task_queue,old_task_queue):
     parse1 = parse.Parse()
     while True:
         try:
             ht = html_queue.get()
             if isinstance(ht,str):
                 new_task_queue.put(ht)
             if isinstance(ht,list):
                 logging.info("完成解析的链接"+ht[0])
                 parse1.master_parse(ht,item_queue,old_task_queue)
         except Exception as e:
             logging.info(e)
             logging.info("生成item出错")
             break
def item2_database_pro(item_queue,new_task_queue):
     client = pymongo.MongoClient("localhost", 27017)
     db = client["anjuke_SZ"]
     coll = db["item_data"]
     while True:
         try:
             it = item_queue.get()
             if isinstance(it,str):
                 new_task_queue.put(it)
                 logging.info("下一页连接"+it)
             else:
                 logging.info("生成的数据"+str(it))
                 coll.insert(it)
         except Exception as e:
             logging.info("数据过滤入库有误或者item已空！")
             break
def task_rein(new_task_queue):
     ur = url_manager.UrlMana("SZ_" + "anjuke")
     while True:
         try:
             new_task = new_task_queue.get()
             if new_task:
                 ur.new_task(new_task)
         except Exception as e:
             logging.info(e)
             logging.info("生成任务队列返回失败或者已空!")
             break
def gather_old_pro(old_queue):
     ur = url_manager.UrlMana("SZ_" + "anjuke")
     while True:
         try:
             old_url = old_queue.get()
             ur.old_task(old_url)
             logging.info("已抓取完的url"+old_url)
         except Exception as e:
             logging.info(e)
             break
if __name__ == '__main__':
    m = Master("深圳","anjuke")
    m.sale_init_task()
    block_queue = mp.Queue()
    html_queue = mp.Queue()
    item_queue = mp.Queue()
    new_task_queue = mp.Queue()
    old_task_queue = mp.Queue()
    p1 = mp.Process(target=block_task_pro, args=(block_queue,))
    p2 = mp.Process(target=html_pro, args=(block_queue, html_queue))
    p3 = mp.Process(target=item_pro, args=(html_queue, item_queue, new_task_queue, old_task_queue))
    p4 = mp.Process(target=item2_database_pro, args=(item_queue, new_task_queue))
    p5 = mp.Process(target=task_rein, args=(new_task_queue,))
    p6 = mp.Process(target=gather_old_pro, args=(old_task_queue,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

