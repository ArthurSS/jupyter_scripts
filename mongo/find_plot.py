# encoding:utf-8

import datetime
import pymongo
import pprint

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
#mpl.style.use('ggplot')
myfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')  
mpl.rcParams['axes.unicode_minus'] = False

#创建服务器
default_client = pymongo.MongoClient('localhost', 27017)
#选择数据库
space_db = default_client['VnTrader_Space_Parity_Db']
#选择collection和document
datetime1 = datetime.datetime(2016, 12, 28, 9, 0, 0)
datetime2 = datetime.datetime(2016, 12, 28, 10, 15, 0)
datetime3 = datetime.datetime(2016, 12, 28, 10, 30, 0)
datetime4 = datetime.datetime(2016, 12, 28, 11, 30, 0)
datetime5 = datetime.datetime(2016, 12, 28, 13, 30, 0)
datetime6 = datetime.datetime(2016, 12, 28, 15, 0, 0)
columns_ = ['close_ca', 'open_ca', 'target_ca', 'fore_ca', 'close_re', 'open_re', 'target_re', 'fore_re', 'time']
query_ = {'$or':[{'$and':[{'time':{'$gt':datetime1}},{'time':{'$lt':datetime2}}]},\
                 {'$and':[{'time':{'$gt':datetime3}},{'time':{'$lt':datetime4}}]},\
                 {'$and':[{'time':{'$gt':datetime5}},{'time':{'$lt':datetime6}}]}]}

#collections列表
coll_names = ["m1703-C-2250", "m1703-C-2300", "m1703-C-2350", "m1703-C-2400", "m1703-C-2450", "m1703-C-2500", "m1703-C-2550", \
         "m1703-C-2600", "m1703-C-2650", "m1703-C-2700", "m1703-C-2750", "m1703-C-2800", "m1703-C-2850", "m1703-C-2900", \
         "m1703-C-2950", "m1703-C-3000", "m1703-C-3050", "m1703-C-3100", "m1703-C-3150", "m1703-C-3200", "m1703-C-3250", \
         "m1703-C-3300", "m1703-C-3350", "m1703-C-3400", "m1703-C-3450", "m1703-C-3500", "m1703-C-3550", "m1705-C-2450", \
         "m1705-C-2500", "m1705-C-2550", "m1705-C-2600", "m1705-C-2650", "m1705-C-2700", "m1705-C-2750", "m1705-C-2800", \
         "m1705-C-2850", "m1705-C-2900", "m1705-C-2950", "m1705-C-3000", "m1705-C-3050", "m1705-C-3100", "m1705-C-3150", \
         "m1705-C-3200", "m1705-C-3250", "m1705-C-3300", "m1705-C-3350", "m1705-C-3400", "m1705-C-3450", "m1707-C-2450", \
         "m1707-C-2500", "m1707-C-2550", "m1707-C-2600", "m1707-C-2650", "m1707-C-2700", "m1707-C-2750", "m1707-C-2800", \
         "m1707-C-2850", "m1707-C-2900", "m1707-C-2950", "m1707-C-3000", "m1707-C-3050", "m1707-C-3100", "m1707-C-3150", \
         "m1707-C-3200", "m1708-C-2450", "m1708-C-2500", "m1708-C-2550", "m1708-C-2600", "m1708-C-2650", "m1708-C-2700", \
         "m1708-C-2750", "m1708-C-2800", "m1708-C-2850", "m1708-C-2900", "m1708-C-2950", "m1708-C-3000", "m1708-C-3050", \
         "m1708-C-3100", "m1708-C-3150", "m1708-C-3200", "m1708-C-3250", "m1709-C-2500", "m1709-C-2550", "m1709-C-2600", \
         "m1709-C-2650", "m1709-C-2700", "m1709-C-2750", "m1709-C-2800", "m1709-C-2850", "m1709-C-2900", "m1709-C-2950", \
         "m1709-C-3000", "m1709-C-3050", "m1709-C-3100", "m1709-C-3150", "m1709-C-3200", "m1711-C-2550", "m1711-C-2600", \
         "m1711-C-2650", "m1711-C-2700", "m1711-C-2750", "m1711-C-2800", "m1711-C-2850", "m1711-C-2900", "m1711-C-2950", \
         "m1711-C-3000", "m1711-C-3050", "m1711-C-3100", "m1711-C-3150", "m1711-C-3200"]

coll_arr = np.array(coll_names).reshape(55,2)
fig, axes = plt.subplots(nrows=55, ncols=2)
plt.figure(figsize=[16,4*55])
for row_ in range(55):
    for col_ in range(2):
        docs = space_db[coll_arr[row_, col_]].find(query_, columns_).sort([('time', pymongo.ASCENDING)])
        result = pd.DataFrame(list(docs), columns=columns_).dropna(how='any')
        result = result.loc[:, ['close_re', 'open_re', 'target_re']]
        #result.loc[:,'fore_re'][result.fore_re>50] = 50
        #result.loc[:,'fore_re'][result.fore_re<-50] = -50
        result = result[result.close_re>-300]
        result = result[result.close_re<300]
        result.plot(ax=axes[row_,col_], legend=False, title=coll_arr[row_, col_], grid=True, figsize=[16,4*55])
plt.show()