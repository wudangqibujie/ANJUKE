import asyncio
import aiohttp
import multiprocessing as mp
import threading as th
import requests
import random
import logging
import time
logging.basicConfig(level=logging.INFO)

class Req(object):
    def __init__(self):
        self.headers = headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    async def get(self,url,html_queue):
        async with aiohttp.ClientSession() as resp:
            try:
                async with resp.get(url,headers = self.headers,proxy=None) as resp:
                    page = await resp.text()
                    html_queue.put([url,page])
            except:
                logging.info(url+"请求出错")
                html_queue.put(url)
    def cun(self,urls,q):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self.get(i,q) for i in urls]
        loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()
    def commen_req(self,url,headers,html_queue=None):
        targetUrl = "http://httpbin.org/ip"
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        # 代理隧道验证信息
        proxyUser = "H05Q64265150WYAD"
        proxyPass = "E1E56BEB2C26CFBC"
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        proxies = {"http": proxyMeta,"https": proxyMeta,}
        try:
            r = requests.get(url,headers=headers,proxies=None)
            logging.info(str(r.status_code)+url)
            if r.status_code == 200:
                if html_queue == None:
                    return r.text
                else:
                    html_queue.put([url,r])
            else:
                logging.info("请求码非200！")
        except Exception as e:
            logging.info(url+"请求发生异常")
            logging.info(e)
            if html_queue != None:
                html_queue.put(url)
    def thre_req(self,urls,headers,html_queue):
        try:
            th_lst = [th.Thread(target=self.commen_req,args = (url,headers,html_queue)) for url in urls]
            for i in th_lst:
                i.start()
        except Exception as e:
            logging.info(e)
            logging.info("多线程请求异常")
if __name__ == '__main__':
    rq = Req()
    html_queue = mp.Queue()
    urls = ["https://shenzhen.anjuke.com/sale/p{}/#filtersort".format(i) for i in range(1,10)]
    # urls = ["http://httpbin.org/ip" for _ in range(10)]
    rq.thre_req(urls,rq.headers,html_queue)
    while True:
        try:
            a = html_queue.get()
            if isinstance(a,str):
                print("没有请求成功的url",a)
            if isinstance(a,list):
                print(a[0])
        except:
            break










