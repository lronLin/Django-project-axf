
import random
from datetime import datetime


# 获取ticket值
def get_ticket():
    ticket = ''
    # 随机设置值
    s = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    for i in range(100):
        # 用ticket去接收 随机产生的值
        ticket += random.choice(s)
    return ticket


# 随机生成订单编号
def get_order_num():

    num = ''
    s = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    for i in range(10):
        num += random.choice(s)
    order_time = datetime.now().strftime('%Y%m%d%H%M%S')
    return order_time + num

