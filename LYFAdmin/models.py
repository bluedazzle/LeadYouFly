# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import get_current_timezone
import datetime
import hashlib
# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
            abstract = True


class MentorManager(BaseUserManager):
    def create_user(self, email, phone, passwd=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = MentorManager.normalize_email(email),
            username = phone,
        )

        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, passwd):

        user = self.create_user(email,
            username = phone,
            password = passwd,

        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = False
        user.save(using=self._db)
        return user


class AdminManager(BaseUserManager):
    def create_user(self, email, phone, passwd=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = MentorManager.normalize_email(email),
            username = phone,
        )

        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, passwd):

        user = self.create_user(email,
            username = phone,
            password = passwd,

        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = False
        user.save(using=self._db)
        return user


class StudentManager(BaseUserManager):
    def create_user(self, email, phone, passwd=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = MerchantManager.normalize_email(email),
            username = phone,
        )

        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, passwd):

        user = self.create_user(email,
            username = phone,
            password = passwd,

        )
        user.is_staff = True
        user.is_active = True
        user.is_admin = False
        user.save(using=self._db)
        return user


class Hero(BaseModel):
    hero_name = models.CharField(max_length=50)
    hero_picture = models.CharField(max_length=200, default=' ')
    hero_background = models.CharField(max_length=200, default='')
    hero_type = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return self.hero_name


class Admin(AbstractBaseUser, BaseModel):
    account = models.CharField(max_length=13, unique=True)
    nick = models.CharField(max_length=20, default='admin')
    token = models.CharField(max_length=64, unique=True)

    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['account']
    objects = AdminManager()

    def __unicode__(self):
        return self.account

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.passwd
        else:
            return hashlib.md5(password).hexdigest()

    # def check_password(self, password):
    #     if self.hashed_password(password) == self.password:
    #         return True
    #     return False


class Mentor(AbstractBaseUser, BaseModel):
    account = models.CharField(max_length=11, unique=True)
    nick = models.CharField(max_length=20, null=True, blank=True, default="Mentor")
    real_name = models.CharField(max_length=50, default='', null=True, blank=True)
    alipay_account = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.IntegerField(default=3)
    intro = models.CharField(max_length=100, default='')
    good_at = models.CharField(max_length=5, default='')
    game_level = models.CharField(max_length=8, default='')
    teach_area = models.CharField(max_length=20, default='0')
    qq = models.CharField(max_length=20, default='')
    yy = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=11, default='')
    intro_detail = models.TextField(default='')
    avatar = models.CharField(max_length=200, default='/img/default_mentor.jpg')
    intro_video = models.CharField(max_length=200, default='')
    have_intro_video = models.BooleanField(default=False)
    intro_picture = models.CharField(max_length=200, default='/img/default_mentor.jpg')
    video_poster = models.CharField(max_length=200, default='')
    expert_hero1 = models.ForeignKey(Hero, related_name='who_expert1', null=True, blank=True, on_delete=models.SET_NULL)
    expert_hero2 = models.ForeignKey(Hero, related_name='who_expert2', null=True, blank=True, on_delete=models.SET_NULL)
    expert_hero3 = models.ForeignKey(Hero, related_name='who_expert3', null=True, blank=True, on_delete=models.SET_NULL)
    hero_list = models.ManyToManyField(Hero, related_name='who_uses', null=True, blank=True)
    id_picture = models.CharField(max_length=100, default='')
    total_income = models.FloatField(default=0.0)
    iden_income = models.FloatField(default=0.0)
    cash_income = models.FloatField(default=0.0)
    commission = models.FloatField(default=0.0)
    mark = models.FloatField(default=0.0)
    freeze = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    disabled = models.BooleanField(default=False)


    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['account']
    objects = MentorManager()

    def __unicode__(self):
        return self.account

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.passwd
        else:
            return hashlib.md5(password).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    def set_password(self, password):
        self.password = self.hashed_password(password)

    def get_orders_count(self):
        orders = self.men_orders.exclude(status=5).exclude(status=6)
        orders_count = orders.count()
        return orders_count

    def get_comment_list(self):
        return self.men_comments.all().order_by('-create_time')

