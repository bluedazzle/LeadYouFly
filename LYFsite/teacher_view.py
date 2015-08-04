from views import *


def teacher_host(request):
    return render_to_response('teacher/teacher_host.html')


def teacher_contact(request):
    return render_to_response('teacher/contact.html')


def teacher_indemnity(request):
    test_list = []
    for i in range(0, 5):
        test_dic = {'test_date': datetime.datetime.utcnow(),
                    'test_number': 290,
                    'test_pay': 356}
        test_list.append(test_dic)
    return render_to_response('teacher/indemnity.html', {'test_list': test_list})


def order_accept(request):
    test_list = range(0, 4)
    return render_to_response('teacher/order_accept.html', {'test_list': test_list})


def manage_courses(request):
    test_list = range(0, 3)
    return render_to_response('teacher/manage_courses.html', {'test_list': test_list})


def teacher_video_upload(request):
    test_list = range(0, 3)
    return render_to_response('teacher/video_upload.html', {'test_list': test_list})