# coding: utf-8


 
class DBManage(object):
    def __init__(self):
        self.data = {}  # {user_id: {name: {"date": date, is_zh: False}}]}
        
    def set(self, user_id, name, date, is_zh=False):
        dic = self.data.setdefault(user_id, {}).setdefault(name, {})
        dic["date"] = date
        dic["is_zh"] = is_zh
        return [(name, dic["date"], dic["is_zh"])]
        
    def get_all(self, user_id):
        res = []
        dic = self.data.get(user_id, {})
        for name, val in dic.items():
            res.append((name, val["date"], val["is_zh"]))
        return res
        
    def name2date(self, user_id, name):
        dic = self.data.get(user_id, {}).get(name, {})
        if dic:
            return [(name, dic["date"], dic["is_zh"])]
        return []
        
    def date2name(self, user_id, date):
        res = []
        dic = self.data.get(user_id, {})
        for k, v in dic.items():
            if v["date"] == date:
                res.append((k, date, v["is_zh"]))
        return res


manage = DBManage()

