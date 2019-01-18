from django.db import models


class StoreBase(list):

    STOR_DEFAULT_URL = 'https://job.firstvds.ru/spares.json'
    ALTS_DEFAULT_URL = 'https://job.firstvds.ru/alternatives.json'


    def _check_alts(self):
        #Пересчитывает позиции по списку аналогов.
        for k in self.alts.keys():
            cnt, arr, mbe = 0, 0, 0
            for i in self.alts.get(k):
                item = self.stor.get(i)
                if (i in self.stor.keys()):
                    self.stor.pop(i)
                else:
                    continue
                cnt += item.get('count') 
                arr += item.get('arrive')
                mbe = mbe if (mbe > item.get('mustbe')) else item.get('mustbe')
            self.stor[k] = {'count': cnt, 'mustbe': mbe, 'arrive': arr}
            if (cnt + arr < mbe):
                self.order_list[k] = mbe - arr - cnt


    def _build_order_list(self):
        #Пересчитывает недостающие по всему списку.
        for k in self.stor.keys():
            item = self.stor.get(k)
            cnt = item.get('count') 
            arr = item.get('arrive')
            mbe = item.get('mustbe')
            if (cnt + arr < mbe):
                self.order_list[k] = mbe - (arr + cnt)


    def _build_whole_list(self):
        #Строит таблицу отчета
        for item_name in self.stor.keys():
            warns = item_name in self.order_list.keys()
            item = self.stor.get(item_name)
            c = str(item.get('count'))
            a = str(item.get('arrive'))
            m = str(item.get('mustbe'))
            self.append([warns, item_name, c, a, m])


    def __init__(self, *, stor_src=STOR_DEFAULT_URL, alts_src=ALTS_DEFAULT_URL):
        from json import loads
        from urllib.request import urlopen
        
        alts = urlopen(alts_src).read()
        stor = urlopen(stor_src).read()
        
        self.alts = loads(alts).get('alternatives')
        self.stor = loads(stor)
        self.order_list = {}

        self._check_alts()
        self._build_order_list()
        self._build_whole_list()


    def dump_order_to_json(self, *, path='store.json', name='order_list'):
        #Сохраняет спецификацию для заказа в json-файл.
        from json import dumps

        self.order_list = dict({name: self.order_list})      
        with open(path, mode='w') as f:
            f.write(dumps(self.order_list, sort_keys=True, indent=4))
