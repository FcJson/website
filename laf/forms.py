from django import forms
from captcha.fields import CaptchaField
from laf.models import User
from django.core.validators import RegexValidator


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=20,
        min_length=4,
        error_messages={
            'required': '请输入用户名',
            'max_length': '用户名最多20个字符',
            'min_length': '用户名最少4个字符'
        },
        widget=forms.TextInput()
    )

    gender = forms.CharField(
        required=True,
        error_messages={
            'required': '请输入性别'
        },
        widget=forms.TextInput()
    )

    age = forms.CharField(
        required=True,
        error_messages={
            'required': '请输入年龄'
        },
        widget=forms.TextInput()
    )

    phone_number = forms.CharField(
        required=True,
        max_length=11,
        min_length=11,
        error_messages={
            'required': '请输入电话号码',
            'max_length': '电话号码过长',
            'min_length': '电话号码过短'
        },
        widget=forms.TextInput(),
        validators=[RegexValidator(r'^1[3578]\d{9}$', '电话号码格式不正确'),]
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
        error_messages={
            'required': '请输入邮箱'
        },
        validators=[RegexValidator(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', '邮箱格式不正确'), ]
    )

    password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请输入密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput(),
    )

    re_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请确认密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput(),
    )

    captcha = CaptchaField(
        error_messages={
            'invalid': '验证码错误',
            'required': '请输入图片验证码'
        }
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        gender = self.cleaned_data.get('gender')
        age = self.cleaned_data.get('age')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        phone_number = self.cleaned_data.get('phone_number')
        email = self.cleaned_data.get('email')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                self.errors['username'] = '用户名已存在'
        if gender and gender not in {'男', '女'}:
            self.errors['gender'] = '性别只能为男或女'
        if age and not age.isdigit():
            self.errors['age'] = '年龄只能是数字'
        if phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                pass
            else:
                self.errors['phone_number'] = '手机号已被注册'
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                self.errors['email'] = '邮箱已被注册'
        if password and re_password and password != re_password:
            self.errors['re_password'] = '密码不一致，请重试'


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=20,
        min_length=4,
        error_messages={
            'required': '请输入用户名',
            'max_length': '用户名最多20个字符',
            'min_length': '用户名最少4个字符'
        },
        widget=forms.TextInput()
    )

    password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请输入密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.errors['username'] = '用户名不存在'
            else:
                return username


# 修改密码表单
class ChangeForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请输入原密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput()
    )

    new_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请输入新密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput()
    )

    re_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请确认密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput()
    )

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        re_password = self.cleaned_data.get('re_password')

        if new_password and re_password and new_password != re_password:
            self.errors['re_password'] = '密码不一致，请重试'


# 忘记密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
        error_messages={'required': '请输入邮箱'},
        validators=[RegexValidator(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', '邮箱格式不正确'), ]
    )

    captcha = forms.CharField(
        required=True,
        error_messages={'required': '请输入验证码'},
        widget=forms.TextInput()
    )

    password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请输入密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput(),
    )

    re_password = forms.CharField(
        required=True,
        max_length=16,
        min_length=6,
        error_messages={
            'required': '请确认密码',
            'max_length': '密码最多16个字符',
            'min_length': '密码最少6个字符'
        },
        widget=forms.PasswordInput(),
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.errors['email'] = '邮箱不存在'
        if password and re_password and password != re_password:
            self.errors['re_password'] = '密码不一致，请重试'


