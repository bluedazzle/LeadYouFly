from views import *


def user_message(request):
    test_list = range(0, 3)
    return render_to_response('user/message.html', {'test_list': test_list})


def complete_mes(request):
    return render_to_response('user/complete_mes.html')


def my_order(request):
    test_list = range(0, 3)
    return render_to_response('user/my_order.html', {'test_list': test_list})