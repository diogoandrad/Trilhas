"""projetoTrilhas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appTrilhas import urls as trilhas_urls
from django.contrib.auth import views as auth_views
from appTrilhas.forms import EmailValidationOnForgotPassword
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('trilhas/', include(trilhas_urls)),
    path('trilhas/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('trilhas/alterar_senha/', auth_views.PasswordChangeView.as_view(template_name='password_change/password_change.html'),
         {'post_change_redirect': 'password_change_done'}, name='password_change'),
    path('trilhas/senha_alterada_sucesso/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change/password_change_done.html'),
         name='password_change_done'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
