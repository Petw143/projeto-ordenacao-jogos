#!/usr/bin/env python3
"""
Script para debug dos boxplots
"""

import pandas as pd
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar src ao path
sys.path.append('src')

try:
    from visualizacao import GeradorGraficos
    
    # Carregar dados
    df = pd.read_csv('data/resultados_experimento.csv')
    
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"Colunas: {list(df.columns)}")
    
    # Verificar valores únicos
    if 'fator_c_algoritmo' in df.columns:
        logger.info(f"Algoritmos únicos: {df['fator_c_algoritmo'].unique()}")
    
    if 'fator_a_tamanho' in df.columns:
        logger.info(f"Tamanhos únicos: {df['fator_a_tamanho'].unique()}")
        
    if 'fator_b_distribuicao' in df.columns:
        logger.info(f"Distribuições únicas: {df['fator_b_distribuicao'].unique()}")
    
    # Gerar boxplot
    viz = GeradorGraficos()
    viz.grafico_boxplot(df)
    
    logger.info("Boxplot gerado com sucesso!")
    
except Exception as e:
    logger.error(f"Erro: {e}")
    import traceback
    traceback.print_exc()
