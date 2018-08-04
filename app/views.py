from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, \
    MainShow, FoodType, Goods, CartModel, OrderModel, OrderGoodsModel
from utils.functions import get_order_num


def Home(request):
    if request.method == 'GET':
        # 获取轮播图信息
        mainwheels = MainWheel.objects.all()
        # 导购
        mainnavs = MainNav.objects.all()
        # 必购
        mainmustbuys = MainMustBuy.objects.all()
        # 商店
        mainshops = MainShop.objects.all()
        # 主要展示的商品
        mainshows = MainShow.objects.all()

        # 轮播图数据
        data = {
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainmustbuys': mainmustbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,
        }
        return render(request, 'home/home.html', data)


# 闪购超市
def Market(request):
    if request.method == 'GET':
        # 跳转传参 - kwargs传字典 / args传元组
        return HttpResponseRedirect(reverse('axf:marketparams', kwargs={'typeid': 104749,
                                                                        'cid': 0,
                                                                        'sid': 0}))


# 商品信息 - 继承闪购超市的方法与传参typeid:闪购类型 / cid:子分类 / sid:排序
def MarketParams(request, typeid, cid, sid):
    if request.method == 'GET':
        # 获取所有商品信息
        foodtypes = FoodType.objects.all()
        # 商品分类信息
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)

        # 排序
        if sid == '0':
            pass
        elif sid == '1':
            # 销量排序 - 倒序
            goods = goods.order_by('-productnum')
            # 降价排序
        elif sid == '2':
            goods = goods.order_by('-price')
            # 升价排序
        elif sid == '3':
            goods = goods.order_by('price')
        # 获取子分类商品
        childtypenames = FoodType.objects.filter(typeid=typeid).first().childtypenames
        # 以 : # 分隔全部分类商品与子分类商品
        childtypenames_list = [i.split(':') for i in childtypenames.split('#')]

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'cid': cid,
            'sid': sid,
            'childtypenames_list': childtypenames_list,
        }
        # 跳转到闪购页面
        return render(request, 'market/market.html', data)


# 添加购物车
def AddToCart(request):

    if request.method == 'POST':
        # 获取关联用户
        user = request.user
        data = {}
        data['code'] = '1001'
        if user.id:
            # 获取关联商品id
            goods_id = request.POST.get('goods_id')
            # 验证当前用户是否对同一商品进行添加操作
            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果是用户的购物车
            if cart:
                # 如果购物车有商品, 则商品数量加1
                cart.c_num += 1
                cart.save()
                data['c_num'] = cart.c_num
            else:
                # 登录的当前用户没有添加商品到购物车中, 则去创建
                CartModel.objects.create(user=user, goods_id=goods_id)
                # 如果购物车没有商品, 则商品的数量为1
                data['c_num'] = 1
            data['code'] = '200'
            data['msg'] = '请求成功!'
            return JsonResponse(data)
        return JsonResponse(data)


# 减少购物车商品数量
def SubToCart(request):

    if request.method == 'POST':
        # 获取用户信息
        user = request.user
        data = {}
        data['code'] = '1001'
        data['msg'] = '请求成功'
        # 验证用户信息
        if user.id:
            # 用户是否对应商品(获取商品)
            goods_id = request.POST.get('goods_id')
            # 获取用户下单对应的商品信息
            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果购物车中已经存在了商品信息(判断是否有数据, 没有则不作处理)
            if cart:
                if cart.c_num == 1:
                    # 直接删除购物车中的商品信息
                    cart.delete()
                    data['c_num'] = 0
                else:
                    # 如果不等于0, 在其基础数量上减1
                    cart.c_num -= 1
                    cart.save()
                    data['c_num'] = cart.c_num
                data['code'] = '200'
                return JsonResponse(data)
            else:
                data['msg'] = '请先添加商品'
                return JsonResponse(data)
        else:
            data['msg'] = '用户没有登录, 请去登录!'
            return JsonResponse(data)


