from django.contrib import admin
from weichat.models import WeChatAdmin, Promotion, Channel, Question

# Register your models here.
admin.site.register(WeChatAdmin)
admin.site.register(Promotion)
admin.site.register(Channel)
admin.site.register(Question)