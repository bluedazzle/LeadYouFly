from django.http import HttpResponse


def alipay_notify(req):
    print req.body
    print req.GET
    print req.POST
    return HttpResponse('success')
