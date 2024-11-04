from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Usuarios

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuarios

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'cpf']

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('some_extra_data',)}),
    )


admin.site.register(Usuarios, MyUserAdmin)