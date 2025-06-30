#!/usr/bin/env python3
"""
Teste específico da distribuição quase-ordenada com base uniforme
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from geradores import GeradorDados

def teste_quase_ordenado_uniforme():
    """Teste detalhado da distribuição quase-ordenada com base uniforme"""
    
    print("TESTE DA DISTRIBUIÇÃO QUASE-ORDENADA (BASE UNIFORME)")
    print("=" * 65)
    
    # Inicializar gerador
    gerador = GeradorDados(seed=42)
    
    # Gerar amostra para análise
    tamanho = 1000
    dados = gerador.gerar(tamanho, 'quase_ordenado')
    
    # Análise estatística
    print(f"Análise de {tamanho} pontuações quase-ordenadas:")
    print(f"   Mínimo:     {min(dados):,}")
    print(f"   Máximo:     {max(dados):,}")
    print(f"   Média:      {np.mean(dados):,.1f}")
    print(f"   Mediana:    {np.median(dados):,.1f}")
    print(f"   Desvio:     {np.std(dados):,.1f}")
    
    # Verificar ordenação (calcular quantos elementos estão na posição correta)
    dados_ordenados = sorted(dados)
    elementos_corretos = sum(1 for i, val in enumerate(dados) if val == dados_ordenados[i])
    percentual_correto = elementos_corretos / len(dados) * 100
    
    print(f"\nVerificação de ordenação:")
    print(f"   Elementos na posição correta: {elementos_corretos:,} ({percentual_correto:.1f}%)")
    print(f"   Esperado para 90% ordenado: ~90%")
    
    # Verificar se está próximo de 90% ordenado
    if 85 <= percentual_correto <= 95:
        print("   DISTRIBUIÇÃO QUASE-ORDENADA CONFIRMADA!")
    else:
        print("   Pode não estar adequadamente quase-ordenada")
    
    # Calcular inversões (pares fora de ordem)
    inversoes = 0
    for i in range(len(dados)):
        for j in range(i+1, len(dados)):
            if dados[i] > dados[j]:
                inversoes += 1
    
    total_pares = len(dados) * (len(dados) - 1) // 2
    percentual_inversoes = inversoes / total_pares * 100
    
    print(f"\nAnálise de inversões:")
    print(f"   Total de inversões: {inversoes:,}")
    print(f"   Total de pares: {total_pares:,}")
    print(f"   Percentual de inversões: {percentual_inversoes:.1f}%")
    print(f"   Esperado para quase-ordenado: 5-15%")
    
    # Verificar distribuição dos valores (deve favorecer valores menores por causa da transformação U²)
    valores_baixos = sum(1 for x in dados if x <= tamanho/3)
    valores_medios = sum(1 for x in dados if tamanho/3 < x <= 2*tamanho/3)
    valores_altos = sum(1 for x in dados if x > 2*tamanho/3)
    
    print(f"\nDistribuição por faixas:")
    print(f"   Valores baixos (≤{tamanho//3}): {valores_baixos} ({valores_baixos/len(dados)*100:.1f}%)")
    print(f"   Valores médios: {valores_medios} ({valores_medios/len(dados)*100:.1f}%)")
    print(f"   Valores altos (>{2*tamanho//3}): {valores_altos} ({valores_altos/len(dados)*100:.1f}%)")
    
    # Verificar se a transformação U² está funcionando (mais valores baixos)
    if valores_baixos > valores_altos:
        print("   TRANSFORMAÇÃO U² FUNCIONANDO (mais valores baixos)")
    else:
        print("   Transformação U² pode não estar funcionando corretamente")
    
    print(f"\nPrimeiros 20 valores: {dados[:20]}")
    print(f"Últimos 20 valores: {dados[-20:]}")
    
    return dados

def comparar_ordenacao():
    """Comparar quase-ordenado com dados completamente desordenados"""
    
    print("\nCOMPARAÇÃO: QUASE-ORDENADO vs ALEATÓRIO")
    print("=" * 55)
    
    gerador = GeradorDados(seed=42)
    
    # Gerar dados quase-ordenados
    quase_ord = gerador.gerar(1000, 'quase_ordenado')
    
    # Gerar dados completamente aleatórios
    np.random.seed(42)
    aleatorios = list(np.random.randint(1, 1001, 1000))
    
    # Calcular inversões para ambos
    def contar_inversoes(dados):
        inversoes = 0
        for i in range(len(dados)):
            for j in range(i+1, len(dados)):
                if dados[i] > dados[j]:
                    inversoes += 1
        return inversoes
    
    inv_quase = contar_inversoes(quase_ord)
    inv_alea = contar_inversoes(aleatorios)
    
    total_pares = 1000 * 999 // 2
    
    print(f"Quase-ordenado - Inversões: {inv_quase:,} ({inv_quase/total_pares*100:.1f}%)")
    print(f"Aleatório      - Inversões: {inv_alea:,} ({inv_alea/total_pares*100:.1f}%)")
    
    if inv_quase < inv_alea * 0.5:
        print("   Dados quase-ordenados têm significativamente menos inversões!")
    else:
        print("   Dados podem não estar adequadamente quase-ordenados")

if __name__ == "__main__":
    # Executar testes
    dados_quase = teste_quase_ordenado_uniforme()
    comparar_ordenacao()
    
    print("\nTESTE CONCLUÍDO!")
