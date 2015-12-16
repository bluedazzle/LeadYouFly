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
    province = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=20, default='')
    sex = models.CharField(max_length=10, default='')
    reply = models.TextField(default='')
    play = models.BooleanField(default=False)
    qq = models.CharField(max_length=30, default='')

    def __unicode__(self):
        return self.nick


class Question(BaseModel):
    question = models.CharField(max_length=200, default='')
    answer = models.TextField(default='')
    image = models.CharField(max_length=512, default='')
    have_image = models.BooleanField(default=False)

    def __unicode__(self):
        return self.question


class Reward(BaseModel):
    user = models.OneToOneField(Promotion, related_name='user_reward')
    reward = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return '{0}:{1}'.format(self.user.nick, self.reward)


class WechatMessage(BaseModel):
    open_id = models.CharField(max_length=128, default='')
    content = models.TextField(default='')
    nick = models.CharField(max_length=128)

    def __unicode__(self):
        return self.nick