class Student(AbstractBaseUser, BaseModel):
    account = models.CharField(max_length=64, unique=True)
    nick = models.CharField(max_length=20, null=True, blank=True, default="Mentor")
    rank = models.IntegerField(default=1)
    qq = models.CharField(max_length=20, null=True, blank=True, default='')
    yy = models.CharField(max_length=50, null=True, blank=True, default='')
    phone = models.CharField(max_length=11, null=True, blank=True, default='')
    avatar = models.CharField(max_length=200, default='/img/avatar/1.png')
    money = models.FloatField(default=0.0)
    exp = models.IntegerField(default=0)
    follow = models.ManyToManyField(Mentor, related_name='my_students', null=True, blank=True)
    wx_open_id = models.CharField(max_length=128, default='')
    wx_union_id = models.CharField(max_length=123, default='', null=True, blank=True)
    qq_open_id = models.CharField(max_length=128, default='')
    # bind_qq = models.BooleanField(default=False)
    # bind_wechat = models.BooleanField(default=False)


    USERNAME_FIELD = 'account'
    REQUIRED_FIELDS = ['account']
    objects = StudentManager()

    def __unicode__(self):
        return self.account

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.passwd
        else:
            return hashlib.md5(password).hexdigest()


class Message(BaseModel):
    content = models.CharField(max_length=500)
    belong = models.ForeignKey(Student, related_name='stu_messages', null=True, blank=True, on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)
    send_all = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content


class Course(BaseModel):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    course_info = models.CharField(max_length=500, default='')
    belong = models.ForeignKey(Mentor, related_name='men_courses')

    def __unicode__(self):
        return '{0}:{1}'.format(self.belong.nick, self.name)


