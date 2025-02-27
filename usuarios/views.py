import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def cadastrar_usuario(request):
    if request.method == "POST":
        usuario = request.POST.get("name")  # Alterado de "usuario" para "name"
        email_usuario = request.POST.get("email")
        senha = request.POST.get("password")  # Alterado de "senha" para "password"
        confirmar_senha = request.POST.get("confirm_password")  # Alterado para "confirm_password"

        # Verifica se os campos estão preenchidos corretamente
        if not usuario:
            messages.error(request, "O campo nome é obrigatório.")
            return redirect("cadastrar")

        # Validação do nome (somente letras)
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", usuario):
            messages.error(request, "O nome deve conter apenas letras e espaços.")
            return redirect("cadastrar")

        if not email_usuario:
            messages.error(request, "O campo e-mail é obrigatório.")
            return redirect("cadastrar")

        # Validação do e-mail
        if "@" not in email_usuario or "." not in email_usuario:
            messages.error(request, "E-mail inválido.")
            return redirect("cadastrar")

        if not senha or not confirmar_senha:
            messages.error(request, "Os campos de senha são obrigatórios.")
            return redirect("cadastrar")

        # Validação da senha
        if len(senha) < 8 or not re.search(r"\d", senha) or not re.search(r"[A-Z]", senha) or not re.search(
                r"[!@#$%^&*(),.?\":{}|<>]", senha):
            messages.error(request,
                           "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, um número e um caractere especial.")
            return redirect("cadastrar")

        # Confirmação de senha
        if senha != confirmar_senha:
            messages.error(request, "As senhas informadas não coincidem.")
            return redirect("cadastrar")

        # Verificação se o e-mail já está cadastrado
        if User.objects.filter(email=email_usuario).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect("cadastrar")

        # Criação do usuário
        novo_usuario = User.objects.create_user(username=usuario, email=email_usuario, password=senha, first_name=usuario)
        messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect("entrar")

    return render(request, "cadastro.html")



def autenticar_usuario(request):
    if request.method == "POST":
        email_fornecido = request.POST.get("email")
        senha_digitada = request.POST.get("password")

        # Verifica se o email existe
        try:
            usuario = User.objects.get(email=email_fornecido)
        except User.DoesNotExist:
            messages.error(request, "O e-mail informado não existe.")
            return redirect("entrar")

        # Verifica se a senha foi informada
        if not senha_digitada:
            messages.error(request, "Por favor, informe a senha.")
            return redirect("entrar")

        # Autenticação do usuário
        usuario_autenticado = authenticate(request, username=usuario.username, password=senha_digitada)
        if usuario_autenticado is None:
            messages.error(request, "Senha inexistente.")
            return redirect("entrar")

        # Login bem-sucedido
        login(request, usuario_autenticado)
        return redirect("home")  

    return render(request, "login.html")


def sair_sessao(request):
    logout(request)
    return redirect("entrar")


@login_required(login_url="entrar")
def painel_principal(request):
    return render(request, "home.html")
