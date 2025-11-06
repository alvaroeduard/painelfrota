# frota/models.py

from django.db import models
from django.utils import timezone

class ModeloVeiculo(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
    
class Regional(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.sigla

    def save(self, *args, **kwargs):
        self.sigla = self.sigla.upper().strip()
        super(Regional, self).save(*args, **kwargs)

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"
    
    def save(self, *args, **kwargs):
        self.sigla = self.sigla.upper().strip()
        super(Departamento, self).save(*args, **kwargs)

class Veiculo(models.Model):

    # Opções para os novos campos
    TIPO_VEICULO_CHOICES = [
        ('LEVE', 'Leve'),
        ('MEDIO', 'Médio'),
        ('PESADO', 'Pesado'),
        ('EQUIPAMENTO', 'Equipamento'),
    ]

    SEGMENTO_CHOICES = [
        ('LT', 'Linha de Transmissão'),
        ('SE', 'Subestação'),
        ('N/A', 'Não Aplicável'),
    ]

    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Em Manutenção', 'Em Manutenção'),
        ('Indisponível', 'Indisponível'),
    ]

    prefixo = models.CharField(max_length=6, unique=True)
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.ForeignKey(ModeloVeiculo, on_delete=models.PROTECT, related_name='veiculos')
    tipo_veiculo = models.CharField(max_length=20, choices=TIPO_VEICULO_CHOICES, default='LEVE')
    segmento = models.CharField(max_length=5, choices=SEGMENTO_CHOICES, default='N/A')
    regional = models.ForeignKey(Regional, on_delete=models.PROTECT, related_name='veiculos')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='veiculos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Manutencao(models.Model):
    STATUS_OS_CHOICES = [
        ('Aguardando Orçamento', 'Aguardando Orçamento'),
        ('Aguardando Aprovação', 'Aguardando Aprovação'),
        ('Aprovado', 'Aprovado'),
        ('Garantia', 'Garantia'),
        ('N/A', 'N/A'),
    ]
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='manutencao')
    servicos = models.TextField()
    nome_oficina = models.CharField(max_length=100, blank=True, verbose_name="Nome da Oficina")
    cidade_oficina = models.CharField(max_length=100, blank=True, verbose_name="Cidade da Oficina")
    data_entrada = models.DateField(default=timezone.now)
    data_previsao_saida = models.DateField(null=True, blank=True)
    numero_os = models.CharField(max_length=50, verbose_name="Número da OS/Ticket")
    status_os = models.CharField(max_length=50, choices=STATUS_OS_CHOICES, verbose_name="Status da OS")

    def __str__(self):
        return f"Manutenção do veículo {self.veiculo.placa}"

class Indisponibilidade(models.Model):
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='indisponibilidade')
    motivo = models.TextField()

    def __str__(self):
        return f"Indisponibilidade do veículo {self.veiculo.placa}"

class UltimaAtualizacao(models.Model):
    data_hora = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.data_hora.strftime('%d/%m/%Y %H:%M:%S')