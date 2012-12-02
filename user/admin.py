from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile,Card,ResvNumber
from fileupload.models import *

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_active' )
    ordering = ('-id',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Card)
admin.site.register(Requirement)
admin.site.register(Order)

admin.site.register(File)
admin.site.register(ResvNumber)