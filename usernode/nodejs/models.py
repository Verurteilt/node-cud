from django.db import models
from django.contrib.auth.models import AbstractBaseUser, _user_has_perm
######################################

from .managers import NodeUserManager


class NodeUser(AbstractBaseUser):

    def image(self, filename):
        upload_to = "ProfilePictures/%s/%s" % (self.first_name, filename)
        return upload_to

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True)
    birth = models.DateField(null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    consumer_key = models.CharField(max_length=100, null=True, blank=True)
    consumer_secret = models.CharField(max_length=100, null=True, blank=True)
    access_token = models.CharField(max_length=100, null=True, blank=True)
    access_token_secret = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to=image, null=True)

    objects = NodeUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['twitter',  'first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Tweet(models.Model):
    message = models.TextField(max_length=140)
    user = models.ForeignKey(NodeUser)
