#换手沉积一段时间（x日内总体换手值小于n）后，突然放量（换手值大于N）的情况【低换手持续时长；低换手阈值；高换手阈值；距离低谷时长；当前异动值】
import datetime
import os

import pandas as pd

import pub_uti_a


class global_param:
    #低谷换手阈值
    low_turn_value = 2
    #低谷时长阈值
    low_turn_long = 20
    #放量阈值
    high_turn_value = 3
    #高低谷间隔阈值
    high_low_turn_long = 5
class sections:
    def __init__(self,star_index=None,end_index=None,start_date=None,end_date=None):
        self.star_index = star_index
        self.end_index = end_index
        self.start_date = start_date
        self.end_date = end_date

class turn_volume_change_factor:
    def __init__(self,single_df):
        self.df = single_df
        self.low_sec_list = []
        self.high_sec_list = []
    def save(self):
        pass
    def deal_data(self):
        #计算换手三日均值
        self.df['turn_volume_mean_3'] = self.df['turnover_rate'].rolling(3).mean()
        self.df['turn_flag'] = 0
    def core(self):
        low_sec = sections()
        high_sec = sections()


        for ind,row in self.df.iterrows():
            #判断低谷
            if row['turn_volume_mean_3'] < global_param.low_turn_value:
                row['turn_flag'] = 1
                #判断section是否存在
                if low_sec.star_index is None:
                    low_sec.star_index = ind
                    low_sec.start_date = row['trade_date']
            else:
                #低谷长度符合条件，加入列表
                if low_sec.star_index != None:
                    if ind - low_sec.star_index > global_param.low_turn_long:
                        low_sec.end_index = ind
                        low_sec.end_date = row['trade_date']
                        self.low_sec_list.append(low_sec)
                        print('low_sec.start_date:',low_sec.start_date,'low_sec.end_date:',low_sec.end_date)
                    low_sec = sections()
            #判断高点
            if row['turnover_rate'] > global_param.high_turn_value:
                row['turn_flag'] = 2
                #判断section是否存在
                if high_sec.star_index is None:
                    high_sec.star_index = ind
                    high_sec.start_date = row['trade_date']
            else:
                #高点长度符合条件，加入列表
                if high_sec.star_index != None:
                    if len(self.low_sec_list) and (ind - self.low_sec_list[-1].end_index) <= global_param.high_low_turn_long:
                        high_sec.end_index = ind
                        high_sec.end_date = row['trade_date']
                        self.high_sec_list.append(high_sec)
                        print('high_sec.start_date:',high_sec.start_date,'high_sec.end_date:',high_sec.end_date)
                    high_sec = sections()
            #最后一次循环，保存高点section
            if ind == self.df.index[-1]:
                if high_sec.star_index != None:
                    high_sec.end_index = ind
                    high_sec.end_date = row['trade_date']
                    self.high_sec_list.append(high_sec)
                    print('high_sec.start_date1:',high_sec.start_date,'high_sec.end_date:',high_sec.end_date)

    def run(self):
        self.deal_data()
        self.core()
'''
def core(self):
    self.info = 'N'
    self.count_matching = 0
    # 判断之前区间中是否有single、hat信号
    self.begin = self.start - self.before_section
    section_flag = self.df['value_abnormal'][self.begin:self.start]
    # count_info = ((section_flag=='single')|(section_flag=='hat')|(section_flag=='single2')).sum()
    target_value = self.df.loc[self.start, 'value_a']
    section_value = self.df['value_a'][0:self.start]
    section_flag = self.df['value_abnormal'][0:self.start]
    continuous_flag = True
    # 记录连续符合abnormal值的天数
    count_hat = 0  # 记录满足hat的天数
    for i in range(len(section_value) - 1, -1, -1):
        if section_flag[i] in self.info_tup:
            if continuous_flag:
                count_hat += 1
            else:
                break
        else:
            continuous_flag = False
            if section_value[i] * self.flag_num <= target_value:
                self.count_matching += 1
            else:
                break
    if self.count_matching > 3:
        if count_hat >= self.highland_num:
            self.info = "highland"
        elif count_hat >= self.hat_num:
            self.info = "hat"
        elif count_hat >= 1:  # 总统计大于连续计数，表示有间隔
            self.info = 'single2'
        else:
            self.info = "single"
    else:
        self.info = 'N'
    self.df.loc[self.start, ['value_abnormal', 'count_matching']] = [self.info, self.count_matching]
'''
#####################################验证因子############################################
###生成结果
class conf_param:
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    #基础路径
    base_path = 'E:/Code/stock_strategy/factor/factor_verify_res/换手率因子/'
    #结果文件名
    res_file_name = 'result.csv'
#写一个函数，判断基础路径是否存在
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
def save_result(list_data):
    df = pd.DataFrame(list_data)
    df.to_csv(conf_param.base_path + conf_param.res_file_name,index=False)
def main(test = False):
    #创建文件夹
    check_path(conf_param.base_path)
    sql = "SELECT trade_code,stock_id,stock_name,trade_date,turnover_rate  " \
          "FROM stock_trade_data " \
          " WHERE trade_date >= '{start_date}' AND trade_date <= '{end_date}' ".format(
        start_date=conf_param.start_date, end_date=conf_param.end_date)

    #test
    if test:
        sql = "SELECT trade_code,stock_id,stock_name,trade_date,turnover_rate  " \
              "FROM stock_trade_data " \
              " WHERE trade_date >= '{start_date}' AND trade_date <= '{end_date}' AND stock_id='002553'".format(start_date = conf_param.start_date, end_date = conf_param.end_date)
        print('sql:',sql)
    df = pub_uti_a.creat_df(sql, ascending=True)
    id_set = set(df['stock_id'].to_list())
    count = 1
    result_list = []
    for id in id_set:
        print('id',count,id)
        count += 1
        single_df = df[df.stock_id == id]
        single_df.reset_index(drop=True, inplace=True)
        if single_df.empty:
            continue
        ########因子生成##########
        t = turn_volume_change_factor(single_df)
        t.run()
        # print(t.low_sec_list,'\n',t.high_sec_list)
        #########
        low_sec_list = []
        high_sec_list = []
        for sec in t.low_sec_list:
            low_sec_list.append((sec.start_date,sec.end_date))
        for sec in t.high_sec_list:
            high_sec_list.append((sec.start_date,sec.end_date))
        if not (low_sec_list and high_sec_list):
            continue
        result_dict = {'stock_id': id, 'stock_name': single_df.loc[0,'stock_name'],
                       'low_sec_list': '', 'high_sec_list': ''}
        result_dict['low_sec_list'] = str(low_sec_list)
        result_dict['high_sec_list'] = str(high_sec_list)
        result_list.append(result_dict)
    save_result(result_list)

if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - start)