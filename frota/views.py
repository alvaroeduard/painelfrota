# frota/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Veiculo, Departamento, Manutencao, Indisponibilidade, UltimaAtualizacao
from .forms import DepartamentoForm, VeiculoForm, ManutencaoForm, IndisponibilidadeForm
from .forms import ModeloVeiculoForm, RegionalForm
from .models import ModeloVeiculo, Regional

# --- Funções Auxiliares ---
def registrar_atualizacao():
    """Cria ou atualiza o registro de última atualização."""
    obj, created = UltimaAtualizacao.objects.get_or_create(pk=1)
    if not created:
        obj.save() # Força a atualização do campo auto_now

# --- Views Públicas ---
def index(request):
    """
    Exibe a página inicial com a lista de veículos e os filtros de pesquisa.
    """
    # Pega todos os parâmetros de filtro da URL (GET request)
    placa = request.GET.get('placa')
    depto_id = request.GET.get('departamento')
    status_selecionado = request.GET.get('status')
    regional_id = request.GET.get('regional')

    # Inicia a busca por todos os veículos, já otimizando a consulta ao banco de dados
    veiculos = Veiculo.objects.select_related('departamento', 'modelo', 'regional', 'manutencao', 'indisponibilidade').all().order_by('prefixo')

    # Aplica os filtros um a um, se eles existirem
    if placa:
        veiculos = veiculos.filter(placa__icontains=placa)
    
    if depto_id:
        veiculos = veiculos.filter(departamento_id=depto_id)
    
    if status_selecionado:
        veiculos = veiculos.filter(status=status_selecionado)

    if regional_id:
        veiculos = veiculos.filter(regional_id=regional_id)
            
    # Busca os dados necessários para preencher os filtros na página
    departamentos = Departamento.objects.all().order_by('sigla')
    regionais = Regional.objects.all().order_by('sigla')
    status_choices = Veiculo.STATUS_CHOICES
    ultima_atualizacao = UltimaAtualizacao.objects.first()

    # Monta o contexto que será enviado para o template HTML
    context = {
        'veiculos': veiculos,
        'departamentos': departamentos,
        'regionais': regionais,
        'status_choices': status_choices,
        'ultima_atualizacao': ultima_atualizacao,
        'depto_id_selecionado': int(depto_id) if depto_id else None,
        'status_selecionado': status_selecionado,
        'regional_id_selecionado': int(regional_id) if regional_id else None,
    }
    return render(request, 'frota/index.html', context)

# --- Views do Painel Admin ---
@login_required
def admin_panel(request):
    ultima_atualizacao = UltimaAtualizacao.objects.first()
    return render(request, 'frota/admin_panel.html', {'ultima_atualizacao': ultima_atualizacao})

