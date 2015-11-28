from django.contrib import admin
from weichat.models import WeChatAdmin, Promotion, Channel

# Register your models here.
admin.site.register(WeChatAdmin)
admin.site.register(Promotion)
admin.site.register(Channel)