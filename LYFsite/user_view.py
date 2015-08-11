from views import *


def user_message(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    return_content['is_login'] = True

    test_list = range(0, 6)
    return_content['test_list'] = test_list
    return render_to_response('user/message.html',
                              return_content,
                              context_instance=RequestContext(request))


def complete_mes(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
    return_content['is_login'] = True
    student_active = return_content['active_user']

    if request.method == 'GET':
        if student_active.qq and student_active.yy and student_active.phone:
            return HttpResponseRedirect('/user/my_orders')
        else:
            return render_to_response('user/complete_mes.html',
                                      return_content,
                                      context_instance=RequestContext(request))
    if request.method == 'POST':
        form = CompleteInfo(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            student_active.qq = form_data['qq']
            student_active.yy = form_data['yy']
            student_active.phone = form_data['phone']
            student_active.save()
            return HttpResponse(json.dumps('success'))
        return HttpResponse(json.dumps('wrong form'))


def my_orders(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    return_content['is_login'] = True
    if request.method == 'GET':
        test_list = range(0, 3)
        return_content['test_list'] = test_list
        return render_to_response('user/my_order.html',
                                  return_content,
                                  context_instance=RequestContext(request))