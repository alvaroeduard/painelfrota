# frota/models.py

from django.db import models
from django.utils import timezone

class ModeloVeiculo(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"
    
    def save(self, *args, **kwargs):
        self.sigla = self.sigla.upper().strip()
        super(Departamento, self).save(*args, **kwargs)

class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Em Manutenção', 'Em Manutenção'),
        ('Indisponível', 'Indisponível'),
    ]

    prefixo = models.CharField(max_length=6, unique=True)
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.ForeignKey(ModeloVeiculo, on_delete=models.PROTECT, related_name='veiculos')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='veiculos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Manutencao(models.Model):
    STATUS_OS_CHOICES = [
        ('Aguardando Orçamento', 'Aguardando Orçamento'),
        ('Aguardando Nível 0', 'Aguardando Nível 0'),
        ('Aguardando Nível 1', 'Aguardando Nível 1'),
        ('Aguardando Nível 2', 'Aguardando Nível 2'),
        ('Aguardando Nível 3', 'Aguardando Nível 3'),
        ('Aprovado', 'Aprovado'),
    ]
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE, related_name='manutencao')
    servicos = models.TextField()
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