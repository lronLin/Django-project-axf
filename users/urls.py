
from django.conf.urls import url

from users import views

urlpatterns = [
    # 个人中心
    url(r'^my/', views.my, name='my'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 注册
    url(r'^register/', views.register, name='register'),
    # 注销
    url(r'^logout/', views.logout, name='logout')
]