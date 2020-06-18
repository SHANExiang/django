from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('male', '男'),
        ('femal', '女')
    )

    name = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=256, choices=gender, default='男')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    


