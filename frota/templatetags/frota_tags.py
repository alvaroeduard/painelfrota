# frota/templatetags/frota_tags.py

from django import template
from ..forms import ManutencaoForm, IndisponibilidadeForm

register = template.Library()

@register.filter
def get_manutencao_form(veiculo):
    if hasattr(veiculo, 'manutencao'):
        return ManutencaoForm(instance=veiculo.manutencao)
    return ManutencaoForm()

@register.filter
def get_indisponibilidade_form(veiculo):
    if hasattr(veiculo, 'indisponibilidade'):
        return IndisponibilidadeForm(instance=veiculo.indisponibilidade)
    return IndisponibilidadeForm()