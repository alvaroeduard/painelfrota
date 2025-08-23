# frota/forms.py

from django import forms
from .models import Departamento, Veiculo, Manutencao, Indisponibilidade

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome', 'sigla']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['prefixo', 'placa', 'modelo', 'departamento']
        widgets = {
            'prefixo': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
        }

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['servicos', 'data_entrada', 'data_previsao_saida', 'numero_os', 'status_os']
        widgets = {
            'servicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_entrada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_previsao_saida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero_os': forms.TextInput(attrs={'class': 'form-control'}),
            'status_os': forms.Select(attrs={'class': 'form-select'}),
        }

class IndisponibilidadeForm(forms.ModelForm):
    class Meta:
        model = Indisponibilidade
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }