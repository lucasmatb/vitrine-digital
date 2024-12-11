from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from usuarios.models import Usuario, Pedido_Lojista

class CriaPedidoLojistaPorUsuarioTestCase(TestCase):

    def setUp(self):
        # Cria um usuário de teste
        self.user = Usuario.objects.create_user(email='testuser@teste.com', password='testpassword')
        
        # Cria uma requisição simulada para a view
        self.client.login(email='testuser@teste.com', password='testpassword')

    def test_cria_pedido_lojista_com_ausencia_de_pedido_em_aberto(self):
        # Não há pedido em aberto para o usuário
        response = self.client.post(reverse('cria_pedido_lojista'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'success', 'message': 'Pedido criado com sucesso.'})
        
        # Verifique se o pedido foi criado no banco de dados
        pedido = Pedido_Lojista.objects.filter(id_usuario=self.user, status_pedido='Aguardando avaliação').first()
        self.assertIsNotNone(pedido)
        self.assertTrue(pedido.ativo)

    def test_cria_pedido_lojista_com_pedido_em_aberto(self):
        # Cria um pedido em aberto para o usuário
        Pedido_Lojista.objects.create(
            status_pedido='Aguardando avaliação',
            id_usuario=self.user,
            ativo=True
        )
        
        # Tentando criar um novo pedido
        response = self.client.post(reverse('cria_pedido_lojista'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'error', 'message': 'Você já tem um pedido em aberto.'})

    def test_cria_pedido_lojista_com_erro(self):
        # Simula um erro (por exemplo, algum campo obrigatório ausente)
        def mock_create(*args, **kwargs):
            raise Exception("Erro ao criar pedido")
        
        # Usar patch corretamente para simular a falha
        with patch('usuarios.views.Pedido_Lojista.objects.create', mock_create):
            response = self.client.post(reverse('cria_pedido_lojista')) 
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'error', 'message': 'Erro ao criar pedido'})