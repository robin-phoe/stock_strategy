#判断一段时间区间内日k线是否平稳
#输入：[single_df,start_date,end_date]
#输出：{'reach':[bool],'steady_rate_abs':[float]}
#判断一段时间内是否走势平稳
class before_section:
    def __init__(self,single_df,start_index,end_index,reach_rate=1.5):
        self.single_df = single_df
        self.start_index = start_index
        self.end_index = end_index
        self.reach_rate = reach_rate
    #筛选数据
    def filter_data(self):
        self.single_df = self.single_df[self.start_index:self.end_index]
        self.single_df.sort_values(by='trade_date', ascending=True,inplace=True)
        self.single_df.reset_index(drop=True, inplace=True)

    #计算k线平稳度
    def core(self):
        self.filter_data()
        #计算k线increase绝对值变化幅度
        self.single_df['increase_abs'] = self.single_df['increase'].abs()
        #计算k线increase绝对值变化幅度均值
        increase_abs_mean = self.single_df['increase_abs'].mean()
        if increase_abs_mean <= self.reach_rate:
            return {'reach':True,'steady_rate_abs':increase_abs_mean}


if __name__ == '__main__':
    pass