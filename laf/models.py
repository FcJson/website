from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# 用户信息表
class User(models.Model):
    username = models.CharField(
        max_length=20,
        unique=True
    )
    gender = models.CharField(max_length=8)
    age = models.CharField(max_length=3)
    phone_number = models.CharField(
        max_length=11,
        unique=True
    )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username


# 物品信息表
class Object(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=5)
    date = models.DateField()
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    image = ProcessedImageField(
        upload_to='img',
        processors=[ResizeToFill(192, 156)],
        options={'quality': 60},
        blank=True,
        null=True
    )
    detail = models.CharField(max_length=100)
    # lost用来划分是丢东西(True)还是捡到东西(False)
    lost = models.BooleanField(default=True)

    def __str__(self):
        return self.detail

    class Meta:
        ordering = ['-date']

