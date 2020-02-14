from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Convite, Trilha, Curso, LinkCurso, User_Link, Trilha_User
from .forms import SignupForm, UserForm, UserChangeFormAdmin, ConviteForm, Trilha_Create_Form, CursoForm, UserFormPreview, CursoLinkForm, CertificadoForm, UserLinkCursoForm
from .admin import UserChangeForm, UserStaffForm
from .mail import send_mail
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import assign_role, clear_roles
from rolepermissions.checkers import has_role
from projetoTrilhas.roles import Administrador, Moderador
from django.contrib import messages
from django.http import HttpResponseRedirect

# @login_required()
# def homePage(request):
#     if not has_role(request.user, ['estudante', 'moderador', 'administrador']):
#         assign_role(request.user, 'estudante')
#
#     return render(request, '_home.html')

def user_create(request, token):
    convite = get_object_or_404(Convite, token=token)
    formConvite = SignupForm(request.POST or None, instance=convite)
    form = SignupForm(request.POST or None)

    if form.is_valid():
        form.save()
        convite.delete()
        return redirect('login')

    return render(request, '_signup.html', {'form': form, 'formConvite': formConvite})

@login_required()
def consultar_users(request):
    users = User.objects.all()

    return render(request, "_admin-consultar-usuario.html", {'users': users})

@login_required()
@has_role_decorator(Administrador)
def user_delete(request, id):
    user = get_object_or_404(User, pk=id)

    user.delete()

    return redirect('consultar_users')

@login_required()
def setUserStudentRole(id):
    user = get_object_or_404(User, pk=id)
    assign_role(user, 'student')
    return has_role(user, Student)

@login_required()
def user_update(request, id):
    user = get_object_or_404(User, pk=id)
    form = UserForm(request.FILES or None, request.POST or None, instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None, instance=user)

        if form.is_valid():
            form.save()
            return redirect('consultar_users')

    return render(request, 'admin-alterar-usuario-2.html', {'user': user, 'form': form})

