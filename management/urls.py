# -*- coding: utf-8 -*-
from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_book_list/$', views.view_book_list, name='view_food_list'),
    url(r'^view_book/detail/$', views.detail, name='detail'),
    url(r'^personal_account/$', views.personal_account, name='personal_account'),
    url(r'^my_account/$', views.my_account, name='my_account'),
    url(r'^adminer/$', views.adminer, name='adminer'),
    url(r'^apply_auditing/$', views.apply_auditing, name='apply_auditing'),
    url(r'^user_management/$', views.user_management, name='user_management'),
    url(r'^permission_apply/$', views.permission_apply, name='permission_apply'),
    url(r'^info_modify/$', views.info_modify, name='info_modify'),
    url(r'^adminer_account/$', views.adminer_account, name='adminer_account'),
    url(r'^test/$', views.test, name='test'),
    url(r'^forget_password/$', views.forget_password, name='forget_password'),

]
