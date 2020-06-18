import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

    send_mail(
        '来自www.shaneblog.com的测试邮件',
        '欢迎访问www.shaneblog.com，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！',
        '1340633154@qq.com',
        ['jasmine246875@126.com'],
    )