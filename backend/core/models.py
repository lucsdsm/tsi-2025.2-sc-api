from django.db import models

class Correntista(models.Model):
    
    # CorrentistaID é criado automaticamente pelo Django como 'id'

    nome_correntista = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome_correntista

class Movimentacao(models.Model):

    # MovimentacaoID é criado automaticamente como 'id'

    TIPO_OPERACAO_CHOICES = [
        ('C', 'Crédito'),
        ('D', 'Débito'),
    ]

    tipo_operacao = models.CharField(max_length=1, choices=TIPO_OPERACAO_CHOICES)
    
    # Chave estrangeira para Correntista
    correntista = models.ForeignKey(
        Correntista, 
        on_delete=models.CASCADE, 
        related_name='movimentacoes'
    )
    
    valor_operacao = models.DecimalField(max_digits=10, decimal_places=2)
    data_operacao = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=50)
    
    # Chave estrangeira para o beneficiário (pode ser nula)
    correntista_beneficiario = models.ForeignKey(
        Correntista, 
        on_delete=models.SET_NULL, 
        related_name='transferencias_recebidas',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.get_tipo_operacao_display()} - {self.correntista.nome_correntista} - R$ {self.valor_operacao}"