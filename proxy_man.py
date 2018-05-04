import req
import redis
import time
import redis
url = "http://www.mogumiao.com/proxy/free/listFreeIp"
def free_ip():
    url = "http://www.mogumiao.com/proxy/free/listFreeIp"
    html = req.Req().commen_req(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    raw_ip = eval(html)
    ip_list = [i["ip"] + ":" + i["port"] for i in raw_ip["msg"]]
    return ip_list

def free_run():
    r = redis.Redis()
    while True:
        try:
            for i in free_ip():
                r.sadd("free_ip", i)
            time.sleep(180)
            r.delete("free_ip")
        except:
            print("IP提取有误")
            break
if __name__ == '__main__':
    a = free_ip()
    print(a)
    free_run()
