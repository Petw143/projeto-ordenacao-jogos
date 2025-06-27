#!/usr/bin/env python3
"""
Script de teste simples para verificar sintaxe do módulo analise.py
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Teste de importação
    print("Testando importação do módulo analise...")
    from analise import AnalisadorResultados
    print("✓ Módulo analise importado com sucesso")
    
    # Teste de instanciação
    print("Testando instanciação da classe...")
    analisador = AnalisadorResultados()
    print("✓ AnalisadorResultados instanciado com sucesso")
    
    # Verificar métodos principais
    print("Verificando métodos principais...")
    assert hasattr(analisador, 'analisar'), "Método 'analisar' não encontrado"
    assert hasattr(analisador, 'gerar_relatorio_markdown'), "Método 'gerar_relatorio_markdown' não encontrado"
    print("✓ Métodos principais disponíveis")
    
    print("\n🎉 Todos os testes de validação passaram!")
    print("O módulo analise.py está pronto para uso.")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulo: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro durante validação: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
