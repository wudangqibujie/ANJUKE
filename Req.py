import asyncio
import aiohttp
import multiprocessing as mp
import threading as th
import requests
import logging
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
    def commen_req(self,url,headers,html_queue=None,proxies=None):
        try:
            r = requests.get(url,headers=headers,proxies=proxies)
            if r.status_code == 200:
                if html_queue == None:
                    print(r.status_code)
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
    def thre_req(self,urls,headers,html_queue,proxies=None):
        try:
            th_lst = [th.Thread(target=self.commen_req,args = (url,headers,html_queue,proxies)) for url in urls]
            for i in th_lst:
                i.start()
        except Exception as e:
            logging.info(e)
            logging.info("多线程请求异常")
if __name__ == '__main__':
    pass
    # rq = Req()
    # urls = ["https://shenzhen.anjuke.com/sale/p{}/".format(i) for i in range(1,11)]
    # html_queue = mp.Queue()
    # rq.thre_req(urls,rq.headers,html_queue)
    # while True:
    #     try:
    #         print(html_queue.get())
    #     except:
    #         print("OVER")
    #         break





