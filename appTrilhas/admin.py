from django.contrib import admin
from .models import User, Convite, Trilha, Curso, LinkCurso, User_Link, Trilha_User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from django import forms
from django.forms import Select

ROLE_CHOICES = [('Administrador', 'Administrador'), ('Estudante', 'Estudante'), ('Moderador', 'Moderador')]

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('role',)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget = Select(choices=ROLE_CHOICES, attrs={'class': 'form-control'})


class UserStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff',]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'matricula', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}), ('Pernmissions', {'fields': ('is_staff', 'is_active', 'user_permissions',
                                                                                'last_login', 'date_joined',)}),
     )


admin.site.register(User, UserAdmin)
admin.site.register(Convite)
admin.site.register(Trilha)
admin.site.register(Curso)
admin.site.register(LinkCurso)
admin.site.register(User_Link)
admin.site.register(Trilha_User)


