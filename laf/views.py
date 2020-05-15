from django.shortcuts import render, redirect
from laf.models import User, Object
from PIL import UnidentifiedImageError
from django.contrib import messages
from laf.forms import RegisterForm, LoginForm, ChangeForm, ForgetForm
from django.core.mail import send_mail
from website import settings
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import random
import re
from location.locationInfo import PROVINCE, CITY
import datetime


email_captcha = ''  # 邮箱验证码
categories = ['---请选择---', '钱包', '钥匙', '宠物', '首饰', '体育用品', '数码产品', '卡类/证件', '挎包/包裹', '衣服/鞋帽', '书籍/文件', '其他']


# 主页视图
@cache_page(60 * 15)
def home(request):
    return render(request, 'home.html')


# 寻物启事视图
def lost(request):
    if not request.session.get('is_login', False):
        messages.info(request, '您尚未登录，请登录后重试')
        return redirect(to='/accounts/login/')

    if request.method == 'POST':
        errors = {}

        result = clean_filter(request.POST, errors)
        if result:
            objects = filter_list(request, lost=True)
            context = {
                'objects': objects,
                'categories': categories,
                'provinces': get_provinces()
            }
            return render(request, 'lost.html', context)
        else:
            context = {
                'errors': errors,
                'categories': categories,
                'provinces': get_provinces(),
                'objects': Object.objects.filter(lost=True)
            }
            return render(request, 'lost.html', context)

    if request.method == 'GET':
        objects = Object.objects.filter(lost=True)
        context = {
            'categories': categories,
            'provinces': get_provinces(),
            'objects': objects
        }
        return render(request, 'lost.html', context)


# 招领启事视图
def found(request):
    if not request.session.get('is_login', False):
        messages.info(request, '您尚未登录，请登录后重试')
        return redirect(to='/accounts/login/')

    if request.method == 'POST':
        errors = {}

        result = clean_filter(request.POST, errors)
        if result:
            objects = filter_list(request, lost=False)
            context = {
                'objects': objects,
                'categories': categories,
                'provinces': get_provinces()
            }
            return render(request, 'lost.html', context)
        else:
            context = {
                'errors': errors,
                'categories': categories,
                'provinces': get_provinces(),
                'objects': Object.objects.filter(lost=False)
            }
            return render(request, 'lost.html', context)

    if request.method == 'GET':
        objects = Object.objects.filter(lost=False)
        context = {
            'categories': categories,
            'provinces': get_provinces(),
            'objects': objects
        }
        return render(request, 'lost.html', context)


# 上传启事信息视图
def upload(request):
    if not request.session.get('is_login', False):
        messages.info(request, '您尚未登录，请登录后重试')
        return redirect(to='/accounts/login/')

    provinces = get_provinces()

    if request.method == 'POST':
        errors = {}

        result = clean_upload(request.POST, errors)
        if result:
            user = User.objects.get(username=request.session['username'])
            lost = request.POST['lost']
            category = request.POST['category']
            date = request.POST['date']
            province = request.POST['province']
            city = request.POST['city']
            image = request.FILES.get('image')
            detail = request.POST['detail']

            if lost == 'True':
                lost = True
            else:
                lost = False
            try:
                obj = Object(
                    user=user,
                    category=category,
                    date=date,
                    province=province,
                    city=city,
                    image=image,
                    detail=detail, lost=lost
                )
                obj.save()
            except UnidentifiedImageError:
                errors['image'] = '仅支持图片文件!'

            context = {
                'categories': categories,
                'provinces': provinces,
                'errors': errors
            }
            if 'image' in errors:
                return render(request, 'upload.html', context)
            else:
                if lost:
                    messages.success(request, '发布寻物启事成功，点击确认进入寻物页面')
                    return redirect(to='/lost/')
                else:
                    messages.success(request, '发布招领启事成功，点击确认进入招领页面')
                    return redirect(to='/found/')

        else:
            context = {
                'categories': categories,
                'provinces': provinces,
                'errors': errors
            }
            return render(request, 'upload.html', context)

    if request.method == 'GET':
        context = {
            'categories': categories,
            'provinces': provinces
        }
        return render(request, 'upload.html', context)


