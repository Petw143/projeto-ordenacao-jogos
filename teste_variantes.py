"""
Teste Rápido das Variantes de Algoritmos
"""

import sys
import os
import time
import random

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.algoritmos_variantes import criar_algoritmos_principais
    print("✅ Módulo algoritmos_variantes importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def teste_rapido():
    """Teste rápido das variantes"""
    print("\n=== TESTE RÁPIDO DAS VARIANTES ===")
    
    # Criar algoritmos
    algoritmos = criar_algoritmos_principais(10)
    print(f"Algoritmos criados: {len(algoritmos)}")
    
    # Dados de teste pequenos
    dados_teste = random.sample(range(1, 1000), 100)
    
    resultados = []
    
    for alg in algoritmos:
        print(f"\nTestando: {alg.nome}")
        
        # Medir tempo
        inicio = time.perf_counter()
        resultado = alg.ordenar(dados_teste.copy())
        fim = time.perf_counter()
        
        tempo_ms = (fim - inicio) * 1000
        
        # Verificar se está ordenado
        esta_ordenado = resultado == sorted(dados_teste)
        
        print(f"  Tempo: {tempo_ms:.2f}ms")
        print(f"  Ordenado corretamente: {'✅' if esta_ordenado else '❌'}")
        
        resultados.append({
            'algoritmo': alg.nome,
            'tempo_ms': tempo_ms,
            'correto': esta_ordenado
        })
    
    print("\n=== RESUMO DOS RESULTADOS ===")
    resultados.sort(key=lambda x: x['tempo_ms'])
    
    for i, r in enumerate(resultados, 1):
        status = "✅" if r['correto'] else "❌"
        print(f"{i}. {r['algoritmo']}: {r['tempo_ms']:.2f}ms {status}")
    
    print(f"\nTeste concluído! {len(resultados)} algoritmos testados.")

if __name__ == "__main__":
    teste_rapido()
