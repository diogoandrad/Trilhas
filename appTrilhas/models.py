from django.db import models
from django.contrib.auth.models import AbstractUser
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_role
import uuid
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit



class Convite(models.Model):
    def generate_token():
        return uuid.uuid4()

    name = models.CharField(max_length=130, blank=False, null=False)
    email = models.EmailField(max_length=70, unique=True, null=False)
    enviado = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    token = models.CharField(max_length=40, unique=True, blank=False, default=generate_token)

    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name

class Curso(models.Model):
    nome = models.CharField(max_length=128, blank=False, null=False)
    carga_horaria = models.IntegerField(null=True, default=0)
    esta_concluido = models.BooleanField(default=False)
    descricao = models.TextField(max_length=300, blank=True, null=True)
    trilha = models.ForeignKey('Trilha', on_delete=models.CASCADE, null=True)
    progresso = models.FloatField(default=0)

    def __str__(self):
        return self.nome

class Trilha(models.Model):
    nome = models.CharField(max_length=128, blank=False, null=False)
    data_de_criacao = models.DateTimeField('Criado em', auto_now_add=True)
    data_de_conclusao = models.DateTimeField('Concluido em', auto_now_add=True)
    data_de_inicio = models.DateTimeField(null=True)
    esta_concluido = models.BooleanField(default=False)
    carga_horaria = models.IntegerField(null=True, default=0)
    imagem = ProcessedImageField(upload_to='trilhas', processors=[ResizeToFit(300, 250)])
    descricao = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nome

class LinkCurso(models.Model):
    nome = models.CharField(max_length=128, blank=False, null=False)
    link = models.URLField(null=True)
    carga_horaria = models.IntegerField(null=True, default=0)
    esta_concluido = models.BooleanField(default=False)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome


class User_Link(models.Model):
    user = models.ForeignKey('User', related_name='user_link', on_delete=models.SET_NULL, null=True)
    cursoLink = models.ForeignKey('LinkCurso', related_name='user_link', on_delete=models.SET_NULL, null=True)
    certificado = models.FileField(upload_to='certificados', null=True, blank=True)
    data_upload = models.DateTimeField('Data do upload', auto_now_add=True)

class Trilha_User(models.Model):
    user = models.ForeignKey('User', related_name='trilha_user', on_delete=models.SET_NULL, null=True)
    trilha = models.ForeignKey('Trilha', related_name='trilha_user', on_delete=models.SET_NULL, null=True)
    progresso = models.FloatField(default=0)

class User(AbstractUser):
    matricula = models.CharField(max_length=10, unique=True)
    ativo = models.BooleanField(default=False)
    username = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    name = models.CharField(max_length=130, blank=False, null=False)
    data_nascimento = models.DateField(null=True)
    genero = models.CharField(max_length=15, choices=(('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outros')))
    role = models.CharField(max_length=20,
                            choices=(('Administrador', 'Administrador'),
                                     ('Estudante', 'Estudante'),
                                     ('Moderador', 'Moderador')),
                            default='Estudante', null=False)

    imagem = ProcessedImageField(upload_to='usuarios', processors=[ResizeToFit(200, 200)], null=True, blank=True)
    cursoLink = models.ManyToManyField('LinkCurso', through='User_Link', related_name='users')
    trilhaProgresso = models.ManyToManyField('Trilha', through='Trilha_User', related_name='users')
    trilha = models.ManyToManyField(Trilha)

    USERNAME_FIELD = 'matricula'

    REQUIRED_FIELDS = ['username', 'email', 'name', 'role']

    def __str__(self):
        return self.name

    def setRole(self):

        if self.is_staff or self.is_superuser:
            clear_roles(self)
            assign_role(self, 'administrador')
            self.role = 'Administrador'
        else:
            if self.role == 'Moderador':
                clear_roles(self)
                assign_role(self, 'moderador')
            else:
                clear_roles(self)
                assign_role(self, 'estudante')
                self.role = 'Estudante'


