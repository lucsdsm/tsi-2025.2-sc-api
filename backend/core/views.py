from rest_framework.generics import ListAPIView
from .models import Movimentacao
from .serializers import MovimentacaoSerializer

class MovimentacaoListView(ListAPIView):
    """
    Esta view exibe uma lista de todas as movimentações.
    """
    queryset = Movimentacao.objects.select_related('correntista', 'correntista_beneficiario').all()
    serializer_class = MovimentacaoSerializer