from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Movimentacao, Correntista

class OperacaoBasicaSerializer(serializers.Serializer): # Serializer básico para operações de Crédito e Débito
    correntista_id = serializers.IntegerField()
    valor = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)])

class CorrentistaSerializer(serializers.ModelSerializer): # Serializer para o modelo Correntista
    class Meta:
        model = Correntista
        fields = ['id', 'nome_correntista']

class MovimentacaoSerializer(serializers.ModelSerializer): # Serializer para o modelo Movimentacao

    correntista = CorrentistaSerializer(read_only=True)
    
    correntista_beneficiario = CorrentistaSerializer(read_only=True, allow_null=True) # Serializa o beneficiário, se houver
    
    tipo_operacao_display = serializers.CharField(source='get_tipo_operacao_display', read_only=True) # Campo extra para mostrar 'Crédito' ou 'Débito' de forma amigável

    class Meta:
        model = Movimentacao
        fields = [
            'id', 
            'tipo_operacao_display',
            'valor_operacao', 
            'data_operacao', 
            'descricao', 
            'correntista', 
            'correntista_beneficiario'
        ]

class PagamentoSerializer(OperacaoBasicaSerializer): # Serializer para operações de Pagamento
    descricao = serializers.CharField(max_length=50)

class TransferenciaSerializer(serializers.Serializer): # Serializer para operações de transferência
    correntista_origem_id = serializers.IntegerField()
    correntista_destino_id = serializers.IntegerField()
    valor = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)])
    
    def validate(self, data):
        """ 
        Valida se os correntistas de origem e destino são diferentes. 
        """

        if data['correntista_origem_id'] == data['correntista_destino_id']:
            raise serializers.ValidationError("Correntista de origem e destino devem ser diferentes.")
        return data