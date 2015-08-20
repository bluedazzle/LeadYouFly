# -*- coding: utf-8 -*-
from views import *


def user_message(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404
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
    student_active = return_content['active_user']

    if request.method == 'GET':
        return render_to_response('user/complete_mes.html',
                                  return_content,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = CompleteInfoForm(request.POST)
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

    if request.method == 'GET':
        orders = Order.objects.order_by('-create_time').filter(belong=return_content['active_user'])
        return_content['orders'] = orders
        return render_to_response('user/my_order.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def appraise_order(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        try:
            order = Order.objects.get(id=order_id,
                                      status=3)
            return_content['order'] = order
            return render_to_response('user/appraise.html',
                                      return_content,
                                      context_instance=RequestContext(request))
        except Order.DoesNotExist:
            raise Http404
        except:
            raise Http404

    if request.method == 'POST':
        form = AppraiseOrder(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
        else:
            return HttpResponse(json.dumps("wrong form"))

        try:
            order = Order.objects.get(id=form_data['order_id'],
                                      belong=return_content['active_user'],
                                      status=3)
            new_comment = Comment()
            new_comment.mark = float(form_data['stars'])
            new_comment.content = form_data['content']
            new_comment.comment_mentor = order.teach_by
            new_comment.comment_by = return_content['active_user']
            new_comment.save()
            order.status = 4
            order.save()
        except Order.DoesNotExist:
            raise Http404
        except:
            return HttpResponse(json.dumps("wrong request"))
        return HttpResponse("success")


def my_follow_mentors(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        return render_to_response('user/follow_mentor.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def follow_mentor(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        mentor_id = request.GET.get('mentor_id')
        student_active = return_content['active_user']
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            if student_active.follow.filter(id=mentor_id).count() == 0:
                student_active.follow.add(mentor)
            else:
                raise Http404
        except Mentor.DoesNotExist:
            raise Http404

        return HttpResponse(json.dumps(mentor_id))


def cancel_follow(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'student':
        raise Http404

    if request.method == 'GET':
        mentor_id = request.GET.get('mentor_id')
        student_active = return_content['active_user']
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            if not student_active.follow.filter(id=mentor_id).count() == 0:
                student_active.follow.remove(mentor)
            else:
                raise Http404
        except Mentor.DoesNotExist:
            raise Http404

        return HttpResponse(json.dumps(mentor_id))


def confirm_order(request):
    return_content = utils.is_login(request)
    if return_content and return_content['login_type'] == 'student':
        return_content['is_login'] = True
    else:
        return HttpResponseRedirect('/login')

    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        if not course_id:
            raise Http404
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise Http404
        return_content['course'] = course
        return render_to_response('common/confirm_order.html',
                                  return_content,
                                  context_instance=RequestContext(request))