
from django.conf.urls import url

from app import views

urlpatterns = [
    # 首页
    url(r'^home/', views.Home, name='home'),
    # 闪购超市
    url(r'^market/', views.Market, name='market'),
    # 访问闪购超市跳转到marketparams这个函数上来
    url(r'^marketparams/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sid>\d+)/', views.MarketParams, name='marketparams'),
    # 添加购物车
    url(r'^addtocart/', views.AddToCart, name='addtocart'),
    # 删除购物车
    url(r'^subtocart/', views.SubToCart, name='subtocart'),
    # 刷新闪购页面商品数量
    url(r'^goodsnum/', views.GoodNum, name='goodsnum'),
    # 购物车页面
    url(r'^cart/', views.Cart, name='cart'),
    # 修改购物车中商品的选择状态 is_select = True / False
    url(r'^changeCartStatus', views.changeCartStatus, name='changeCartStatus'),
    # 计算价格
    url(r'^goodsCount/', views.goodsCount, name='goodsCount'),
    # 下单
    url(r'^order/', views.order, name='order'),
    # 修改订单状态 o_status = 0 / 1
    url(r'^changeOrderStatus/', views.changeOrderStatus, name='changeOrderStatus'),
    # 商品支付的页面
    url(r'^orderInfo/', views.orderInfo, name='orderInfo'),
    # 待支付
    url(r'^waitPay/', views.waitPay, name='waitPay'),
    # 待收货
    url(r'^payed/', views.Payed, name='payed'),
    # 全选
    url(r'^changeCartAllSelect/', views.changeCartAllSelect, name='changeCartAllSelect'),


]
