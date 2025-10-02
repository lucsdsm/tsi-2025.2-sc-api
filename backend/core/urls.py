from django.urls import path
from .views import ExtratoView

urlpatterns = [
    path('correntistas/<int:correntista_id>/extrato/', ExtratoView.as_view(), name='extrato-correntista'),
]