#教练账款纪录
class MoneyRecord(BaseModel):
    record_id = models.CharField(max_length=30, unique=True)
    action = models.CharField(max_length=8, default='')
    income = models.FloatField(default=0.0)
    type = models.BooleanField(default=True)
    info = models.CharField(max_length=200, default='')
    belong = models.ForeignKey(Mentor, related_name='men_money_records', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.action


class Lesson(BaseModel):
    name = models.CharField(max_length=50)
    intro = models.TextField(default='')
    cover = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name

    def get_comments(self):
        return self.les_comments.all().order_by('-create_time')


class Comment(BaseModel):
    mark = models.FloatField(default=0.0)
    content = models.CharField(max_length=50000, default='')
    comment_by = models.ForeignKey(Student, related_name='stu_comments', null=True, blank=True, on_delete=models.SET_NULL)
    comment_mentor = models.ForeignKey(Mentor, related_name='men_comments', null=True, blank=True, on_delete=models.SET_NULL)
    comment_lesson = models.ForeignKey(Lesson, related_name='les_comments', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.content


class CourseClass(BaseModel):
    limit_number = models.IntegerField(default=10)
    apply_number = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default='')
    price = models.FloatField(default=0.0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_time = models.DateTimeField()
    lesson = models.ForeignKey(Lesson, related_name='cls_les', on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_apply_number(self):
        number = Order.objects.filter(order_type=2, class_info=self).exclude(status=5).exclude(status=6).count()
        self.apply_number = number
        self.save()
        return number


class Order(BaseModel):
    order_type_dict = {(1, u'教练订单'),
                       (2, u'课程订单')}

    order_id = models.CharField(max_length=28, unique=True)
    order_price = models.FloatField(default=0.0)
    order_type = models.IntegerField(default=1, choices=order_type_dict)
    pay_type = models.IntegerField(default=1)
    course_name = models.CharField(max_length=50, default='')
    course_intro = models.CharField(max_length=500, default='')
    learn_area = models.CharField(max_length=30, default='')
    learn_type = models.CharField(max_length=10, default='')
    learn_hero = models.CharField(max_length=20, default='')
    status = models.IntegerField(default=6)
    teach_video = models.CharField(max_length=200, default='')
    video_name = models.CharField(max_length=200, default='')
    video_size = models.FloatField(default=0)
    video_url = models.CharField(max_length=200, default='')
    video_poster = models.CharField(max_length=200, default='')
    if_upload_video = models.BooleanField(default=False)
    video_audit = models.BooleanField(default=False)
    video_pass = models.NullBooleanField(default=None)
    teach_long = models.FloatField(default=1.5)
    teach_start_time = models.DateTimeField(null=True, blank=True)
    teach_end_time = models.DateTimeField()
    belong = models.ForeignKey(Student, related_name='stu_orders')
    teach_by = models.ForeignKey(Mentor, related_name='men_orders', null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, related_name='comment_order', null=True, blank=True, on_delete=models.SET_NULL)
    if_pay = models.BooleanField(default=False)
    mentor_money = models.FloatField(default=0.0)
    platform_money = models.FloatField(default=0.0)

    lesson = models.ForeignKey(Lesson, related_name='ord_les', on_delete=models.SET_NULL, null=True, blank=True)
    class_info = models.ForeignKey(CourseClass, related_name='ord_cls', on_delete=models.SET_NULL, null=True, blank=True)




    def __unicode__(self):
        return self.order_id


class PayInfo(BaseModel):
    order = models.OneToOneField(Order, related_name='info_order')
    pay_id = models.CharField(max_length=64, default='')
    buyer_email = models.CharField(max_length=100, default='')
    status_info = models.CharField(max_length=30, default='')
    price = models.FloatField(default=0)

    def __unicode__(self):
        return self.pay_id


class IndexAdmin(models.Model):
    rec_mentor1 = models.ForeignKey(Mentor, blank=True, null=True, related_name='ind_rec_1', on_delete=models.SET_NULL)
    rec_mentor2 = models.ForeignKey(Mentor, blank=True, null=True, related_name='ind_rec_2', on_delete=models.SET_NULL)
    rec_mentor3 = models.ForeignKey(Mentor, blank=True, null=True, related_name='ind_rec_3', on_delete=models.SET_NULL)
    rec_mentor4 = models.ForeignKey(Mentor, blank=True, null=True, related_name='ind_rec_4', on_delete=models.SET_NULL)
    index_pic1 = models.CharField(max_length=500, default=' ')
    index_pic2 = models.CharField(max_length=500, default=' ')
    index_pic3 = models.CharField(max_length=500, default=' ')
    index_video = models.CharField(max_length=500, default='')
    video_poster = models.CharField(max_length=500, default='')

    def __unicode__(self):
        return unicode(self.id)

#投诉
class Report(BaseModel):
    reporter = models.ForeignKey(Student, related_name='stu_reports')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    qq = models.CharField(max_length=30, null=True, blank=True)
    reported = models.CharField(max_length=30)
    type = models.IntegerField(default=0)
    finish = models.BooleanField(default=False)
    content = models.CharField(max_length=1000, default='')
    pic1 = models.CharField(max_length=200, default='')
    pic2 = models.CharField(max_length=200, default='')
    pic3 = models.CharField(max_length=200, default='')
    pic4 = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return self.name

#学生充值纪录
class ChargeRecord(BaseModel):
    record_id = models.CharField(max_length=30, unique=True)
    charge_number = models.FloatField(default=0.0)
    note = models.CharField(max_length=200, default='')
    belong = models.ForeignKey(Student, related_name='stu_charge_recs')

    def __unicode__(self):
        return self.record_id

#教练提现请求纪录
class CashRecord(BaseModel):
    record_id = models.CharField(max_length=30, unique=True)
    money = models.FloatField(default=0.0)
    alipay_account = models.CharField(max_length=50)
    real_name = models.CharField(max_length=100)
    belong = models.ForeignKey(Mentor, related_name='men_cash_recs')
    manage = models.BooleanField(default=False)
    agree = models.NullBooleanField(default=None)
    success = models.NullBooleanField(default=None)
    info = models.CharField(max_length=500, default='')

    def __unicode__(self):
        return self.record_id + '|' + self.alipay_account


class PhoneVerify(BaseModel):
    phone = models.CharField(max_length=11)
    verify = models.IntegerField(default=0)

    def __unicode__(self):
        return self.phone

    def is_current(self, verify_code):
        if int(verify_code) == self.verify:
            return True
        else:
            return False

    def is_get_again(self):
        time_now = datetime.datetime.now(tz=get_current_timezone())
        time_delta = datetime.timedelta(seconds=30)
        if time_now - self.modify_time >= time_delta:
            return True
        else:
            return False

    def is_expire(self):
        time_now = datetime.datetime.now(tz=get_current_timezone())
        time_delta = datetime.timedelta(minutes=10)
        if time_now - self.modify_time >= time_delta:
            return True
        else:
            return False


class Notice(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField(default='')

    def __unicode__(self):
        return self.title


class Coupon(BaseModel):
    type_dict = {(1, u'注册赠送'),
                 (2, u'邀请注册赠送'),
                 (3, u'系统赠送')}
    money = models.FloatField(default=0.0)
    type = models.IntegerField(max_length=1, default=1, choices=type_dict)
    info = models.CharField(max_length=500, default='')
    use = models.BooleanField(default=False)
    expire = models.DateField()
    belong = models.ForeignKey(Student, related_name='stu_coupons')

    def __unicode__(self):
        return u'{0}:{1}元'.format(self.belong.account, self.money)

