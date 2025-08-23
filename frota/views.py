# frota/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Veiculo, Departamento, Manutencao, Indisponibilidade, UltimaAtualizacao
from .forms import DepartamentoForm, VeiculoForm, ManutencaoForm, IndisponibilidadeForm

# --- Funções Auxiliares ---
def registrar_atualizacao():
    """Cria ou atualiza o registro de última atualização."""
    obj, created = UltimaAtualizacao.objects.get_or_create(pk=1)
    if not created:
        obj.save() # Força a atualização do campo auto_now

# --- Views Públicas ---
def index(request):
    placa = request.GET.get('placa')
    depto_id = request.GET.get('departamento')
    
    veiculos = Veiculo.objects.select_related('departamento', 'manutencao', 'indisponibilidade').all().order_by('prefixo')

    if placa:
        veiculos = veiculos.filter(placa__icontains=placa)
    
    if depto_id:
        veiculos = veiculos.filter(departamento_id=depto_id)
        
    departamentos = Departamento.objects.all().order_by('sigla')
    ultima_atualizacao = UltimaAtualizacao.objects.first()

    context = {
        'veiculos': veiculos,
        'departamentos': departamentos,
        'ultima_atualizacao': ultima_atualizacao,
        'depto_id_selecionado': int(depto_id) if depto_id else None
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
    veiculos = Veiculo.objects.select_related('departamento').all().order_by('prefixo')
    if placa:
        veiculos = veiculos.filter(placa__icontains=placa)

    departamentos = Departamento.objects.all() # ADICIONE ESTA LINHA
    ultima_atualizacao = UltimaAtualizacao.objects.first()

    context = {
        'form': form,
        'veiculos': veiculos,
        'departamentos': departamentos, # ADICIONE ESTA LINHA
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