# 注册视图
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if request.POST.get('agree_protocol', None):
                data = form.cleaned_data
                new_user = User(
                    username=data['username'],
                    gender=data['gender'],
                    age=data['age'],
                    phone_number=data['phone_number'],
                    email=data['email'],
                    password=data['password']
                )
                new_user.save()
                messages.success(request, '注册成功，请登录')
                return redirect(to='/accounts/login/')
            else:
                errors = form.errors
                errors['agree_protocol'] = '您必须遵守用户协议才能继续'
                result = refresh_captcha_hashkey_image_url()
                hashkey = result['hashkey']
                image_url = captcha_image_url(hashkey)
                context = {
                    'form': form,
                    'errors': errors,
                    'hashkey': hashkey,
                    'image_url': image_url
                }
                return render(request, 'register.html', context)
        else:
            errors = form.errors
            result = refresh_captcha_hashkey_image_url()
            hashkey = result['hashkey']
            image_url = captcha_image_url(hashkey)
            context = {
                'form': form,
                'errors': errors,
                'hashkey': hashkey,
                'image_url': image_url
            }
            return render(request, 'register.html', context)

    if request.method == 'GET':
        form = RegisterForm()
        result = refresh_captcha_hashkey_image_url()
        hashkey = result['hashkey']
        image_url = captcha_image_url(hashkey)
        context = {
            'form': form,
            'image_url': image_url,
            'hashkey': hashkey
        }
        return render(request, 'register.html', context)


