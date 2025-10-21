from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_initial_users(apps, schema_editor):
    """
    Cria os usuários iniciais (joao, maria) e suas respectivas
    contas de correntista com saldo inicial.
    """
    
    User = apps.get_model('auth', 'User')
    Correntista = apps.get_model('core', 'Correntista')

    # --- Usuário 1: João ---
    joao_user, created = User.objects.get_or_create(
        username='joao',
        defaults={
            'first_name': 'João',
            'last_name': 'Silva',
            'email': 'joao@email.com',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('123456'),
        }
    )
    if created:
    
        Correntista.objects.create(
            user=joao_user,
            nome_correntista='João Silva',
            saldo=1500.00
        )
        print("Usuário 'joao' e sua conta foram criados.")


    # --- Usuário 2: Maria ---
    maria_user, created = User.objects.get_or_create(
        username='maria',
        defaults={
            'first_name': 'Maria',
            'last_name': 'Oliveira',
            'email': 'maria@email.com',
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('123456'),
        }
    )
    if created:
        
        Correntista.objects.create(
            user=maria_user,
            nome_correntista='Maria Oliveira',
            saldo=2500.00
        )
        print("Usuário 'maria' e sua conta foram criados.")

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]
