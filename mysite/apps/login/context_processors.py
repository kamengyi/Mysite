# -*- coding:utf-8
from .models import User


def current_user(request):
    '''
    创建模板全局变量
    '''
    try:
        current_user = User.objects.get(id=request.session.get('user_id', None))
    # 用户不存在, 抛出DoesNotExist
    except User.DoesNotExist:
        current_user = None

    return {
        'current_user': current_user
    }

