from lxml import etree
import logging
logging.basicConfig(level=logging.INFO)
class Parse(object):
    def __init__(self):
        pass
    def master_parse(self,page_source,q,old_task_queue):
        html = etree.HTML(page_source[1].text)
        item_data = html.xpath('//ul[@id="houselist-mod-new"]/li')
        next_item = html.xpath('//div[@class="multi-page"]/a')
        if next_item:
            if "下一页" in next_item[-1].xpath('text()')[0]:
                next_url = next_item[-1].xpath('@href')
                if next_url:
                    logging.info("下一页连接" + next_url[0])
                    q.put("https://www.xin.com" + next_url[0])
        if item_data:
            for i in item_data:
                item = dict()
                item["title"] = i.xpath('div[@class="house-details"]/div[1]/@title')
                item["room_style"] = i.xpath('div[@class="house-details"]/div[2]/span[1]/text()')
                item["size"] = i.xpath('div[@class="house-details"]/div[2]/span[2]/text()')
                item["year"] = i.xpath('div[@class="house-details"]/div[2]/span[3]/text()')
                item["name)location"] =i.xpath('div[@class="house-details"]/div[3]/span/@title')
                logging.info(item)
                old_task_queue.put(page_source[0])
                q.put(item)
    def init_task_parse(self,page_source):
        html = etree.HTML(page_source)
        items = html.xpath('//ul/li')
        for i in items:
            lst = i.xpath('div/a')
            for j in lst:
                item = dict()
                item[j.xpath('text()')[0]] = j.xpath('@href')[0]
                logging.info(item)
                yield item
if __name__ == '__main__':
    import requests
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
    r = requests.get("https://www.anjuke.com/sy-city.html",headers=headers)
    p = Parse()
    for i in p.init_task_parse(r.text):
        print(i)


