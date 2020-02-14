from django import forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordContextMixin
from django.forms import ModelForm, PasswordInput, Select, formset_factory
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from .models import User, Convite, Trilha, Curso, LinkCurso, User_Link, Trilha_User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from .mail import send_mail_template
from rolepermissions.decorators import has_role_decorator
from projetoTrilhas.roles import Administrador
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

GENERO_CHOICES = [('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outros')]
ROLE_CHOICES = (('Estudante', 'Estudante'), ('Moderador', 'Moderador'), ('Administrador', 'Administrador'))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'matricula', 'data_nascimento', 'genero', 'email']

        widgets = {
            'matricula': forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'style': 'margin-top: 8px', 'readonly': 'true'}),
            'data_nascimento': forms.SelectDateWidget(years=range(1960, 2010),
                                                      attrs={'class': 'form-control',
                                                            'style': 'width: 33.333%; '
                                                                     'display: inline-block; '
                                                                     'margin-top: 6px; '
                                                                     'margin-bottom: 6px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmação de Senha'})
        self.fields['genero'].widget = Select(choices=GENERO_CHOICES, attrs={'class': 'form-control',
                                                    'style': 'height: 78%; margin-top: 6px; margin-bottom: 6px;'})


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'matricula', 'email', 'data_nascimento', 'role', 'imagem', 'genero']

        widgets = {'data_nascimento': forms.SelectDateWidget(years=range(1960, 2010),
                                                              attrs={'class': 'form-control',
                                                                    'style': 'width: 33.3%; '
                                                                             'display: inline-block; '
                                                                             'margin-top: 6px; '
                                                                             'margin-bottom: 6px;'}),
                    'name': forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class': 'form-control'}),
                    'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'style': 'margin-top: 8px',}),
                    'matricula': forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'form-control', 'readonly':'true'}),
                    'role': forms.Select(choices=ROLE_CHOICES, attrs={'class': 'form-control'}),
                    'genero': forms.Select(choices=GENERO_CHOICES,
                                                  attrs={'class': 'form-control',
                                                         'style': 'height: 78%; margin-top: 6px; margin-bottom: 6px;'
                                                         })
                   }

    '''
    def clean_imagem(self):
        image = self.cleaned_data['imagem']

        if image:
            if image._size > 4*1024*1024:
                raise ValidationError("A imagem ultrapassa o limite de tamanho (4mb).")

            if image._width > 60:
                raise forms.ValidationError("A imagem selecionada é muito larga.")

            return image

        else:
            raise ValidationError("Não é possível carregar a imagem.")
        '''
