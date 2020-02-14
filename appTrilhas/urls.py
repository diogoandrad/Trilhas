from django.urls import path
from .views import user_create, user_delete, user_update, enviar_convite, criar_convite, \
    admin_painel, consultar_users, convite_delete, trilha_gerenciar, trilha_delete, trilha_update, curso_create, \
    curso_delete, user_update_preview, curso_apagar, curso_alterar, curso_link_user, upload_certificado, user_lista_certificados
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('signup/<uuid:token>', user_create, name='signup'),

    path('paniel_controle/', admin_painel, name='admin_painel'),
    path('apagar_usuario/<int:id>/', user_delete, name='user_delete'),
    path('editar_usuario/<int:id>/', user_update, name='user_update'),
    path('editar_usuario_consultar/<int:id>/', user_update_preview, name='user_update_preview'),
    path('consultar_usuarios/', consultar_users, name='consultar_users'),

    # path('user_change_admin/<int:id>', userChangeAdmin, name='user_change_admin'),

    path('criar_convite/', criar_convite, name='admin_gerar_convite'),
    path('convite_enviado/', enviar_convite, name='enviar_convite'),
    path('apagar_convite/<int:id>/', convite_delete, name='convite_delete'),

    #path('criar_trilha/', trilha_create, name='criar_trilha'),
    path('apagar_trilha/<int:id>/', trilha_delete, name='apagar_trilha'),
    path('editar_trilha/<int:id>/', trilha_update, name='trilha_update'),
    path('gerenciar_trilhas/', trilha_gerenciar, name='gerenciar_trilhas'),

    path('gerenciar_cursos/<int:id>/', curso_create, name='criar_curso'),
    path('apagar_curso/<int:id>/', curso_delete, name='apagar_curso'),
    path('curso_apagar/<int:id>/', curso_apagar, name='curso_apagar'),
    path('curso_alterar/<int:id>/', curso_alterar, name='curso_alterar'),
    #path('consultar_curso/', consultar_cursos, name='consultar_cursos'),

    path('user_link_curso/<int:id>/', curso_link_user, name='user_link_curso'),
    path('lista_certificados/<int:id>/', user_lista_certificados, name='user_lista_certificados'),

    path('upload_certificado/<int:id_user>/<int:id_link>/', upload_certificado, name='upload_certificado'),

    #path('criar_link/<int:id>/', link_create, name='criar_link'),
]