@login_required()
def user_update_preview(request, id):
    user = get_object_or_404(User, pk=id)
    form = UserFormPreview(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('consultar_users')

    return render(request, 'admin-alterar-usuario.html', {'user': user, 'form': form})

# @login_required()
# @has_role_decorator(Administrador)
# def userChangeAdmin(request, id):
#     user = get_object_or_404(User, pk=id)
#     form = UserChangeForm(request.POST or None, instance=user)
#     form_is_staff = UserStaffForm(request.POST or None, instance=user)
#
#     if form.is_valid() and form_is_staff.is_valid():
#         form_is_staff.save()
#         user.setRole()
#         form.save()
#
#         return redirect('consultar_users')
#
#     return render(request, '_userChangeAdmin.html', {'form': form, 'user': user, 'form_is_staff': form_is_staff})

@login_required()
@has_role_decorator(Administrador)
def criar_convite(request):
    #conviteFormset = modelformset_factory(Convite, fields=('name', 'email'), extra=1)
    args = {}
    convites = Convite.objects.all()
    form = ConviteForm(request.POST or None)
    storaged = messages.get_messages(request)

    if form.is_valid():
        #form = conviteFormset(request.POST)
        form.save()
        #return redirect('admin_gerar_convite')

    #form = conviteFormset()

    return render(request, 'convite/admin-gerar-convite.html', {'form': form, 'convites': convites, 'messages': storaged})

@login_required()
@has_role_decorator(Administrador)
def enviar_convite(request):
    convites = Convite.objects.all()

    for convite in convites:
        send_mail(convite)
        convite.enviado = True
        convite.save(force_update=True)

    messages.success(request, 'Convite(s) enviado(s) com sucesso!')

    return redirect('admin_gerar_convite')

@login_required()
@has_role_decorator(Administrador)
def convite_delete(request, id):
    convite = get_object_or_404(Convite, pk=id)

    convite.delete()

    return redirect('admin_gerar_convite')

@login_required()
def admin_painel(request):
    return render(request, "_admin-painel.html")


#---- código para referência
'''
def enviar_convite(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            form.send_mail()

    else:
        form = EmailForm

    return render(request, 'convite_envio.html', {'form': form})

'''

@login_required()
def trilha_gerenciar(request):

    form = Trilha_Create_Form(request.POST or None)

    trilhas_user = Trilha_User.objects.filter(user=request.user)

    if request.user.role == 'Administrador' or request.user.role == 'Moderador':
        trilhas = Trilha.objects.all()
    else:
        trilhas = request.user.trilha.all()

    if request.method == 'POST':

        form = Trilha_Create_Form(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('gerenciar_trilhas')

    return render(request, "trilhas/admin_gerenciar_trilha.html", {'form': form,
                                                                   'trilhas': trilhas,
                                                                   'trilhasProgress': trilhas_user})

@login_required()
@has_role_decorator(Administrador, Moderador)
def trilha_update(request, id):
    trilha = get_object_or_404(Trilha, pk=id)
    form = Trilha_Create_Form(request.POST or None, request.FILES or None, instance=trilha)

    if request.method == 'POST':
        form = Trilha_Create_Form(request.POST or None, request.FILES or None, instance=trilha)

        if form.is_valid():
            form.save()
            return redirect('gerenciar_trilhas')

    return render(request, 'trilhas/admin_alterar_trilha.html', {'form': form})


@login_required()
@has_role_decorator(Administrador, Moderador)
def trilha_delete(request, id):
    trilha = get_object_or_404(Trilha, pk=id)

    trilha.delete()

    return redirect('gerenciar_trilhas')

@login_required()
def curso_create(request, id):

    trilha = get_object_or_404(Trilha, pk=id)
    cursos = Curso.objects.filter(trilha=id)

    form = CursoForm
    formLink = CursoLinkForm
    formLinkEdit = CursoLinkForm

    links = LinkCurso.objects.all()

    if request.method == 'POST' and 'AddCurso' in request.POST:
        form = CursoForm(request.POST or None)

        if form.is_valid():
            instance = form.save(commit=True)
            instance.trilha = trilha
            instance.save()

            return redirect('criar_curso', id=id)

    elif request.method == 'POST' and 'AddLink' in request.POST:
        formLink = CursoLinkForm(request.POST or None)

        if formLink.is_valid():
            instance = formLink.save(commit=True)
            curso = get_object_or_404(Curso, pk=request.POST['AddLink'])
            instance.curso = curso
            instance.save()
            formLink.setCargaHorariaToCursoAndTrilha()

            return redirect('criar_curso', id=id)

    elif request.method == 'POST' and 'LinkEdit' in request.POST:
        link = get_object_or_404(LinkCurso, pk=request.POST['LinkEdit'])
        formLinkEdit = CursoLinkForm(request.POST or None, instance=link)

        if formLinkEdit.is_valid():
            formLinkEdit.save()
            formLinkEdit.setCargaHorariaToCursoAndTrilha()

            return redirect('criar_curso', id=id)

    else:
        form = CursoForm()
        formLink = CursoLinkForm()
        formLinkEdit = CursoLinkForm()

    return render(request, 'trilhas/admin_gerenciar_curso.html', {'form': form,
                                                                  'trilha': trilha,
                                                                  'cursos': cursos,
                                                                  'formLink': formLink,
                                                                  'linksCursos': links,
                                                                  'formLinkEdit': formLinkEdit})

# @login_required()
# def curso_update(request, id):
#     linkCurso = get_object_or_404(LinkCurso, pk=id)
#     formLinkEdit = CursoLinkForm(request.POST or None, instance=linkCurso)
#
#     if formLinkEdit.is_valid():
#         formLinkEdit.save()
#         return redirect('criar_curso', id=linkCurso.curso.trilha.pk)
#
#     return render(request, 'trilhas/admin_gerenciar_curso.html', {'formLinkEdit': formLinkEdit})


@login_required()
def curso_delete(request, id):

    linkObject = get_object_or_404(LinkCurso, pk=id)
    linkToCurso = LinkCurso.objects.filter(pk=id)

    linkObject.curso.trilha.carga_horaria -= linkObject.carga_horaria
    linkObject.curso.trilha.save(force_update=True)

    linkToCurso.delete()

    return redirect('criar_curso', id=linkObject.curso.trilha.pk)

@login_required()
@has_role_decorator(Administrador, Moderador)
def curso_apagar(request, id):
    curso = get_object_or_404(Curso, pk=id)

    curso.trilha.carga_horaria -= curso.carga_horaria
    curso.trilha.save(force_update=True)

    curso.delete()

    return redirect('criar_curso', id=curso.trilha.pk)

@login_required()
@has_role_decorator(Administrador, Moderador)
def curso_alterar(request, id):
    curso = get_object_or_404(Curso, pk=id)
    form = CursoForm(request.POST or None, instance=curso)

    if request.method == 'POST':
        form = CursoForm(request.POST or None, instance=curso)

        if form.is_valid():
            form.save()
            return redirect('criar_curso', id=curso.trilha.pk)

    return render(request, 'trilhas/admin_alterar_curso.html', {'form': form, 'curso': curso})

@login_required()
def curso_link_user(request, id):
    context = {}
    cursos = []
    linksCursos = []

    user = get_object_or_404(User, pk=id)
    context['form'] = UserLinkCursoForm(instance=user)

    for trilha in user.trilha.all():
        cursos.append(Curso.objects.filter(trilha=trilha))

    for curso in cursos:
        linksCursos.append(LinkCurso.objects.filter(curso__in=curso))

    if request.method == 'POST':
        form = UserLinkCursoForm(request.POST or None, instance=user)

        if form.is_valid():
            context['form'] = form
            form.save()
            form.createCursoLinkAndUser()

            return redirect('user_link_curso', id=id)

    context['userLinks'] = User_Link.objects.filter(user=user)
    context['allLinks'] = LinkCurso.objects.all()
    context['links_users'] = linksCursos
    context['user'] = user

    return render(request, 'gerenciar_user_trilhas.html', context)

@login_required()
def user_lista_certificados(request, id):
    context = {}
    cursos = []
    linksCursos = []

    user = get_object_or_404(User, pk=id)

    for trilha in user.trilha.all():
        cursos.append(Curso.objects.filter(trilha=trilha))

    for curso in cursos:
        linksCursos.append(LinkCurso.objects.filter(curso__in=curso))

    context['userLinks'] = User_Link.objects.filter(user=user)
    context['allLinks'] = LinkCurso.objects.all()
    context['user'] = user

    return render(request, 'user_lista_certificados.html', context)

@login_required()
def upload_certificado(request, id_user, id_link):
    user_link = get_object_or_404(User_Link, user=id_user, cursoLink=id_link)

    form = CertificadoForm(request.POST or None, request.FILES or None, instance=user_link)

    if request.method == 'POST':
        form = CertificadoForm(request.POST or None, request.FILES or None, instance=user_link)

        if form.is_valid():
            form.save()
            form.setProgressoToTrilhaAndCurso(user_link)
            return redirect('user_link_curso', id=id_user)

    return render(request, 'upload_certificado.html', {'form': form, 'user_link': user_link})
