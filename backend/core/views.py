from django.db import transaction

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Movimentacao, Correntista
from .serializers import (
    MovimentacaoSerializer,
    OperacaoBasicaSerializer,
    PagamentoSerializer,
    TransferenciaSerializer
)

# 1. EXTRATO
class ExtratoView(ListAPIView):
    """
    View para listar todas as movimentações de um correntista específico.
    Acesso via /api/correntistas/<id>/extrato/
    """
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        # Pega o correntista associado ao usuário que fez a requisição
        correntista = self.request.user.correntista
        # Filtra as movimentações apenas para esse correntista
        return Movimentacao.objects.filter(correntista=correntista).order_by('-data_operacao')
    
# 2. PAGAMENTO
@api_view(['POST'])
@transaction.atomic # garante que todas as operações no banco ou funcionam ou falham juntas
def pagamento_view(request):
    """
    View para processar um pagamento (débito) de um correntista.
    Espera um JSON com 'correntista_id', 'valor' e 'descricao'.
    """
    serializer = PagamentoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dados = serializer.validated_data
    valor = dados['valor']
    descricao = dados['descricao']

    try:
        correntista = Correntista.objects.select_for_update().get(user=request.user)

        if correntista.saldo < valor:
            return Response({"erro": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
        
        correntista.saldo -= valor
        correntista.save()

        Movimentacao.objects.create(
            tipo_operacao='D',
            correntista=correntista,
            valor_operacao=valor,
            descricao=f"Pagamento: {descricao}"
        )
        return Response({"sucesso": "Pagamento realizado com sucesso."}, status=status.HTTP_200_OK)
    
    except Correntista.DoesNotExist:
        return Response({"erro": "Correntista não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
# 3. TRANSFERÊNCIA
@api_view(['POST'])
@transaction.atomic
def transferencia_view(request):
    """
    View para processar uma transferência entre dois correntistas.
    Espera um JSON com 'correntista_origem_id', 'correntista_destino_id' e 'valor'.
    """
    serializer = TransferenciaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dados = serializer.validated_data
    destino_id = dados['correntista_destino_id']
    valor = dados['valor']

    try:
        correntista_origem = Correntista.objects.select_for_update().get(user=request.user)
        destino = Correntista.objects.select_for_update().get(pk=destino_id)

        if correntista_origem.id == destino_id:
            return Response({"erro": "A conta de origem e destino não podem ser a mesma."}, status=status.HTTP_400_BAD_REQUEST)
        
        correntista_destino = Correntista.objects.select_for_update().get(pk=destino_id)

        if correntista_origem.saldo < valor:
            return Response({"erro": "Saldo insuficiente no correntista de origem."}, status=status.HTTP_400_BAD_REQUEST)
        
        correntista_origem.saldo -= valor
        correntista_destino.saldo += valor

        Movimentacao.objects.create(
            tipo_operacao='D',
            correntista=correntista_origem,
            valor_operacao=valor,
            descricao=f"Transferência para {correntista_destino.nome_correntista}",
            correntista_beneficiario=correntista_destino
        )
        Movimentacao.objects.create(
            tipo_operacao='C',
            correntista=correntista_destino,
            valor_operacao=valor,
            descricao=f"Transferência de {correntista_origem.nome_correntista}",
            correntista_beneficiario=correntista_origem
        )

        correntista_origem.save()
        correntista_destino.save()

        return Response({"sucesso": "Transferência realizada com sucesso."}, status=status.HTTP_200_OK)
    
    except Correntista.DoesNotExist:
        return Response({"erro": "Correntista de origem ou destino não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
# 4. SAQUE
@api_view(['POST'])
@transaction.atomic
def saque_view(request):
    """
    View para processar um saque (débito) de um correntista.
    Espera um JSON com 'correntista_id' e 'valor'.
    """
    serializer = OperacaoBasicaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dados = serializer.validated_data
    valor = dados['valor']

    try:
        correntista = Correntista.objects.select_for_update().get(user=request.user)

        if correntista.saldo < valor:
            return Response({"erro": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
        
        correntista.saldo -= valor
        correntista.save()

        Movimentacao.objects.create(
            tipo_operacao='D',
            correntista=correntista,
            valor_operacao=valor,
            descricao="Saque realizado"
        )
        return Response({"sucesso": "Saque realizado com sucesso."}, status=status.HTTP_200_OK)
    
    except Correntista.DoesNotExist:
        return Response({"erro": "Correntista não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
# 5. DEPÓSITO
@api_view(['POST'])
@transaction.atomic
def deposito_view(request):
    """
    View para processar um depósito (crédito) em um correntista.
    Espera um JSON com 'correntista_id' e 'valor'.
    """
    serializer = OperacaoBasicaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dados = serializer.validated_data
    valor = dados['valor']

    try:
        correntista = Correntista.objects.select_for_update().get(user=request.user)
        
        correntista.saldo += valor
        correntista.save()

        Movimentacao.objects.create(
            tipo_operacao='C',
            correntista=correntista,
            valor_operacao=valor,
            descricao="Depósito realizado"
        )
        return Response({"sucesso": "Depósito realizado com sucesso."}, status=status.HTTP_200_OK)
    
    except Correntista.DoesNotExist:
        return Response({"erro": "Correntista não encontrado."}, status=status.HTTP_404_NOT_FOUND)