from django.urls import path
from .views import MovimentacaoListView

urlpatterns = [
    path('movimentacoes/', MovimentacaoListView.as_view(), name='lista-movimentacoes'),
]