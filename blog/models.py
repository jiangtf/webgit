# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
#from .DjangoUeditor.models import UEditorField


# Create your models here.

# 用户模型.
# 第一种：采用的继承方式扩展用户信息（本系统采用）
# 扩展：关联的方式去扩展用户信息
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


# tag（标签）
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 自定义一个文章Model的管理器
# 1、新加一个数据处理的方法
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title

# 年级
class grade(models.Model):
    name = models.CharField(max_length=50, verbose_name='年级')

    class Meta:
        verbose_name = u'年级'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

# 学科
class subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='学科')

    class Meta:
        verbose_name = u'学科'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# grade（年级学科学费）
class grade_course(models.Model):
    grade_name = models.ForeignKey(grade, blank=True, null=True, verbose_name='年级', on_delete=models.CASCADE)

    term_list = (
        (1, '上学期'),
        (2, '下学期'),
    )
    term = models.IntegerField('学期', choices=term_list)

    subject_name = models.ForeignKey(subject, blank=True, null=True, verbose_name='学科', on_delete=models.CASCADE)

    price = models.IntegerField('价格', default=0)

    class Meta:
        verbose_name = '年级学科学费'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #    return self.price

# 标准题库
class nomal_questions(models.Model):
    questions_org = models.ForeignKey(grade_course, verbose_name=u"题目分类", on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u"题目标题",max_length=50)
    type = models.CharField(max_length=50, verbose_name=u"题目类型")
    desc = models.CharField(max_length=300, verbose_name=u"题目选项")
    answer = models.CharField(max_length=300, verbose_name=u"题目答案")
    keypoint = models.CharField(max_length=300, verbose_name=u"知识点", null=True, blank=True)
    point = models.IntegerField(default=0, verbose_name=u'题目分值', blank=True)
    complexity = models.CharField(max_length=300, verbose_name=u"难度", null=True, blank=True)
    show_time = models.DateTimeField( null=True, blank=True,verbose_name=u"题目出现时间")
    add_time = models.DateTimeField( null=True, blank=True, verbose_name=u"添加时间")
    detail =  models.CharField(verbose_name=u"试题解析",max_length=50)

    class Meta:
        verbose_name = u"标准题库"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
