#上影线因子
#上时间冷淡振幅走势后，突然拉出上影线
#输入：market,[high_increase_param,h_c_rate_param]
#输出：真：(h_inc,h_c_rate)  假：False
from .. verfiy_factor_util import market
class shangyingxian:
    def __init__(self,high_increase_param=0.05,h_c_rate_param=2):
        self.high_increase_param = high_increase_param
        self.h_c_rate_param = h_c_rate_param #上影线顶点与收盘价长度比例（high_increase/increase）
    def core(self,market:market):
        market: market = market
        #昨收盘价
        pre_close_price = market.close_price / (1 + market.increase/100)
        #判断高值是否达标
        h_inc = market.high_price / pre_close_price -1
        if h_inc < self.high_increase_param:
            return False
        #上影线顶点与收盘价长度比例（high_increase/increase）
        h_c_rate = (market.high_price / pre_close_price - 1) / abs(market.increase/100 + 0.000001)
        #判断上影线顶点与收盘价长度比例是否达标
        if h_c_rate < self.h_c_rate_param:
            return False
        return (h_inc,h_c_rate)



if __name__ == '__main__':
    pass
