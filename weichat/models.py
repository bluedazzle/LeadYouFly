from django.db import models
from LYFAdmin.models import BaseModel
# Create your models here.
class WeChatAdmin(models.Model):
    app_id = models.CharField(max_length=128, default='')
    app_secret = models.CharField(max_length=128, default='')
    access_token = models.CharField(max_length=1024, default='')

    def __unicode__(self):
        return self.app_id


class Channel(BaseModel):
    name = models.CharField(max_length=256, default='')
    scene = models.CharField(max_length=60, unique=True)
    ticket = models.CharField(max_length=512, default='')
    welcome_text = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')

    def get_channel_promotion(self):
        return self.cnl_pros.all().count()

    def __unicode__(self):
        return self.name


class Promotion(BaseModel):
    open_id = models.CharField(max_length=128, unique=True)
    nick = models.CharField(max_length=512, default='')
    channel = models.ForeignKey(Channel, related_name='cnl_pros', null=True, blank=True)
    cancel = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nick