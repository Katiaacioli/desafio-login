from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioCadastro(UserCreationForm):
    endereco_email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = ['nome_usuario', 'endereco_email', 'senha1', 'senha2']
    
    def validar_email(self):
        endereco_email = self.cleaned_data.get('endereco_email')
        if User.objects.filter(email=endereco_email).exists():
            raise forms.ValidationError("O e-mail informado já está cadastrado.")
        return endereco_email
