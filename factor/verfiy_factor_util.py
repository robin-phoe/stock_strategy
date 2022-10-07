###验证因子的基础函数
import mpl_finance
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
import pub_uti_a

class market:
    def __init__(self,trade_date,stock_id,stock_name,open_price,close_price,high_price,low_price,increase):
        self.trade_date = trade_date
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.open_price= open_price
        self.close_price= close_price
        self.high_price= high_price
        self.low_price= low_price
        self.increase= increase
class market_hub:
    def __init__(self,start_date,end_date):
        print('market start.', datetime.datetime.now())
        self.start_date = start_date
        self.end_date = end_date
        self.market_df = None
        self.market_buffer = {}
        self.select_market()
        self.create_market_buffer()
    #创建时段内行情信息
    def select_market(self):
        sql = "select trade_code,trade_date,stock_id,stock_name,open_price,close_price,high_price,low_price,increase " \
              " from {0} " \
              "where trade_date >= '{1}' and trade_date <= '{2}' ".format('stock_trade_data',self.start_date,self.end_date)
        self.market_df = pub_uti_a.creat_df(sql)
        print('market select complete.', datetime.datetime.now())
    #create buffer
    def create_market_buffer(self):
        for index,row in self.market_df.iterrows():
            self.market_buffer.setdefault(row['trade_date'],{})
            # print('row',row,'\n',row['trade_date'],self.market_buffer)
            self.market_buffer[row['trade_date']][row['stock_id']] = market(trade_date=row['trade_date'],stock_id = row['stock_id'],
                                                                       stock_name = row['stock_name'],open_price= row['open_price'],close_price= row['close_price'],
                                                                       high_price= row['high_price'],low_price= row['low_price'],increase= row['increase'])
        print('market buffer complete.', datetime.datetime.now())
    def get_market_by_day(self,date,stock_id)-> market:
        return self.market_buffer.get(date).get(stock_id)
    #返回pic k线数据[[time,open,close,high,low],[]]
    def get_market_pic_data(self,date_list,stock_id):
        market_res = []
        count = 0
        for date in date_list:
            market = self.get_market_by_day(date,stock_id)
            if market:
                market_res.append([count,market.open_price,market.close_price,market.high_price,market.low_price])
                count += 1
        return market_res
'''
class plot_bar_new:
    def __init__(self,chart_title,day_line_data,result_dir):
        self.chart_title = chart_title
        self.day_line_data = day_line_data
        self.result_dir = result_dir
        # self.draw_k_line(chart_title,market_res)
        # self.attach_drow()
        # self.save_pic()
        self.is_exist()
    #判断文件夹是否存在
    def is_exist(self):
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
    def draw_k_line(self,chart_title,data):
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(figsize=(23, 5))
        # ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))#时间轴
        ax.set_title(chart_title, fontsize=20)
        # 绘制K线图
        mpl_finance.candlestick_ochl(
            ax=ax,
            quotes=data,#df[['dates', 'open_price', 'close_price', 'high_price', 'low_price']].values,
            width=0.7,
            colorup='r',
            colordown='g',
            alpha=0.7)
    def attach_drow(self):
        plt.axvline(t_s_index, c='red')
        plt.axvline(t_e_index, c='red')
        plt.legend();

    def save_pic(self):
        image_path = '../{}/{}.jpg'.format(self.result_dir, chart_title)
        plt.savefig(image_path)
        plt.close('all')
        # plt.show()
'''
#原方法
class plot_bar:
    def __init__(self,start_date,end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.market_date_range = ()
        self.return_file_dir = "E:\\Code\\stock_strategy\\factor\\factor_verify_res\\换手率因子\\result.csv"#return_18-22_test.csv
        self.return_df = None
        self.trade_date_list = []
        self.before_long = 60
        self.after_long = 10
        self.year = None

    def select_return_file(self):
        try:
            self.return_df = pd.read_csv(self.return_file_dir, encoding=u'gbk')
        except:
            self.return_df = pd.read_csv(self.return_file_dir)
    def create_tradedate_list(self):
        sql = "select distinct trade_date from {0} where trade_date >= '{1}' and trade_date <= '{2}'".format(
            base_config.source_table,self.start_date,self.end_date
        )
        trade_data_df = pub_uti_a.creat_df(sql,ascending=True)
        self.trade_date_list = trade_data_df['trade_date'].to_list()
        print('trade_date_list:',self.trade_date_list)
    def run(self):
        m = market_hub(self.start_date,self.end_date)
        self.create_tradedate_list()
        self.select_return_file()
        # 恢复账号前导0
        self.return_df['stock_id'] = self.return_df['stock_id'].apply(lambda x: str(x).rjust(6, '0'))
        # 日期处理
        self.return_df['start_date'] = self.return_df['start_date'].astype(str).apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d'))
        self.return_df['end_date'] = self.return_df['end_date'].astype(str).apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d'))
        # 交易数据切片
        self.return_df = self.return_df[(self.return_df['start_date'] >= self.start_date)&(self.return_df['end_date'] <= self.end_date)]
        date_len = len(self.trade_date_list)
        for index,row in self.return_df.iterrows():
            self.year = row['start_date'][0:4]
            id = row['stock_id']
            print(row['stock name'])
            stock_name = re.sub('\*','',row['stock name'])
            chart_title = "{}".format(stock_name)
            m_s_index = self.trade_date_list.index(row['start_date']) - self.before_long
            m_e_index = self.trade_date_list.index(row['end_date']) + self.after_long
            if m_s_index < 0:
                m_s_index = 0
            if m_e_index > date_len:
                m_e_index = date_len
            pic_date_list = self.trade_date_list[m_s_index:m_e_index]
            t_s_index = pic_date_list.index(row['start_date'])
            t_e_index = pic_date_list.index(row['end_date'])
            market_res = []
            count = 0
            for date in pic_date_list:
                market = m.get_market_by_day(date,id)
                if market:
                    market_res.append([count,market.open_price,market.close_price,market.high_price,market.low_price])
                    count += 1
            try:
                self.draw_k_line(chart_title,market_res,t_s_index,t_e_index)
            except Exception as err:
                print(stock_name,err)

    def draw_k_line(self,chart_title,data,t_s_index,t_e_index):

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(figsize=(23, 5))
        # ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))#时间轴
        ax.set_title(chart_title, fontsize=20)
        # 绘制K线图
        mpl_finance.candlestick_ochl(
            ax=ax,
            quotes=data,#df[['dates', 'open_price', 'close_price', 'high_price', 'low_price']].values,
            width=0.7,
            colorup='r',
            colordown='g',
            alpha=0.7)
        plt.axvline(t_s_index, c='red')
        plt.axvline(t_e_index, c='red')
        plt.legend();
        # plt.show()
        image_path = 'E:\\Code\\stock_strategy\\factor\\factor_verify_res\\换手率因子\\pic\\{}.jpg'.format(chart_title)
        plt.savefig(image_path)
        plt.close('all')
        # plt.clf()
if __name__ == '__main__':
    plot_bar('2022-01-01','2022-09-01').run()