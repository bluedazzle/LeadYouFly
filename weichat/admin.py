from django.contrib import admin
from weichat.models import WeChatAdmin, Promotion, Channel, Question, Reward

# Register your models here.

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['nick', 'create_time']
    search_fields = ['nick', 'sex']
    ordering = ('-create_time',)

admin.site.register(WeChatAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Channel)
admin.site.register(Question)
admin.site.register(Reward)