# 登录视图
@cache_page(60 * 15)
def login(request):
    # 不允许重复登录
    if request.session.get('is_login', False):
        messages.info(request, '您已登录，点击确认进入招领页面')
        return redirect(to='/found/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == User.objects.get(username=data['username']).password:
                request.session['username'] = data['username']
                request.session['is_login'] = True
                if request.POST.get('remember_password', False):
                    # 用户点击记住密码开关，登录状态保持两周（默认）
                    pass
                else:
                    # 用户如果没点击记住密码开关，那么登录状态会在浏览器关闭时失效
                    request.session.set_expiry(value=0)
                return redirect(to='/found/')
            else:
                errors = form.errors
                errors['password'] = '密码错误'
                return render(request, 'login.html', {'form': form, 'errors': errors})
        else:
            errors = form.errors
            return render(request, 'login.html', {'form': form, 'errors': errors})

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


# 注销视图
def logout(request):
    if not request.session.get('is_login', False):
        return redirect(to='/home/')

    request.session.flush()
    messages.success(request, '注销成功')
    return redirect(to='/home/')


# 修改密码视图
def change(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.session.get('username'))
        except User.DoesNotExist:
            messages.error(request, '您尚未登录，请登录')
            return redirect(to='/accounts/login/')
        else:
            form = ChangeForm(request.POST)
            if form.is_valid():
                if user.password == form.cleaned_data['old_password']:
                    user.password = form.cleaned_data['new_password']
                    user.save()
                    request.session['is_login'] = False
                    request.session['username'] = None
                    messages.success(request, '密码修改成功，请重新登录')
                    return redirect(to='/accounts/login/')
                else:
                    errors = form.errors
                    errors['old_password'] = '密码错误'
                    return render(request, 'change.html', {'form': form, 'errors': errors})
            else:
                errors = form.errors
                return render(request, 'change.html', {'form': form, 'errors': errors})

    if request.method == 'GET':
        form = ChangeForm()
        return render(request, 'change.html', {'form': form})


# 忘记密码视图
def forget(request):
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # 验证码是否正确
            if email_captcha == data['captcha']:
                user = User.objects.get(email=data['email'])
                user.password = data['password']
                user.save()
                messages.success(request, '密码修改成功，请重新登录')
                return redirect(to='/accounts/login/')
            else:
                errors = form.errors
                errors['captcha'] = '验证码错误，请重试'
                return render(request, 'forget.html', {'form': form, 'errors': errors})
        else:
            errors = form.errors
            return render(request, 'forget.html', {'form': form, 'errors': errors})

    if request.method == 'GET':
        form = ForgetForm()
        return render(request, 'forget.html', {'form': form})


# 生成新图片验证码的哈希值和图片
def refresh_captcha_hashkey_image_url():
    result = {}
    result['hashkey'] = CaptchaStore.generate_key()
    result['image_url'] = captcha_image_url(result['hashkey'])
    return result


# ajax异步刷新图片验证码
def refresh_captcha(request):
    to_json_response = {}
    to_json_response['status'] = 1
    result = refresh_captcha_hashkey_image_url()
    to_json_response.update(result)
    return JsonResponse(to_json_response)


# 生成六位随机数字验证码
def generate_captcha():
    choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    captcha = ''
    for item in range(6):
        captcha += random.choice(choices)
    return captcha


# 发送验证码电子邮件
def send_email(email, captcha):
    msg = '验证码:' + captcha + '，请及时进行验证。(如非本人操作，请忽略本条邮件。)'
    send_mail(
        subject='Lost $ Found 身份验证',
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


# ajax异步发送邮件验证码
def send_captcha(request):
    response = {}
    email = request.POST.get('email')

    # 验证邮箱是否有效
    is_valid = re.fullmatch(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email)
    if not is_valid:
        response['email'] = '邮箱格式不正确'
    else:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response['email'] = '邮箱不存在'
        else:
            global email_captcha
            email_captcha = generate_captcha()
            send_email(email, email_captcha)
            response['status'] = 1
    return JsonResponse(response)


# 获得所有省份
def get_provinces():
    provinces = []
    for key, value in PROVINCE:
        provinces.append(value)
    return provinces


# 获得省份对应的键
def get_province_key(province):
    for key, value in PROVINCE[1:]:
        if province == value:
            return key
    return None


# ajax异步获得省份对应的所有城市
def get_cities(request):
    cities = {}
    province = request.POST.get('province', None)
    if province == '北京市' or province == '上海市' or province == '重庆市' or province == '天津市' or province == '香港特别行政区' or province == '澳门特别行政区':
        cities[province] = province
    else:
        province_key = get_province_key(province)
        for key, value in CITY[province_key]:
            cities[value] = value
    return JsonResponse(cities)


# 检查upload表单数据是否有效
def clean_upload(post, errors):
    category = post.get('category', None)
    date = post.get('date', None)
    province = post.get('province', None)
    city = post.get('city', None)
    detail = post.get('detail', None)
    image = post.get('image', None)

    if category == '---请选择---':
        errors['category'] = '请选择种类'
    if not date:
        errors['date'] = '请选择日期'
    if date and date > datetime.date.today().strftime('%Y-%m-%d'):
        errors['date'] = '不能晚于当前日期'
    if province == '---请选择---':
        errors['province'] = '请选择省份'
    if not city:
        errors['city'] = '请选择城市'
    if not detail:
        errors['detail'] = '请输入详细信息'
    if detail and len(detail) > 100:
        errors['detail'] = '详细信息最多100个字符'

    for error in errors:
        if errors[error]:
            return False
    return True


def clean_filter(post, errors):
    category = post.get('category', None)
    province = post.get('province', None)
    city = post.get('city', None)

    if category == '---请选择---':
        errors['category'] = '请选择种类'
    if province == '---请选择---':
        errors['province'] = '请选择省份'
    if not city:
        errors['city'] = '请选择城市'

    for error in errors:
        if errors[error]:
            return False
    return True


# 筛选启事信息列表
def filter_list(request, lost):
    category = request.POST.get('category')
    province = request.POST.get('province')
    city = request.POST.get('city')

    objects = Object.objects.filter(category=category, province=province, city=city, lost=lost)
    return objects


