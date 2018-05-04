import redis
def get_ip():
    r = redis.Redis()
    ip_lst = r.srandmember("free_ip",5)
    ip_lst = [{"http":i.decode("utf-8"),"https":i.decode("utf-8")} for i in ip_lst]
    return ip_lst


test_url = "http://httpbin.org/ip"
import req
urls = [test_url for _ in range(5)]
import multiprocessing as mp
html_queue = mp.Queue()
req = req.Req()
req.thre_req(urls,req.headers,html_queue,get_ip())
while True:
    a = html_queue.get()
    if isinstance(a,list):
        print(a)

