# wlog/urls.py
from django.urls import path

from . import views


app_name = 'wlog'
urlpatterns = [
    # 主页显示所有标题
    path('', views.titles, name='titles'),
    
    # 查看某个标题下的所有日志
    path('<int:title_id>/logs/', views.logs_by_title, name='logs_by_title'),
    
    # 查看单个日志详情
    path('log/<int:log_id>/', views.log_detail, name='log_detail'),
    
    # 创建日志
    path('log/create/', views.LogCreateView.as_view(), name='log_create'),
    
    # 为特定标题创建日志
    path(
        'title/<int:title_id>/log/create/',
        views.LogCreateView.as_view(),
        name='log_create_for_title'
    ),
]