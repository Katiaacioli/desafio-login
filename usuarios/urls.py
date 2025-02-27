from django.urls import path
from . import views

urlpatterns = [
    path("cadastrar/", views.cadastrar_usuario, name="cadastrar"),
    path("login/", views.autenticar_usuario, name="entrar"),
    path("logout/", views.sair_sessao, name="sair"),
    path("home/", views.painel_principal, name="home"),
    
]