class UserFormPreview(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'genero', 'data_nascimento', 'matricula', 'email', 'role', 'imagem', 'genero']

        widgets = {'data_nascimento': forms.SelectDateWidget(years=range(1960, 2010),
                                                            attrs={'class': 'form-control',
                                                                    'style': 'width: 33.3%; '
                                                                             'display: inline-block; '
                                                                             'margin-top: 6px; '
                                                                             'margin-bottom: 6px;'}),
                   'name': forms.TextInput(attrs={'placeholder': 'Nome Completo', 'class': 'form-control'}),
                   'email': forms.TextInput(
                       attrs={'placeholder': 'Email', 'class': 'form-control', 'style': 'margin-top: 8px', }),
                   'matricula': forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'form-control'}),
                   'role': forms.Select(choices=ROLE_CHOICES, attrs={'class': 'form-control'})
                   }

    def __init__(self, *args, **kwargs):
        super(UserFormPreview, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['data_nascimento'].widget.attrs['readonly'] = True
        self.fields['matricula'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['role'].widget.attrs['readonly'] = True
        self.fields['genero'].widget = Select(choices=GENERO_CHOICES,
                                              attrs={'class': 'form-control',
                                                     'style': 'height: 78%; margin-top: 6px; margin-bottom: 6px;',
                                                     'readonly':'true'
                                                     }
                                              )


UserFormset = formset_factory(UserForm, extra=1)

class UserChangeFormAdmin(ModelForm):
    class Meta:
        model = User
        fields = ['role',]

        widgets = {
            'role': forms.Select(choices=ROLE_CHOICES, attrs={'class': 'form-control'})
        }

class ConviteForm(ModelForm):
    class Meta:
        model = Convite
        fields = ['name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']

        if Convite.objects.filter(email=email).count():
            raise forms.ValidationError("Já existe um convite cadastrado com este e-mail.")

        if User.objects.filter(email=email).count():
            raise forms.ValidationError("Já existe um usuário cadastrado com este e-mail.")

        return email

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = _("E-mail não registrado.")
            self.add_error('email', msg)
        return email

class Trilha_Create_Form(ModelForm):
    class Meta:
        model = Trilha
        fields = ['nome', 'descricao', 'imagem']

        widgets = {
                'nome': forms.TextInput(attrs={'placeholder': 'Título', 'class': 'form-control'}),
                'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'class': 'form-control'}),
        }

class CursoForm(ModelForm):
    class Meta:
        model = Curso

        fields = ['nome', 'descricao']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Título', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'class': 'form-control'})
        }

class CursoLinkForm(ModelForm):
    class Meta:
        model = LinkCurso

        fields = ['nome', 'link', 'carga_horaria']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Título do Curso', 'class': 'form-control'}),
            'link': forms.TextInput(attrs={'placeholder': 'Link', 'class': 'form-control'}),
            'carga_horaria': forms.NumberInput(attrs={'placeholder': 'Carga horaria', 'class': 'form-control', 'min': '0'}),
        }

    def setCargaHorariaToCursoAndTrilha(self):
        linkCurso = super(CursoLinkForm, self).save(commit=False)


        linkCurso.curso.trilha.carga_horaria += linkCurso.carga_horaria
        linkCurso.curso.trilha.save(force_update=True)

        linkCurso.curso.carga_horaria += linkCurso.carga_horaria
        linkCurso.curso.save(force_update=True)

'''
class PasswordChangeView(PasswordContextMixin, FormView):
    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        messages.success('Convite(s) enviado(s) com sucesso!')
        return super().form_valid(form)'''

class UserLinkCursoForm(ModelForm):
    class Meta:
        model = User
        fields = ['trilha']

        widgets = {
            'trilha': forms.CheckboxSelectMultiple(),
        }

    def createCursoLinkAndUser(self):
        userTrilha = super(UserLinkCursoForm, self).save(commit=False)

        cursos = []
        linksCursos = []

        for trilha in Trilha.objects.all():
            cursos.append(Curso.objects.filter(trilha=trilha))

        for curso in cursos:
            linksCursos.append(LinkCurso.objects.filter(curso__in=curso))

        for linkCurso in linksCursos:
             for userLink in linkCurso:

                if userLink not in userTrilha.cursoLink.all():
                    User_Link.objects.create(user=userTrilha, cursoLink=userLink)


class CertificadoForm(ModelForm):
    class Meta:
        model = User_Link
        fields = ['certificado']

    def setProgressoToTrilhaAndCurso(self, user_link):
        trilhas_user = Trilha_User.objects.filter(user=user_link.user, trilha=user_link.cursoLink.curso.trilha)
        user_links = User_Link.objects.filter(user=user_link.user)

        somador_carga_horaria = 0

       #faz o cálculo da carga horária considerando apenas os links em que há certificado:
        for linkCurso in user_links:
            if linkCurso.cursoLink:
                if linkCurso.certificado:
                    for trilha_user in trilhas_user:
                        if linkCurso.cursoLink.curso.trilha == trilha_user.trilha:
                            somador_carga_horaria += linkCurso.cursoLink.carga_horaria

        if user_link.cursoLink.curso.trilha.carga_horaria != 0:
            progresso = (somador_carga_horaria / user_link.cursoLink.curso.trilha.carga_horaria) * 100

        if trilhas_user:
            for trilha_user in trilhas_user:
                if trilha_user:
                    trilha_user.progresso = progresso
                    trilha_user.save(force_update=True)

        else:
            Trilha_User.objects.create(user=user_link.user, trilha=user_link.cursoLink.curso.trilha, progresso=0)
