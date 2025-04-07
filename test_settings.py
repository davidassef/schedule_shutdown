#!/usr/bin/env python
"""
Testes unitários para o módulo settings do Agendador de Desligamento.
"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, mock_open

from settings import Settings


class TestSettings(unittest.TestCase):
    """Testes para a classe Settings"""

    def setUp(self):
        """Configuração executada antes de cada teste"""
        # Criar um arquivo temporário para os testes
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file_path = self.temp_file.name
        self.temp_file.close()

        # Configurações padrão esperadas
        self.default_settings = {
            "dark_theme": False,
            "start_with_windows": False,
            "warning_time": 300,
            "minimize_to_tray": True,
            "show_notifications": True
        }

    def tearDown(self):
        """Limpeza executada após cada teste"""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_init_default_settings(self):
        """Testa a inicialização com configurações padrão"""
        # Usar um arquivo que não existe para forçar carregamento dos padrões
        settings = Settings("arquivo_que_nao_existe.json")

        # Verificar se as configurações padrão foram carregadas
        for key, expected_value in self.default_settings.items():
            self.assertEqual(settings.get(key), expected_value)

    def test_init_existing_file(self):
        """Testa a inicialização com um arquivo existente"""
        # Criar arquivo de configuração com valores personalizados
        custom_settings = {
            "dark_theme": True,
            "warning_time": 600
        }

        with open(self.temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(custom_settings, f)

        # Inicializar com o arquivo temporário
        settings = Settings(self.temp_file_path)

        # Verificar se os valores foram carregados corretamente
        self.assertTrue(settings.get("dark_theme"))  # Personalizado
        self.assertEqual(settings.get("warning_time"), 600)  # Personalizado
        self.assertFalse(settings.get("start_with_windows"))  # Padrão
        self.assertTrue(settings.get("minimize_to_tray"))  # Padrão

    def test_load_settings_file_error(self):
        """Testa o carregamento quando há erro ao ler o arquivo"""
        with patch('builtins.open', side_effect=Exception('Erro ao abrir')):
            settings = Settings("qualquer_arquivo.json")

            # Deve usar configurações padrão em caso de erro
            for key, expected_value in self.default_settings.items():
                self.assertEqual(settings.get(key), expected_value)

    def test_save_settings(self):
        """Testa o salvamento das configurações"""
        # Inicializar com arquivo temporário
        settings = Settings(self.temp_file_path)

        # Modificar algumas configurações
        settings.set("dark_theme", True)
        settings.set("warning_time", 600)

        # Verificar se o arquivo foi salvo com as configurações corretas
        with open(self.temp_file_path, 'r', encoding='utf-8') as f:
            saved_settings = json.load(f)

        self.assertTrue(saved_settings["dark_theme"])
        self.assertEqual(saved_settings["warning_time"], 600)
        self.assertFalse(saved_settings["start_with_windows"])  # Valor padrão não alterado

    def test_save_settings_error(self):
        """Testa o salvamento quando há erro ao escrever o arquivo"""
        settings = Settings(self.temp_file_path)

        with patch('builtins.open', side_effect=Exception('Erro ao salvar')):
            result = settings.save_settings()
            self.assertFalse(result)  # Deve retornar False em caso de erro

    def test_get_existing_key(self):
        """Testa a obtenção de uma chave existente"""
        settings = Settings(self.temp_file_path)
        self.assertEqual(settings.get("warning_time"), 300)

    def test_get_nonexistent_key(self):
        """Testa a obtenção de uma chave inexistente"""
        settings = Settings(self.temp_file_path)

        # Sem valor padrão
        self.assertIsNone(settings.get("chave_inexistente"))

        # Com valor padrão
        self.assertEqual(settings.get("chave_inexistente", "valor_padrao"), "valor_padrao")

    def test_set_key(self):
        """Testa a definição de um valor"""
        settings = Settings(self.temp_file_path)

        # Definir um valor para uma chave existente
        result = settings.set("warning_time", 600)
        self.assertTrue(result)
        self.assertEqual(settings.get("warning_time"), 600)

        # Definir um valor para uma nova chave
        result = settings.set("nova_chave", "novo_valor")
        self.assertTrue(result)
        self.assertEqual(settings.get("nova_chave"), "novo_valor")

    def test_set_key_error(self):
        """Testa a definição quando há erro ao salvar"""
        settings = Settings(self.temp_file_path)

        with patch.object(Settings, 'save_settings', return_value=False):
            result = settings.set("warning_time", 600)
            self.assertFalse(result)  # Deve retornar False em caso de erro

    def test_reset_to_defaults(self):
        """Testa o reset para valores padrão"""
        # Inicializar e modificar algumas configurações
        settings = Settings(self.temp_file_path)
        settings.set("dark_theme", True)
        settings.set("warning_time", 600)
        settings.set("nova_chave", "novo_valor")

        # Resetar para os padrões
        result = settings.reset_to_defaults()
        self.assertTrue(result)

        # Verificar se os valores foram resetados
        self.assertFalse(settings.get("dark_theme"))
        self.assertEqual(settings.get("warning_time"), 300)
        self.assertIsNone(settings.get("nova_chave"))  # Chave personalizada deve ser removida

    def test_reset_to_defaults_error(self):
        """Testa o reset quando há erro ao salvar"""
        settings = Settings(self.temp_file_path)

        with patch.object(Settings, 'save_settings', return_value=False):
            result = settings.reset_to_defaults()
            self.assertFalse(result)  # Deve retornar False em caso de erro

    def test_update_settings(self):
        """Testa a atualização de múltiplas configurações"""
        settings = Settings(self.temp_file_path)

        # Atualizar várias configurações de uma vez
        updates = {
            "dark_theme": True,
            "warning_time": 600,
            "nova_chave": "novo_valor"
        }

        result = settings.update(updates)
        self.assertTrue(result)

        # Verificar se os valores foram atualizados
        self.assertTrue(settings.get("dark_theme"))
        self.assertEqual(settings.get("warning_time"), 600)
        self.assertEqual(settings.get("nova_chave"), "novo_valor")
        self.assertTrue(settings.get("minimize_to_tray"))  # Valor não alterado deve permanecer

    def test_update_settings_error(self):
        """Testa a atualização quando há erro ao salvar"""
        settings = Settings(self.temp_file_path)

        with patch.object(Settings, 'save_settings', return_value=False):
            result = settings.update({"dark_theme": True})
            self.assertFalse(result)  # Deve retornar False em caso de erro

    def test_remove_key(self):
        """Testa a remoção de uma configuração"""
        # Inicializar e adicionar uma chave personalizada
        settings = Settings(self.temp_file_path)
        settings.set("nova_chave", "novo_valor")

        # Remover a chave
        result = settings.remove("nova_chave")
        self.assertTrue(result)
        self.assertIsNone(settings.get("nova_chave"))  # Chave deve ser removida

    def test_remove_nonexistent_key(self):
        """Testa a remoção de uma chave inexistente"""
        settings = Settings(self.temp_file_path)

        # Tentar remover uma chave que não existe
        result = settings.remove("chave_inexistente")
        self.assertTrue(result)  # Deve retornar True, pois não há erro

    def test_remove_key_error(self):
        """Testa a remoção quando há erro ao salvar"""
        settings = Settings(self.temp_file_path)
        settings.set("nova_chave", "novo_valor")

        with patch.object(Settings, 'save_settings', return_value=False):
            result = settings.remove("nova_chave")
            self.assertFalse(result)  # Deve retornar False em caso de erro


if __name__ == "__main__":
    unittest.main()