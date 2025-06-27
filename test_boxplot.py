#!/usr/bin/env python3
import pandas as pd
import sys
import os
sys.path.append('src')

from visualizacao import GeradorGraficos

def main():
    print("🔍 TESTANDO BOXPLOTS")
    print("=" * 40)
    
    # Verificar se existem dados
    if not os.path.exists('data/resultados_experimento.csv'):
        print("❌ Arquivo de dados não encontrado!")
        return
    
    # Carregar dados
    df = pd.read_csv('data/resultados_experimento.csv')
    print(f"✅ Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    
    # Mostrar informações do DataFrame
    print(f"\n📊 Colunas disponíveis:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    # Mostrar valores únicos dos fatores
    if 'fator_c_algoritmo' in df.columns:
        print(f"\n🔧 Algoritmos: {df['fator_c_algoritmo'].unique()}")
    if 'fator_a_tamanho' in df.columns:
        print(f"📏 Tamanhos: {df['fator_a_tamanho'].unique()}")
    if 'fator_b_distribuicao' in df.columns:
        print(f"📈 Distribuições: {df['fator_b_distribuicao'].unique()}")
    
    # Gerar boxplot
    print(f"\n🎨 Gerando boxplots...")
    try:
        viz = GeradorGraficos()
        viz.grafico_boxplot(df)
        print("✅ Boxplots gerados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao gerar boxplots: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
