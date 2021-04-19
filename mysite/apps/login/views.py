import datetime
import hashlib
from .models import User, ConfirmString
from .forms import LoginForm, RegisterForm
from django.conf import settings
from django.shortcuts import render, redirect
from apps.article.models import Article

# Create your views here.

def index(request):
    try:
        article_list = Article.objects.all()
    except Exception:
        print(Exception)
        article_list = []

    return render(request, 'login/index.html', locals())


# 邮箱验证完成后即跳转到首页
def login_redirect(request):
    if request.session.get('is_login', None):
        redirect('/index/')


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    # update()方法需要byte类型参数
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(user=user, code=code)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = "测试邮箱验证功能"
    text_content = "邮箱验证功能文本内容, 若收到此内容, 说明邮箱不支持HTML链接功能, 请联系管理员"
    html_content = '''
                   邮箱验证功能HTML内容, 跳转验证<a href='http://{}/confirm/?code={}'>链接</a>
                   <p>此链接有效期是{}天</p>
                   '''.format('192.168.188.201:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def logout(request):
    # 删除request.seesion信息
    request.session.flush()
    return redirect('/index/')


def user_confirm(request):
    code = request.GET.get('code', None)

    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    created = confirm.created
    now = datetime.datetime.now()
    if now > created + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期了, 请重新注册'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢确认, 请登录!"
        return render(request, 'login/confirm.html', locals())


def login(request):
    login_redirect(request)

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        message = '请检查输入内容'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
            except:
                message = '用户不存在'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '请先验证邮箱再登录！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('/index/')
            else:
                message = '密码错误'
                return render(request, 'login/login.html', locals())
        else:
            print(login_form.errors.as_data())
            return render(request, 'login/login.html', locals())

    login_form = LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    login_redirect(request)

    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        message = '请检查输入内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if password1 != password2:
                message = '两次输入密码不一致'
                return render(request, 'login/register.html', locals())
            else:
                same_user = User.objects.filter(username=username)
                if same_user:
                    message = '用户名已存在'
                    return render(request, 'login/register.html', locals())
                
                same_email = User.objects.filter(email=email)
                if same_email:
                    message = '该邮箱已被注册'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.username = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                
                code = make_confirm_string(new_user)
                send_email(email, code)
                message = "请前往邮箱确认!"

                return render(request, 'login/register.html', locals())
        else:
            return render(request, 'login/register.html', locals())

    register_form = RegisterForm()

    return render(request, 'login/register.html', locals())

