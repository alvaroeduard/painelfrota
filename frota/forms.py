# frota/forms.py

from django import forms
from .models import Departamento, Veiculo, Manutencao, Indisponibilidade, ModeloVeiculo, Regional

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nome', 'sigla']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ModeloVeiculoForm(forms.ModelForm):
    class Meta:
        model = ModeloVeiculo
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat Strada'}),
        }

class RegionalForm(forms.ModelForm):
    class Meta:
        model = Regional
        fields = ['nome', 'sigla']

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['prefixo', 'placa', 'modelo', 'tipo_veiculo', 'segmento', 'regional', 'departamento']
        widgets = {
            'prefixo': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.Select(attrs={'class': 'form-select'}),
            'tipo_veiculo': forms.Select(attrs={'class': 'form-select'}),
            'segmento': forms.Select(attrs={'class': 'form-select'}),
            'regional': forms.Select(attrs={'class': 'form-select'}), # Adicione o widget
            'departamento': forms.Select(attrs={'class': 'form-select'}),
        }

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['servicos', 'nome_oficina', 'cidade_oficina', 'data_entrada', 'data_previsao_saida', 'numero_os', 'status_os']
        widgets = {
            'servicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nome_oficina': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade_oficina': forms.TextInput(attrs={'class': 'form-control'}), # Adicione
            'data_entrada': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'data_previsao_saida': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
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