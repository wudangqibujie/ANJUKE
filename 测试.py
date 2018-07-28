from lxml import etree
import logging
import matplotlib

import aiohttp


import requests
logging.basicConfig(level=logging.INFO)
def master_parse(page_source ):
    html = etree.HTML(page_source)
    item_data = html.xpath('//ul[@id="houselist-mod-new"]/li')
    next_item = html.xpath('//div[@class="multi-page"]/a')
    if next_item:
        if "下一页" in next_item[-1].xpath('text()')[0]:
            next_url = next_item[-1].xpath('@href')
            if next_url:
                logging.info("下一页连接" + next_url[0])
    if item_data:
        for i in item_data:
            item = dict()
            item["title"] = i.xpath('div[@class="house-details"]/div[1]/a/@title')
            item["link"] = i.xpath('div[@class="house-details"]/div[1]/a/@href')
            item["room_style"] = i.xpath('div[@class="house-details"]/div[2]/span[1]/text()')
            item["size"] = i.xpath('div[@class="house-details"]/div[2]/span[2]/text()')
            item["year"] = i.xpath('div[@class="house-details"]/div[2]/span')[-2].xpath('text()')
            item["name_location"] =i.xpath('div[@class="house-details"]/div[3]/span/@title')
            logging.info(item)
def commen_req(url,headers,html_queue=None,proxies=None):
    try:
        r = requests.get(url,headers=headers,proxies=proxies)
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
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
url = "https://shenzhen.anjuke.com/sale/luohu/"
page = commen_req(url,headers=headers)
master_parse(page)