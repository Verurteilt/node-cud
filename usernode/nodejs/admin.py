from .models import NodeUser, Tweet
from .forms import MyUserAdmin
from django.contrib import admin

admin.site.register(NodeUser, MyUserAdmin)
admin.site.register(Tweet)
