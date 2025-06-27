#!/usr/bin/env python3
"""
Script de teste para verificar se o módulo analise.py está funcionando
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from analise import AnalisadorResultados
    print("✓ Módulo analise importado com sucesso")
    
    # Teste básico de instanciação
    analisador = AnalisadorResultados()
    print("✓ AnalisadorResultados instanciado com sucesso")
    
    # Teste com dados simulados
    import pandas as pd
    import numpy as np
    
    # Criar dados de teste
    dados = {
        'algoritmo': ['merge_sort', 'quick_sort'] * 10,
        'tempo_execucao': np.random.uniform(0.1, 2.0, 20),
        'tamanho': [1000, 5000] * 10
    }
    df = pd.DataFrame(dados)
    
    # Testar análise
    analise = analisador.analisar(df)
    print("✓ Análise executada com sucesso")
    print(f"✓ Resultados da análise: {list(analise.keys())}")
    
    print("\n🎉 Todos os testes passaram! O módulo analise.py está funcionando corretamente.")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulo: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro durante teste: {e}")
    sys.exit(1)
