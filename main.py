#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agendador de Desligamento v2.0

Ponto de entrada principal da aplicação.
Este arquivo serve como launcher para a interface principal do aplicativo.

Autor: Desenvolvido com boas práticas de código limpo
Versão: 2.0
"""

import sys
import os

# Adiciona o diretório src ao path para permitir imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main import main

if __name__ == "__main__":
    main()