# -*- coding: utf-8 -*-
def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False