# 闪购页面商品数量
def GoodNum(request):
    if request.method == 'GET':
        user = request.user
        cart_list = []
        if user.id:
            carts = CartModel.objects.filter(user=user)
            for cart in carts:
                data = {
                    'id': cart.id,
                    'goods_cart': cart.goods,
                    'c_num': cart.c_num,
                    'user_id': cart.user_id,
                }
                cart_list.append(data)
            return JsonResponse({'cart': cart_list, 'code': '200'})
        else:
            JsonResponse({'carts': '', 'code': '1001'})


# 购物车页面
def Cart(request):
    if request.method == 'GET':
        # 获取用户信息
        user = request.user
        # 获取购物车数据
        carts = CartModel.objects.filter(user=user)
        # 跳转到购物车页面
        return render(request, 'cart/cart.html', {'carts': carts})


# 修改购物车中商品的选择状态
def changeCartStatus(request):

    if request.method == 'POST':
        # 获取购物车id
        cart_id = request.POST.get('cart_id')
        # 获取购物车数据
        carts = CartModel.objects.get(pk=cart_id)
        if carts.is_select:
            carts.is_select = False
        else:
            carts.is_select = True
        carts.save()
        return JsonResponse({'code': '200', 'is_select': carts.is_select})


# 计算价格
def goodsCount(request):
    if request.method == 'GET':
        # 获取用户
        user = request.user

        # 获取当前用户选择的商品
        carts = CartModel.objects.filter(user=user, is_select=True)
        count_prices = 0
        for cart in carts:
            # 所有商品的价格
            count_prices += cart.goods.price * cart.c_num

        # 处理小数后几位 : round - 保留3位数
        # 处理浮点数 : '%.2f' - 数字为保留几位
        count_prices = '%.2f' % count_prices
        return JsonResponse({'count': count_prices, 'code': 200})


# 下单
def order(request):
    if request.method == 'POST':
        user = request.user
        if user.id:
            # 哪些商品需要下单
            carts = CartModel.objects.filter(user=user, is_select=True)
            # 创建订单
            o_num = get_order_num()
            order = OrderModel.objects.create(user=user, o_num=o_num)
            # 创建订单详情信息
            for cart in carts:
                OrderGoodsModel.objects.create(order=order,
                                               goods=cart.goods,
                                               goods_num=cart.c_num)
            # 删除购物车中已经下单的商品信息
            carts.delete()

            return JsonResponse({'code': 200, 'order_id': order.id})


# 商品支付的页面
def orderInfo(request):
    if request.method == 'GET':

        # 获取订单id
        order_id = request.GET.get('order_id')
        # 获取下单商品信息
        order_goods = OrderGoodsModel.objects.filter(order_id=order_id)
        return render(request, 'order/order_info.html', {'order_goods': order_goods})


# 修改订单状态
def changeOrderStatus(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()
        order.o_status = 1
        order.save()
        return JsonResponse({'code': 200})


# 待支付 o_status=0
def waitPay(request):
    if request.method == 'GET':
        user = request.user
        # 待付款订单信息
        orders = OrderModel.objects.filter(user=user, o_status=0)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


# 待收货 o_status=1
def Payed(request):
    if request.method == 'GET':
        user = request.user
        # 待收货订单信息
        orders = OrderModel.objects.filter(user=user, o_status=1)
        return render(request, 'order/order_list_payed.html', {'orders': orders})


# 全选
def changeCartAllSelect(request):
    if request.method == 'POST':
        user = request.user
        is_select = request.POST.get('all_select')
        # flag为一个变量名, 判断条件是否成立
        flag = False
        carts = CartModel.objects.filter(user=user)
        if is_select == '1':
            CartModel.objects.filter(user=user).update(is_select=True)
        else:
            flag = True
            CartModel.objects.filter(user=user).update(is_select=False)
            data = {
                'code': 200,
                'ids': [u.id for u in carts],
                'flag': flag,
            }
            return JsonResponse(data)








