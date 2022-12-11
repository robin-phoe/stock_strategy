#平稳k 线后 上影线，双因子联合测试

#打印当前路径
import datetime
import sys

import pandas as pd

sys.path.append('E:\\Code\\stock_strategy\\factor\\')
print(sys.path)
import pub_uti_a
from verfiy_factor_util import market #相对路径报错，采用绝对路径
from factor.factor_base import shangyingxian_factor,steady_k_line_factor
class shangyingxian_steady_double_factors:
    def __init__(self):
        self.df = None
        self.res_df = None
        self.start_date = '2022-10-01'
        self.end_date = '2022-10-25'
        self.steady_long_param = 10
        self.res_dir = 'E:\\Code\\stock_strategy\\factor\\factor_verify_res\\上影线_k线平稳双因子\\'
    def select_market(self):
        sql = "select trade_code,trade_date,stock_id,stock_name,open_price,close_price,high_price,low_price,increase " \
                " from {0} " \
                "where trade_date >= '{1}' and trade_date <= '{2}' ".format('stock_trade_data',self.start_date,self.end_date)
        self.df = pub_uti_a.creat_df(sql,ascending=True)
        #滤科创板
        self.df = self.df[~self.df['stock_id'].str.startswith(('688','300'))]
    def core(self):
        #股票列表
        stock_set = set(self.df['stock_id'].to_list())
        #结果列表
        res_list = []
        #遍历所有股票
        count = 0
        for stock_id in stock_set:
            single_df = self.df[self.df['stock_id'] == stock_id]
            single_df.reset_index(drop=True,inplace=True)
            #遍历所有日期
            for index,row in single_df.iterrows():
                market_obj = market(trade_date=row['trade_date'],stock_id = row['stock_id'],
                                    stock_name = row['stock_name'],open_price= row['open_price'],close_price= row['close_price'],
                                    high_price= row['high_price'],low_price= row['low_price'],increase= row['increase'])
                #判断是否符合上影线因子
                if shangyingxian_factor.shangyingxian().core(market_obj):
                    #计算索引区间
                    start_index = index - self.steady_long_param
                    if start_index < 0:
                        start_index = 0
                    end_index = index
                    #判断是否符合平稳k线因子
                    res = steady_k_line_factor.before_section(single_df,start_index,end_index).core()
                    if res['reach']:
                        count += 1
                        print('符合双因子：',count,market_obj.stock_id,market_obj.trade_date)
                        res_list.append({'stock_id':market_obj.stock_id,'stock_name':market_obj.stock_name,'trade_date':market_obj.trade_date})
        #结果写入df
        self.res_df = pd.DataFrame(res_list)
        #存储结果
        self.save_df_to_csv()
    #存储df结果到csv
    def save_df_to_csv(self):
        #验证文件夹是否存在
        pub_uti_a.verify_folder_exist(self.res_dir)
        # print('{}shangyingxian_steady_factors_{}.csv'.format(self.res_dir,datetime.datetime.now().strftime('%m%d%H%M%S')))
        self.res_df.to_csv('{}shangyingxian_steady_factors_{}.csv'.format(self.res_dir,datetime.datetime.now().strftime('%m%d%H%M%S')),index=False)


if __name__ == '__main__':
    s = shangyingxian_steady_double_factors()
    s.select_market()
    s.core()