from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ExtratoView,
    pagamento_view,
    transferencia_view,
    saque_view,
    deposito_view
)

urlpatterns = [
    # Rota para obter o token de autenticação
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Rotas GET para extrato
    path('extrato/', ExtratoView.as_view(), name='extrato'),
    # Rota POST para operações
    path('pagar/', pagamento_view, name='pagamento'),
    path('transferir/', transferencia_view, name='transferencia'),
    path('sacar/', saque_view, name='saque'),
    path('depositar/', deposito_view, name='deposito'),
]