#!/usr/bin/env python3
"""
Teste específico da distribuição exponencial
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import matplotlib.pyplot as plt
from geradores import GeradorDados

def teste_distribuicao_exponencial():
    """Teste detalhado da distribuição exponencial"""
    
    print("TESTE DETALHADO DA DISTRIBUIÇÃO EXPONENCIAL")
    print("=" * 60)
    
    # Inicializar gerador
    gerador = GeradorDados(seed=42)
    
    # Gerar amostra grande para análise estatística
    tamanho = 10000
    dados = gerador.gerar(tamanho, 'exponencial')
    
    # Análise estatística
    print(f"Análise de {tamanho} pontuações exponenciais:")
    print(f"   Mínimo:     {min(dados):,}")
    print(f"   Máximo:     {max(dados):,}")
    print(f"   Média:      {np.mean(dados):,.1f}")
    print(f"   Mediana:    {np.median(dados):,.1f}")
    print(f"   Desvio:     {np.std(dados):,.1f}")
    print(f"   λ esperado: {gerador.lambda_exp}")
    print(f"   Média teórica (1/λ): {1/gerador.lambda_exp:,.1f}")
    
    # Verificar propriedades da exponencial
    media_empirica = np.mean(dados)
    media_teorica = 1 / gerador.lambda_exp
    erro_relativo = abs(media_empirica - media_teorica) / media_teorica * 100
    
    print(f"\nVerificação teórica:")
    print(f"   Média empírica:  {media_empirica:,.1f}")
    print(f"   Média teórica:   {media_teorica:,.1f}")
    print(f"   Erro relativo:   {erro_relativo:.1f}%")
    
    # Verificar se a maioria dos valores são baixos (típico da exponencial)
    percentil_25 = np.percentile(dados, 25)
    percentil_75 = np.percentile(dados, 75)
    percentil_90 = np.percentile(dados, 90)
    
    print(f"\nDistribuição dos valores:")
    print(f"   25% dos valores ≤ {percentil_25:,.0f}")
    print(f"   75% dos valores ≤ {percentil_75:,.0f}")
    print(f"   90% dos valores ≤ {percentil_90:,.0f}")
    
    # Verificar se a característica da exponencial está presente (muitos valores baixos)
    valores_baixos = sum(1 for x in dados if x < media_empirica)
    percentual_baixos = valores_baixos / len(dados) * 100
    
    print(f"\nCaracterística exponencial:")
    print(f"   Valores abaixo da média: {valores_baixos:,} ({percentual_baixos:.1f}%)")
    print(f"   Esperado para exponencial: ~63.2%")
    
    # Avaliar resultado
    if 60 <= percentual_baixos <= 67:
        print("   DISTRIBUIÇÃO EXPONENCIAL CONFIRMADA!")
    else:
        print("    Distribuição pode não ser perfeitamente exponencial")
    
    print(f"\nPrimeiros 20 valores: {dados[:20]}")
    
    return dados

def comparar_com_uniforme():
    """Comparar distribuição exponencial com uniforme"""
    
    print("\nCOMPARAÇÃO: EXPONENCIAL vs UNIFORME")
    print("=" * 60)
    
    gerador = GeradorDados(seed=42)
    
    # Gerar dados exponenciais
    exp_data = gerador.gerar(5000, 'exponencial')
    
    # Gerar dados uniformes para comparação
    np.random.seed(42)
    uniform_data = np.random.randint(0, 10000, 5000).tolist()
    
    print(f"Exponencial - Média: {np.mean(exp_data):,.1f}, Mediana: {np.median(exp_data):,.1f}")
    print(f"Uniforme   - Média: {np.mean(uniform_data):,.1f}, Mediana: {np.median(uniform_data):,.1f}")
    
    # Verificar assimetria (skewness)
    from scipy import stats
    try:
        skew_exp = stats.skew(exp_data)
        skew_unif = stats.skew(uniform_data)
        
        print(f"\nAssimetria (Skewness):")
        print(f"   Exponencial: {skew_exp:.2f} (deve ser ~2.0)")
        print(f"   Uniforme:    {skew_unif:.2f} (deve ser ~0.0)")
        
        if skew_exp > 1.5:
            print("   Exponencial tem assimetria positiva correta!")
        else:
            print("   Assimetria da exponencial pode estar incorreta")
            
    except ImportError:
        print("   scipy não disponível para teste de skewness")

if __name__ == "__main__":
    # Executar testes
    dados_exp = teste_distribuicao_exponencial()
    
    try:
        comparar_com_uniforme()
    except ImportError as e:
        print(f"\nTeste de comparação requer scipy: {e}")
    
    print("\nTESTE CONCLUÍDO!")
