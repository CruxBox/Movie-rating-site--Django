from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Actor, Director, Person, Public_user
from .forms import register_public_user,UserChangeForm
from django.contrib.auth.models import Group


class Person_admin(UserAdmin):
    model = Person
    form = UserChangeForm
    add_form = register_public_user


    list_display = ('username','email','active','staff')
    list_filter = ('username',)
    fieldsets = (
        (None, {'fields':('username','password')}),
        ('Permissions',{'fields':('staff','admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide'),
            'fields':('first_name','last_name','email','phone_no','birth_date','username','password1','password2')}
            ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(Person,Person_admin)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Public_user)
admin.site.unregister(Group)