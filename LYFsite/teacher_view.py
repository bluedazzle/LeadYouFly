# -*- coding: utf-8 -*-
from views import *
from LYFAdmin.qn import *


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
        return_content['all_heroes'] = Hero.objects.all()
        return render_to_response('teacher/teacher_host.html',
                                  return_content,
                                  context_instance=RequestContext(request))


def change_mentor_status(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404

    if request.method == 'GET':
        status = request.GET.get('status')
        mentor = return_content['mentor']
        if int(status) == 1:
            if mentor.status == 0 or mentor.status == 1:
                mentor.status = 1
                mentor.save()
                return HttpResponse(json.dumps("success"))
            else:
                return HttpResponse(json.dumps("failed"))
        elif int(status) == 0:
            if mentor.status == 2:
                return HttpResponse(json.dumps('failed'))
            else:
                mentor.status = 0
                mentor.save()
                return HttpResponse(json.dumps("success"))


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
    if request.method == 'GET':
        mentor = return_content['mentor']
        return_content['money_records'] = mentor.men_money_records.order_by('-create_time').all()
    return render_to_response('teacher/indemnity.html',
                              return_content,
                              context_instance=RequestContext(request))


def order_accept(request):
    return_content = utils.is_login(request)
    if not return_content:
        return HttpResponseRedirect('/login')
    if not return_content['login_type'] == 'teacher':
        raise Http404

    if request.method == 'GET':
        return render_to_response('teacher/order_accept.html',
                                  return_content,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        mentor = return_content['mentor']
        if not mentor.status == 1:
            return HttpResponse(json.dumps(u'请先更改状态为可立即授课'))
        try:
            order = Order.objects.get(order_id=order_id)
            if order.status == 1:
                order.status = 2
                order.save()
                return HttpResponse(json.dumps('success'))
            else:
                return HttpResponse(json.dumps('failed'))
        except Order.DoesNotExist:
            raise Http404
        except:
            return HttpResponse(json.dumps('wrong form'))


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
    if request.method == 'GET':
        return render_to_response('teacher/video_upload.html',
                                  return_content,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        video_format = ['mp4', 'flv', 'avi', 'rmvb', 'webm', 'ogg']
        support_format = ['mp4', 'webm', 'ogg']
        video_data = request.FILES.get('new_video', None)
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id)
            t = order.id
        except Order.DoesNotExist:
            return HttpResponse(json.dumps('wrong order id'))

        if video_data is not None:
            res = utils_upload_video(video_data, video_format, order_id, support_format)
            if res:
                order.if_upload_video = True
                order.video_url = QINIU_DOMAIN + res['sfile_name']
                order.video_poster = QINIU_DOMAIN + res['poster_name']
                order.video_name = res['sfile_name']
                order.video_size = video_data.size
                order.save()
                return HttpResponse(json.dumps('success'))
            else:
                return HttpResponse(json.dumps('failed'))
        else:
            return HttpResponse(json.dumps('no video'))


def utils_upload_video(video_data, video_format, order_id, support_format):
    file_name, ext_name = video_data.name.encode('utf-8').split('.')
    if ext_name in video_format:
        upload_name = file_name + '_' + str(order_id) + '.' + ext_name
        progress_handler = lambda progress, total: progress
        sign = 'video_order' + str(order_id)
        res, sfile_name = put_block_data(upload_name, video_data, progress_handler=progress_handler,
                                         sign=sign)
        if res:
            poster_name = sfile_name.encode('utf-8').split('.')[0] + '_poster.jpg'
            res, info = data_handle(sfile_name, poster_name, VIDEO_POSTER_PARAM)
            if ext_name not in support_format:
                new_name = sfile_name.encode('utf-8').split('.')[0] + '.mp4'
                res, info = data_handle(sfile_name, new_name, VIDEO_CONVERT_PARAM)
                delete_data(sfile_name.encode('utf-8'))
                sfile_name = new_name
                return {'poster_name': poster_name,
                        'sfile_name': sfile_name}

        return False