import Parse
import Req
import Datadase

class Master(object):
     def __init__(self):
         self.req = Req.Req()
         self.parse = Parse.Parse()
         self.mongo = Datadase.Data2Mongo("anjuke")
     def city_urls(self):
         url = "https://www.anjuke.com/sy-city.html"
         page_spurce = self.req.commen_req(url,self.req.headers)
         for i in self.parse.init_task_parse(page_spurce):
             self.mongo.insert_data("city_urls", i)
    
if __name__ == '__main__':
    m = Master()
    m.city_urls()

