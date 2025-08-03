import json
import os
from typing import Dict, Any

class Settings:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_settings = {
            "dark_theme": False,
            "start_with_windows": False,
            "warning_time": 300,  # 5 minutos em segundos
            "minimize_to_tray": True,
            "show_notifications": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Carrega as configurações do arquivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**self.default_settings, **json.load(f)}
            except Exception:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Salva as configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor de configuração"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Define um valor de configuração"""
        try:
            self.settings[key] = value
            return self.save_settings()
        except Exception:
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reseta todas as configurações para os valores padrão"""
        try:
            self.settings = self.default_settings.copy()
            return self.save_settings()
        except Exception:
            return False
    
    def update(self, settings_dict: Dict[str, Any]) -> bool:
        """Atualiza múltiplas configurações de uma vez"""
        try:
            self.settings.update(settings_dict)
            return self.save_settings()
        except Exception:
            return False
    
    def remove(self, key: str) -> bool:
        """Remove uma configuração específica"""
        try:
            if key in self.settings:
                del self.settings[key]
                return self.save_settings()
            return True  # Chave não existe, consideramos sucesso
        except Exception:
            return False 