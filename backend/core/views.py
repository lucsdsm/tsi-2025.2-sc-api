from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import Movimentacao, Correntista
from .serializers import (
    MovimentacaoSerializer,
    OperacaoBasicaSerializer,
    PagamentoSerializer,
    TransferenciaSerializer
)

class ExtratoView(ListAPIView):
    """
    View para listar todas as movimentações de um correntista específico.
    Acesso via /api/correntistas/<id>/extrato/
    """
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        correntista_id = self.kwargs['correntista_id']
        return Movimentacao.objects.filter(correntista_id=correntista_id).order_by('-data_operacao')