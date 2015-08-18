# -*- coding: utf-8 -*-
from views import *


def teacher_login(request):
    if request.method == 'GET':
        return render_to_response('teacher/teacher_login.html',
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse(json.dumps("wrong forms"))
        teacher_has = Mentor.objects.filter(account=request.POST.get('username'))
        if teacher_has.count() == 0:
            return HttpResponse(json.dumps(u"用户名或者密码错误"))
        if not teacher_has[0].check_password(request.POST.get('password')):
            return HttpResponse(json.dumps(u"用户名或者密码错误"))
        request.session.clear()
        request.session['teacher'] = teacher_has[0].account
        return HttpResponse(json.dumps("success"))


def teacher_host(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    if request.method == 'GET':
        return render_to_response('teacher/teacher_host.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def teacher_contact(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    mentor_active = return_content['mentor']

    if request.method == 'GET':
        return render_to_response('teacher/contact.html',
                                  return_content,
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = MentorContactForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            mentor_active.qq = form_data['qq']
            mentor_active.yy = form_data['yy']
            mentor_active.phone = form_data['phone']
            mentor_active.save()
            return HttpResponse(json.dumps('success'))
        return HttpResponse(json.dumps('wrong form'))


def teacher_indemnity(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    test_list = []
    for i in range(0, 5):
        test_dic = {'test_date': datetime.datetime.utcnow(),
                    'test_number': 290,
                    'test_pay': 356}
        test_list.append(test_dic)
    return render_to_response('teacher/indemnity.html', {'test_list': test_list})


def order_accept(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    return render_to_response('teacher/order_accept.html',
                              return_content,
                              context_instance=RequestContext(request))


def manage_courses(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    mentor_active = return_content['mentor']
    if request.method == 'GET':
        return render_to_response('teacher/manage_courses.html',
                                  return_content,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = UpdateCourseForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
        else:
            return HttpResponse(json.dumps('wrong form'))

        if form_data['id']:
            update_course = Course.objects.get(id=form_data['id'])
            update_course.name = form_data['course_name']
            update_course.price = form_data['course_price']
            update_course.course_info = form_data['course_info']
            update_course.save()
            return HttpResponse(json.dumps('success'))

        else:
            new_course = Course()
            new_course.name = form_data['course_name']
            new_course.price = form_data['course_price']
            new_course.course_info = form_data['course_info']
            new_course.belong = mentor_active
            new_course.save()
            return HttpResponse(json.dumps('success'))




def teacher_video_upload(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404
    test_list = range(0, 3)
    return render_to_response('teacher/video_upload.html', {'test_list': test_list})