@login_required
def gerenciar_departamentos(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento cadastrado com sucesso!')
            return redirect('gerenciar_departamentos')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os dados.')
    else:
        form = DepartamentoForm()
    
    pesquisa = request.GET.get('pesquisa')
    departamentos = Departamento.objects.all().order_by('nome')
    if pesquisa:
        departamentos = departamentos.filter(Q(nome__icontains=pesquisa) | Q(sigla__icontains=pesquisa))

    ultima_atualizacao = UltimaAtualizacao.objects.first()
    context = {
        'form': form,
        'departamentos': departamentos,
        'ultima_atualizacao': ultima_atualizacao
    }
    return render(request, 'frota/departamentos.html', context)

@login_required
def editar_departamento(request, id):
    depto = get_object_or_404(Departamento, id=id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=depto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento atualizado com sucesso!')
            return redirect('gerenciar_departamentos')
    # Não precisa de um GET, a edição será feita via modal na página principal.
    return redirect('gerenciar_departamentos')

@login_required
def excluir_departamento(request, id):
    depto = get_object_or_404(Departamento, id=id)
    if depto.veiculos.exists():
        messages.error(request, 'Não é possível excluir um departamento que possui veículos associados.')
    else:
        depto.delete()
        messages.success(request, 'Departamento excluído com sucesso!')
    return redirect('gerenciar_departamentos')


@login_required
def gerenciar_veiculos(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            registrar_atualizacao()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('gerenciar_veiculos')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os dados (placa e prefixo não podem ser duplicados).')
    else:
        form = VeiculoForm()

    placa = request.GET.get('placa')
    veiculos = Veiculo.objects.select_related('departamento', 'modelo', 'regional').all().order_by('prefixo') # Adicione 'modelo' aqui

    if placa:
        veiculos = veiculos.filter(placa__icontains=placa)

    departamentos = Departamento.objects.all() # ADICIONE ESTA LINHA
    modelos = ModeloVeiculo.objects.all() # ADICIONE ESTA LINHA
    regionais = Regional.objects.all()
    ultima_atualizacao = UltimaAtualizacao.objects.first()

    context = {
        'form': form,
        'veiculos': veiculos,
        'departamentos': departamentos,
        'modelos': modelos, # ADICIONE ESTA LINHA
        'regionais': regionais,
        'ultima_atualizacao': ultima_atualizacao
    }
    return render(request, 'frota/lista_veiculos.html', context)

@login_required
def editar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            registrar_atualizacao()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('gerenciar_veiculos')
    return redirect('gerenciar_veiculos')

@login_required
def excluir_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    veiculo.delete()
    registrar_atualizacao()
    messages.success(request, 'Veículo excluído com sucesso!')
    return redirect('gerenciar_veiculos')

@login_required
def gerenciar_manutencao(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    
    if veiculo.status == 'Indisponível':
        messages.error(request, 'O veículo está indisponível. Finalize a indisponibilidade primeiro.')
        return redirect('gerenciar_veiculos')

    manutencao_instance = getattr(veiculo, 'manutencao', None)

    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao_instance)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.veiculo = veiculo
            manutencao.save()
            veiculo.status = 'Em Manutenção'
            veiculo.save()
            registrar_atualizacao()
            messages.success(request, 'Informações de manutenção salvas com sucesso!')
            return redirect('gerenciar_veiculos')
    return redirect('gerenciar_veiculos')

@login_required
def concluir_manutencao(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if hasattr(veiculo, 'manutencao'):
        veiculo.manutencao.delete()
        veiculo.status = 'Disponível'
        veiculo.save()
        registrar_atualizacao()
        messages.success(request, f'Manutenção do veículo {veiculo.placa} concluída.')
    return redirect('gerenciar_veiculos')

@login_required
def gerenciar_indisponibilidade(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if veiculo.status == 'Em Manutenção':
        messages.error(request, 'O veículo está em manutenção. Finalize a manutenção primeiro.')
        return redirect('gerenciar_veiculos')

    indisponibilidade_instance = getattr(veiculo, 'indisponibilidade', None)

    if request.method == 'POST':
        form = IndisponibilidadeForm(request.POST, instance=indisponibilidade_instance)
        if form.is_valid():
            indisponibilidade = form.save(commit=False)
            indisponibilidade.veiculo = veiculo
            indisponibilidade.save()
            veiculo.status = 'Indisponível'
            veiculo.save()
            registrar_atualizacao()
            messages.success(request, 'Status de indisponibilidade salvo com sucesso!')
            return redirect('gerenciar_veiculos')
    return redirect('gerenciar_veiculos')

@login_required
def tornar_disponivel(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    if hasattr(veiculo, 'indisponibilidade'):
        veiculo.indisponibilidade.delete()
        veiculo.status = 'Disponível'
        veiculo.save()
        registrar_atualizacao()
        messages.success(request, f'Veículo {veiculo.placa} agora está disponível.')
    return redirect('gerenciar_veiculos')

@login_required
def gerenciar_modelos(request):
    if request.method == 'POST':
        form = ModeloVeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo cadastrado com sucesso!')
            return redirect('gerenciar_modelos')
        else:
            messages.error(request, 'Erro ao cadastrar. O modelo já pode existir.')
    else:
        form = ModeloVeiculoForm()

    pesquisa = request.GET.get('pesquisa')
    modelos = ModeloVeiculo.objects.all().order_by('nome')
    if pesquisa:
        modelos = modelos.filter(nome__icontains=pesquisa)

    context = {
        'form': form,
        'modelos': modelos,
        'ultima_atualizacao': UltimaAtualizacao.objects.first()
    }
    return render(request, 'frota/modelos.html', context)

@login_required
def editar_modelo(request, id):
    modelo = get_object_or_404(ModeloVeiculo, id=id)
    if request.method == 'POST':
        form = ModeloVeiculoForm(request.POST, instance=modelo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modelo atualizado com sucesso!')
            return redirect('gerenciar_modelos')
    return redirect('gerenciar_modelos')

@login_required
def excluir_modelo(request, id):
    modelo = get_object_or_404(ModeloVeiculo, id=id)
    if modelo.veiculos.exists():
        messages.error(request, 'Não é possível excluir um modelo que possui veículos associados.')
    else:
        modelo.delete()
        messages.success(request, 'Modelo excluído com sucesso!')
    return redirect('gerenciar_modelos')

@login_required
def gerenciar_regionais(request):
    """
    Gerencia o cadastro, listagem e pesquisa de Regionais.
    """
    if request.method == 'POST':
        form = RegionalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Regional cadastrada com sucesso!')
            return redirect('gerenciar_regionais')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique se a sigla já existe.')
    else:
        form = RegionalForm()
    
    pesquisa = request.GET.get('pesquisa')
    regionais = Regional.objects.all().order_by('nome')
    if pesquisa:
        regionais = regionais.filter(Q(nome__icontains=pesquisa) | Q(sigla__icontains=pesquisa))

    ultima_atualizacao = UltimaAtualizacao.objects.first()
    context = {
        'form': form,
        'regionais': regionais,
        'ultima_atualizacao': ultima_atualizacao
    }
    return render(request, 'frota/regionais.html', context)

@login_required
def editar_regional(request, id):
    """
    Edita uma Regional existente.
    """
    regional = get_object_or_404(Regional, id=id)
    if request.method == 'POST':
        form = RegionalForm(request.POST, instance=regional)
        if form.is_valid():
            form.save()
            messages.success(request, 'Regional atualizada com sucesso!')
            return redirect('gerenciar_regionais')
    # Se o método não for POST, apenas redireciona de volta, pois a edição é via modal.
    return redirect('gerenciar_regionais')

@login_required
def excluir_regional(request, id):
    """
    Exclui uma Regional, com verificação para não excluir se houver veículos associados.
    """
    regional = get_object_or_404(Regional, id=id)
    if regional.veiculos.exists():
        messages.error(request, f'Não é possível excluir a regional "{regional.sigla}" pois ela possui veículos associados.')
    else:
        regional.delete()
        messages.success(request, 'Regional excluída com sucesso!')
    return redirect('gerenciar_regionais')