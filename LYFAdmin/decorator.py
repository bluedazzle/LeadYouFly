from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect
from LYFAdmin.models import Admin
from functools import wraps

def login_require(func):
    def exect(*args, **kw):
        req = args[0]
        token = req.session.get('token', None)
        if token is None or token == '':
            return HttpResponseRedirect('/admin/')
        else:
            admin = Admin.objects.filter(token=token)
            if not admin.exists():
                return HttpResponseRedirect('/admin/')
        res = func(*args, **kw)
        return res
    return exect