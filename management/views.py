# -*- coding:utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Book, Img, OrderInfo
from django.core.urlresolvers import reverse
from management.utils import permission_check
from management.check_code import send_sms

import random


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None

    if request.method == 'POST':

        mobilephone = request.POST.get('mobilephone', '')
        send_sms(mobile=mobilephone)
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif len(password) <= 5:
            state = 'too_short'
        elif password != repeat_password:
            state = 'repeat_error'
        elif len(mobilephone) != 11:
            state = 'phone_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password, )
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''),
                                     mobilephone=request.POST.get('mobilephone', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def test(request):
    rand_number = random.randint(1000, 9999)

    # global rand_number

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None

    if request.is_ajax():
        mobilephone = request.POST.get('mobilep', '')
        if len(mobilephone) != 11:
            state = 'phone_error'
        else:
            send_sms(text='您的验证码是：' + str(rand_number) + '。请不要把验证码泄露给其他人。', mobile=mobilephone)
            global string
            string = str(rand_number)

    if request.method == 'POST':

        mobilephone = request.POST.get('mobilephone', '')
        checkcode = request.POST.get('checkcode', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if checkcode != string:
            state = 'checkcode_error'

        elif password == '' or repeat_password == '':
            state = 'empty'
        elif len(password) <= 5:
            state = 'too_short'
        elif password != repeat_password:
            state = 'repeat_error'
        elif len(mobilephone) != 11:
            state = 'phone_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password, )
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''), mobilephone=mobilephone)
                new_my_user.save()
                state = 'success'

    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/test.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@login_required
def forget_password(request):
    user = request.user
    state = None

    rand_number = random.randint(1000, 9999)

    if request.is_ajax():
        mobilephone = request.POST.get('mobile', '')
        if len(mobilephone) != 11:
            state = 'phone_error'
        else:
            send_sms(text='您的验证码是：' + str(rand_number) + '。请不要把验证码泄露给其他人。', mobile=mobilephone)
            global string1
            string1 = str(rand_number)

    if request.method == 'POST':

        checkcode = request.POST.get('checkcode', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if checkcode != string1:
            state = 'checkcode_error'
        else:
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    content = {
        'user': user,
        'myuser': MyUser.objects.filter(user_id=request.user.id),
        'active_menu': 'personal_account',
        'state': state,
    }
    return render(request, 'management/forget_password.html', content)


@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
            name=request.POST.get('name', ''),
            author=request.POST.get('author', ''),
            category=request.POST.get('category', ''),
            price=request.POST.get('price', 0),
            publish_date=request.POST.get('publish_date', ''),
            user_id_id=request.user.id,
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
        'myuser': MyUser.objects.filter(user_id=request.user.id),
    }
    return render(request, 'management/add_food.html', content)


def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    return render(request, 'management/view_food_list.html', content)


@login_required
def detail(request):
    user = request.user if request.user.is_authenticated() else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))

    if request.method == 'POST':
        order_info = OrderInfo(
            name=request.POST.get('name', ''),
            order_seq=datetime.now().strftime("%Y%m%d%H%M%S").strip(':'),
            order_num=request.POST.get('order_num', ''),
            price=request.POST.get('price', ''),
            total_price=request.POST.get('total_price', ''),
            my_account=request.POST.get('my_account', ''),

            user_name_id=request.user.id,
            book=Book.objects.get(pk=book_id),

        )
        order_info.save()
        # 更新MyUser表中的account

        obj = MyUser.objects.get(user_id=request.user.id)
        for i in OrderInfo.objects.filter(user_name_id=request.user.id):
            obj.account = i.my_account
        obj.save()

    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
        'orderInfo': OrderInfo,
        'myuser': MyUser.objects.filter(user_id=request.user.id),
    }
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                name=request.POST.get('name', ''),
                description=request.POST.get('description', ''),
                img=request.FILES.get('img', ''),
                book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)


def personal_account(request):
    content = {
        'active_menu': 'personal_account',
    }
    return render(request, 'management/personal_account.html', content)


def my_account(request):
    content = {
        'active_menu': 'personal_account',
        'orderInfo': OrderInfo.objects.filter(user_name_id=request.user.id),
        'myuser': MyUser.objects.filter(user_id=request.user.id),

    }
    return render(request, 'management/my_account.html', content)


def adminer(request):
    content = {
        'active_menu': 'adminer',
    }
    return render(request, 'management/adminer.html', content)


def adminer_account(request):
    content = {
        'active_menu': 'adminer_account',
    }
    return render(request, 'management/adminer_account.html', content)


def apply_auditing(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

        book = Book.objects.get(id=request.POST.get('id', ''))
        book.is_allow = request.POST.get('is_allow', '')
        book.save()

        obj = MyUser.objects.get(user_id=request.user.id)
        for i in OrderInfo.objects.filter(user_name_id=request.user.id):
            obj.account = i.my_account
        obj.save()

        book = Book.objects.get(id=request.POST.get('id', ''))




        # 审核菜品权限
        # Book.objects.filter(id=2).update(is_allow=1)

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'adminer',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,

    }

    return render(request, 'management/apply_auditing.html', content)


def user_management(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'user': user,
        'myuser': MyUser.objects.all(),
        'active_menu': 'adminer',
    }
    return render(request, 'management/user_management.html', content)


def permission_apply(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'user': user,
        'myuser': MyUser.objects.all(),
        'active_menu': 'personal_account',
    }
    return render(request, 'management/permission_apply.html', content)


@login_required
def info_modify(request):
    user = request.user if request.user.is_authenticated() else None
    info_id = request.GET.get('id', '')
    if info_id == '':
        return HttpResponseRedirect(reverse('user_management'))
    try:
        info = User.objects.get(pk=info_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('user_management'))

    state = None
    if request.method == 'POST':

        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if not new_password:
            state = 'empty'
        elif new_password != repeat_password:
            state = 'repeat_error'
        else:
            info.set_password(new_password)
            info.save()
            state = 'success'

    content = {
        'user': user,
        'myuser': MyUser.objects.all(),
        'state': state,
        'active_menu': 'adminer',
    }
    return render(request, 'management/info_modify.html', content)
