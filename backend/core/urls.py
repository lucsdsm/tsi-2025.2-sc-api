from django.urls import path
from .views import ExtratoView
from .views import pagamento_view
from .views import transferencia_view
from .views import saque_view
from .views import deposito_view

urlpatterns = [
    # Rotas GET para extrato
    path('correntistas/<int:correntista_id>/extrato/', ExtratoView.as_view(), name='extrato-correntista'),

    # Rota POST para operações
    path('pagar/', pagamento_view, name='pagamento'),
    path('transferir/', transferencia_view, name='transferencia'),
    path('sacar/', saque_view, name='saque'),
    path('depositar/', deposito_view, name='deposito'),
]