"""
Módulo para geração de visualizações e gráficos dos resultados dos benchmarks.
Implementa gráficos profissionais para análise de        # Por algoritmo
        if 'algoritmo' in df.columns:
            sns.boxplot(data=df, x='algoritmo', y='tempo_medio', ax=axes[0,0], hue='algoritmo', 
                       palette=self.cores[:len(df['algoritmo'].unique())], legend=False)
            axes[0,0].set_title('🏆 Distribuição dos Tempos por Algoritmo', fontweight='bold')
            axes[0,0].set_xlabel('Algoritmo')
            axes[0,0].set_ylabel('Tempo de Execução (s)')
        
        # Por tamanho
        col_tamanho = self._obter_nome_coluna(df, ['tamanho', 'tamanho_dados'])
        if col_tamanho:
            sns.boxplot(data=df, x=col_tamanho, y='tempo_medio', ax=axes[0,1], hue=col_tamanho,
                       palette=self.cores[:len(df[col_tamanho].unique())], legend=False)
            axes[0,1].set_title('Distribuição dos Tempos por Tamanho', fontweight='bold')
            axes[0,1].set_xlabel('Tamanho dos Dados')
            axes[0,1].set_ylabel('Tempo de Execução (s)')de algoritmos.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import os
import logging
from datetime import datetime

# Imports de bibliotecas de visualização
# Nota: Estas dependências são instaladas no ambiente Docker
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import plotly.graph_objects as go  # type: ignore
import plotly.express as px  # type: ignore
from plotly.subplots import make_subplots  # type: ignore
import warnings

# Configurar estilo dos gráficos e suprimir warnings de fontes
plt.style.use('default')
sns.set_palette("husl")
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']

class GeradorGraficos:
    """Classe para gerar visualizações dos resultados dos benchmarks"""
    
    def __init__(self, tema: str = 'gaming'):
        """
        Inicializar gerador com tema específico
        
        Args:
            tema: Tema visual ('gaming', 'scientific', 'corporate')
        """
        self.tema = tema
        self.logger = logging.getLogger(__name__)
        self.cores_gaming = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']  # Reduzido para 4 cores
        self.dpi = 300
        
        # Verificar disponibilidade das bibliotecas (informativo apenas)
        self.logger.info("Inicializando gerador de gráficos...")
        
        # Configurar tema
        if tema == 'gaming':
            plt.style.use('dark_background')
            self.cores = self.cores_gaming
        else:
            self.cores = sns.color_palette("husl", 4)  # Reduzido para 4 cores
            
        # Criar diretório de plots
        os.makedirs('plots', exist_ok=True)
        
    def _obter_nome_coluna(self, df: pd.DataFrame, preferencias: List[str]) -> Optional[str]:
        """Obter o nome correto da coluna baseado em preferências"""
        for nome in preferencias:
            if nome in df.columns:
                return nome
        return None

    def gerar_todos(self, resultados):
        """
        Gerar todos os gráficos principais
        
        Args:
            resultados: Lista com resultados dos benchmarks
        """
        self.logger.info("Gerando todas as visualizações")
        
        # Converter para DataFrame se necessário
        if isinstance(resultados, list):
            df = pd.DataFrame(resultados)
        else:
            df = resultados
        
        # Gerar gráficos principais
        self.grafico_barras_comparativo(df)
        self.grafico_boxplot(df)
        self.grafico_linhas_escalabilidade(df)
        self.heatmap_correlacao(df)
        self.grafico_interacao_fatores(df)
        self.grafico_distribuicao_tempos(df)
        self.grafico_throughput(df)
        self.grafico_memoria_vs_tempo(df)
        
        # Gráficos interativos com Plotly
        self.grafico_interativo_3d(df)
        self.dashboard_interativo(df)
        
        # Relatório visual completo
        self.gerar_relatorio_visual(df)
        
        self.logger.info("Todas as visualizações foram geradas")
    
    def grafico_barras_comparativo(self, df: pd.DataFrame):
        """Gráfico de barras comparativo entre algoritmos"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Por tamanho
        col_tamanho = self._obter_nome_coluna(df, ['tamanho', 'tamanho_dados'])
        if col_tamanho and 'algoritmo' in df.columns:
            dados_pivot = df.pivot_table(values='tempo_medio', index=col_tamanho, 
                                       columns='algoritmo', aggfunc='mean')
            
            dados_pivot.plot(kind='bar', ax=axes[0], color=self.cores[:len(dados_pivot.columns)])
            axes[0].set_title('Tempo Médio por Tamanho dos Dados', fontsize=14, fontweight='bold')
            axes[0].set_xlabel('Tamanho dos Dados')
            axes[0].set_ylabel('Tempo (segundos)')
            axes[0].legend(title='Algoritmo')
            axes[0].tick_params(axis='x', rotation=45)
        
        # Por tipo de dados
        if 'tipo_dado' in df.columns:
            dados_pivot2 = df.pivot_table(values='tempo_medio', index='tipo_dado', 
                                        columns='algoritmo', aggfunc='mean')
            
            dados_pivot2.plot(kind='bar', ax=axes[1], color=self.cores[:len(dados_pivot2.columns)])
            axes[1].set_title('Tempo Médio por Tipo de Distribuição', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Tipo de Distribuição')
            axes[1].set_ylabel('Tempo (segundos)')
            axes[1].legend(title='Algoritmo')
            axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Adicionar anotações com contexto de jogos
        fig.text(0.5, 0.02, 'Contexto: Análise de performance para rankings de jogadores online', 
                ha='center', fontsize=10, style='italic')
        
        plt.savefig('plots/comparativo_barras.png', dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico de barras comparativo salvo")
    
    def grafico_boxplot(self, df: pd.DataFrame):
        """Box plots para análise de distribuição dos tempos"""
        # Debug: mostrar colunas disponíveis
        self.logger.info(f"DEBUG Boxplot - Colunas disponíveis: {list(df.columns)}")
        self.logger.info(f"DEBUG Boxplot - Shape do DataFrame: {df.shape}")
        
        # Verificar valores únicos em cada fator
        if 'fator_c_algoritmo' in df.columns:
            unique_algos = df['fator_c_algoritmo'].unique()
            self.logger.info(f"DEBUG Boxplot - Algoritmos únicos: {unique_algos}")
        
        if 'fator_a_tamanho' in df.columns:
            unique_tamanhos = df['fator_a_tamanho'].unique()
            self.logger.info(f"DEBUG Boxplot - Tamanhos únicos: {unique_tamanhos}")
            
        if 'fator_b_distribuicao' in df.columns:
            unique_distribuicoes = df['fator_b_distribuicao'].unique()
            self.logger.info(f"DEBUG Boxplot - Distribuições únicas: {unique_distribuicoes}")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise de Distribuição dos Tempos de Execução', fontsize=16, fontweight='bold')
        
        # Por algoritmo
        if 'fator_c_algoritmo' in df.columns and len(df['fator_c_algoritmo'].unique()) > 1:
            try:
                sns.boxplot(data=df, x='fator_c_algoritmo', y='tempo_medio', hue='fator_c_algoritmo', ax=axes[0,0], 
                           palette=self.cores[:len(df['fator_c_algoritmo'].unique())], legend=False)
                axes[0,0].set_title('Distribuição dos Tempos por Algoritmo', fontweight='bold')
                axes[0,0].set_xlabel('Algoritmo')
                axes[0,0].set_ylabel('Tempo (segundos)')
                axes[0,0].tick_params(axis='x', rotation=45)
                self.logger.info("DEBUG - Subplot 1 (algoritmo) criado com sucesso")
            except Exception as e:
                self.logger.warning(f"DEBUG - Erro no subplot algoritmo: {e}")
                axes[0,0].text(0.5, 0.5, 'Dados insuficientes\npara algoritmos', 
                              ha='center', va='center', transform=axes[0,0].transAxes)
                axes[0,0].set_title('Distribuição por Algoritmo (Dados Insuficientes)')
        else:
            axes[0,0].text(0.5, 0.5, 'Coluna algoritmo\nnão encontrada', 
                          ha='center', va='center', transform=axes[0,0].transAxes)
            axes[0,0].set_title('Distribuição por Algoritmo (N/A)')
        
        # Por tamanho
        if 'fator_a_tamanho' in df.columns and len(df['fator_a_tamanho'].unique()) > 1:
            try:
                # Converter tamanhos para string para melhor visualização
                df_copy = df.copy()
                df_copy['fator_a_tamanho_str'] = df_copy['fator_a_tamanho'].astype(str)
                
                sns.boxplot(data=df_copy, x='fator_a_tamanho_str', y='tempo_medio', hue='fator_a_tamanho_str', ax=axes[0,1], 
                           palette=self.cores[:len(df_copy['fator_a_tamanho_str'].unique())], legend=False)
                axes[0,1].set_title('Distribuição dos Tempos por Tamanho', fontweight='bold')
                axes[0,1].set_xlabel('Tamanho dos Dados')
                axes[0,1].set_ylabel('Tempo (segundos)')
                axes[0,1].tick_params(axis='x', rotation=45)
                self.logger.info("DEBUG - Subplot 2 (tamanho) criado com sucesso")
            except Exception as e:
                self.logger.warning(f"DEBUG - Erro no subplot tamanho: {e}")
                axes[0,1].text(0.5, 0.5, 'Dados insuficientes\npara tamanhos', 
                              ha='center', va='center', transform=axes[0,1].transAxes)
                axes[0,1].set_title('Distribuição por Tamanho (Dados Insuficientes)')
        else:
            axes[0,1].text(0.5, 0.5, 'Coluna tamanho\nnão encontrada', 
                          ha='center', va='center', transform=axes[0,1].transAxes)
            axes[0,1].set_title('Distribuição por Tamanho (N/A)')
        
        # Por tipo de dados
        if 'fator_b_distribuicao' in df.columns and len(df['fator_b_distribuicao'].unique()) > 1:
            try:
                sns.boxplot(data=df, x='fator_b_distribuicao', y='tempo_medio', hue='fator_b_distribuicao', ax=axes[1,0], 
                           palette=self.cores[:len(df['fator_b_distribuicao'].unique())], legend=False)
                axes[1,0].set_title('Distribuição dos Tempos por Tipo de Dados', fontweight='bold')
                axes[1,0].set_xlabel('Tipo de Distribuição')
                axes[1,0].set_ylabel('Tempo (segundos)')
                axes[1,0].tick_params(axis='x', rotation=45)
                self.logger.info("DEBUG - Subplot 3 (distribuição) criado com sucesso")
            except Exception as e:
                self.logger.warning(f"DEBUG - Erro no subplot distribuição: {e}")
                axes[1,0].text(0.5, 0.5, 'Dados insuficientes\npara distribuições', 
                              ha='center', va='center', transform=axes[1,0].transAxes)
                axes[1,0].set_title('Distribuição por Tipo de Dados (Dados Insuficientes)')
        else:
            axes[1,0].text(0.5, 0.5, 'Coluna distribuição\nnão encontrada', 
                          ha='center', va='center', transform=axes[1,0].transAxes)
            axes[1,0].set_title('Distribuição por Tipo de Dados (N/A)')
        
        # Violin plot combinado - interação entre algoritmo e tipo de dados
        if ('fator_c_algoritmo' in df.columns and 'fator_b_distribuicao' in df.columns and 
            len(df['fator_c_algoritmo'].unique()) > 1 and len(df['fator_b_distribuicao'].unique()) > 1):
            try:
                sns.violinplot(data=df, x='fator_c_algoritmo', y='tempo_medio', hue='fator_b_distribuicao', 
                              ax=axes[1,1], palette=self.cores[:len(df['fator_b_distribuicao'].unique())])
                axes[1,1].set_title('Densidade dos Tempos: Algoritmo × Distribuição', fontweight='bold')
                axes[1,1].set_xlabel('Algoritmo')
                axes[1,1].set_ylabel('Tempo (segundos)')
                axes[1,1].tick_params(axis='x', rotation=45)
                self.logger.info("DEBUG - Subplot 4 (violin plot) criado com sucesso")
            except Exception as e:
                self.logger.warning(f"DEBUG - Erro no violin plot: {e}")
                axes[1,1].text(0.5, 0.5, 'Dados insuficientes para\ninteração algoritmo×distribuição', 
                              ha='center', va='center', transform=axes[1,1].transAxes)
                axes[1,1].set_title('Interação Algoritmo × Distribuição (Dados Insuficientes)')
        else:
            axes[1,1].text(0.5, 0.5, 'Colunas para interação\nnão encontradas', 
                          ha='center', va='center', transform=axes[1,1].transAxes)
            axes[1,1].set_title('Interação Algoritmo × Distribuição (N/A)')
        
        plt.tight_layout()
        
        # Adicionar explicação dos boxplots
        fig.text(0.5, 0.02, 
                'EXPLICAÇÃO DOS BOXPLOTS: Cada subplot mostra a distribuição dos tempos de execução por diferentes fatores.\n'
                'Superior Esquerdo: Comparação entre algoritmos | Superior Direito: Comparação entre tamanhos de dados\n'
                'Inferior Esquerdo: Comparação entre tipos de distribuição | Inferior Direito: Interação algoritmo × distribuição',
                ha='center', fontsize=9, style='italic', wrap=True)
        
        plt.savefig('plots/boxplots_distribuicao.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Box plots salvos com explicação detalhada")
    
    def grafico_linhas_escalabilidade(self, df: pd.DataFrame):
        """Gráfico de linhas mostrando escalabilidade dos algoritmos"""
        col_tamanho = self._obter_nome_coluna(df, ['tamanho', 'tamanho_dados'])
        if not col_tamanho or 'algoritmo' not in df.columns:
            return
            
        plt.figure(figsize=(12, 8))
        
        for i, algoritmo in enumerate(df['algoritmo'].unique()):
            dados_algo = df[df['algoritmo'] == algoritmo]
            
            # Agrupar por tamanho e calcular média
            escalabilidade = dados_algo.groupby(col_tamanho)['tempo_medio'].agg(['mean', 'std']).reset_index()
            
            plt.errorbar(escalabilidade[col_tamanho], escalabilidade['mean'], 
                        yerr=escalabilidade['std'], label=algoritmo, 
                        marker='o', linewidth=2, markersize=8, color=self.cores[i])
        
        plt.title('⚡ Análise de Escalabilidade dos Algoritmos', fontsize=16, fontweight='bold')
        plt.xlabel('Tamanho dos Dados (número de elementos)', fontsize=12)
        plt.ylabel('Tempo de Execução (segundos)', fontsize=12)
        plt.legend(title='Algoritmo', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')  # Escala logarítmica para melhor visualização
        plt.xscale('log')
        
        # Adicionar anotações de complexidade teórica
        plt.text(0.02, 0.98, 'Complexidades Teóricas:\\n• Merge Sort: O(n log n)\\n• Quick Sort: O(n log n) médio', 
                transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('plots/escalabilidade_algoritmos.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico de escalabilidade salvo")
    
    def heatmap_correlacao(self, df: pd.DataFrame):
        """Heatmap de correlações entre variáveis numéricas"""
        # Selecionar apenas colunas numéricas
        colunas_numericas = df.select_dtypes(include=[np.number]).columns
        
        if len(colunas_numericas) < 2:
            return
        
        plt.figure(figsize=(10, 8))
        
        # Calcular matriz de correlação
        matriz_corr = df[colunas_numericas].corr()
        
        # Criar heatmap
        sns.heatmap(matriz_corr, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        
        plt.title('Matriz de Correlação entre Métricas', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('plots/heatmap_correlacao.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Heatmap de correlação salvo")
    
    def grafico_interacao_fatores(self, df: pd.DataFrame):
        """Gráfico de interação entre fatores do experimento"""
        
        # Verificar colunas necessárias
        if not all(col in df.columns for col in ['fator_c_algoritmo', 'fator_a_tamanho', 'fator_b_distribuicao']):
            self.logger.warning("Colunas necessárias não encontradas para gráfico de interação")
            return
            
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Interação Algoritmo x Tamanho
        for algoritmo in df['fator_c_algoritmo'].unique():
            dados_algo = df[df['fator_c_algoritmo'] == algoritmo]
            medias_por_tamanho = dados_algo.groupby('fator_a_tamanho')['tempo_medio'].mean()
            
            axes[0].plot(medias_por_tamanho.index, medias_por_tamanho.values, 
                        marker='o', linewidth=2, markersize=8, label=algoritmo)
        
        axes[0].set_title('Interação: Algoritmo × Tamanho', fontweight='bold')
        axes[0].set_xlabel('Tamanho dos Dados')
        axes[0].set_ylabel('Tempo Médio (segundos)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Interação Algoritmo x Tipo de Dados
        dados_pivot = df.pivot_table(values='tempo_medio', index='fator_b_distribuicao', 
                                   columns='fator_c_algoritmo', aggfunc='mean')
        
        for algoritmo in dados_pivot.columns:
            axes[1].plot(range(len(dados_pivot.index)), dados_pivot[algoritmo], 
                        marker='o', linewidth=2, markersize=8, label=algoritmo)
        
        axes[1].set_title('Interação: Algoritmo × Tipo de Distribuição', fontweight='bold')
        axes[1].set_xlabel('Tipo de Distribuição')
        axes[1].set_ylabel('Tempo Médio (segundos)')
        axes[1].set_xticks(range(len(dados_pivot.index)))
        axes[1].set_xticklabels(dados_pivot.index, rotation=45)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('plots/interacao_fatores.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico de interação de fatores salvo")
    
    def grafico_distribuicao_tempos(self, df: pd.DataFrame):
        """Gráfico de distribuição dos tempos de execução"""
        if 'tempo_medio' not in df.columns:
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Histograma geral
        axes[0,0].hist(df['tempo_medio'], bins=20, alpha=0.7, color=self.cores[0], edgecolor='black')
        axes[0,0].set_title('Distribuição Geral dos Tempos', fontweight='bold')
        axes[0,0].set_xlabel('Tempo (segundos)')
        axes[0,0].set_ylabel('Frequência')
        
        # Histograma por algoritmo
        if 'algoritmo' in df.columns:
            for i, algoritmo in enumerate(df['algoritmo'].unique()):
                dados_algo = df[df['algoritmo'] == algoritmo]['tempo_medio']
                axes[0,1].hist(dados_algo, bins=15, alpha=0.6, label=algoritmo, 
                              color=self.cores[i], edgecolor='black')
            
            axes[0,1].set_title('Distribuição por Algoritmo', fontweight='bold')
            axes[0,1].set_xlabel('Tempo (segundos)')
            axes[0,1].set_ylabel('Frequência')
            axes[0,1].legend()
        
        # Q-Q plot para normalidade
        from scipy import stats
        stats.probplot(df['tempo_medio'], dist="norm", plot=axes[1,0])
        axes[1,0].set_title('Q-Q Plot (Teste de Normalidade)', fontweight='bold')
        
        # Densidade por algoritmo
        if 'algoritmo' in df.columns:
            for i, algoritmo in enumerate(df['algoritmo'].unique()):
                dados_algo = df[df['algoritmo'] == algoritmo]['tempo_medio']
                axes[1,1].hist(dados_algo, bins=15, alpha=0.5, density=True, 
                              label=algoritmo, color=self.cores[i])
                
                # Adicionar curva de densidade
                from scipy.stats import gaussian_kde
                densidade = gaussian_kde(dados_algo)
                x_range = np.linspace(dados_algo.min(), dados_algo.max(), 100)
                axes[1,1].plot(x_range, densidade(x_range), color=self.cores[i], linewidth=2)
            
            axes[1,1].set_title('Curvas de Densidade', fontweight='bold')
            axes[1,1].set_xlabel('Tempo (segundos)')
            axes[1,1].set_ylabel('Densidade')
            axes[1,1].legend()
        
        plt.tight_layout()
        plt.savefig('plots/distribuicao_tempos.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico de distribuição dos tempos salvo")
    
    def grafico_throughput(self, df: pd.DataFrame):
        """Gráfico de throughput (elementos processados por segundo)"""
        col_tamanho = self._obter_nome_coluna(df, ['tamanho', 'tamanho_dados'])
        
        if 'throughput_medio' not in df.columns and col_tamanho and 'tempo_medio' in df.columns:
            # Calcular throughput se não existir
            df['throughput_calculado'] = df[col_tamanho] / df['tempo_medio']
            coluna_throughput = 'throughput_calculado'
        else:
            coluna_throughput = 'throughput_medio'
            
        if coluna_throughput not in df.columns:
            return
            
        plt.figure(figsize=(12, 8))
        
        if 'algoritmo' in df.columns and col_tamanho:
            dados_pivot = df.pivot_table(values=coluna_throughput, index=col_tamanho, 
                                       columns='algoritmo', aggfunc='mean')
            
            for i, algoritmo in enumerate(dados_pivot.columns):
                plt.plot(dados_pivot.index, dados_pivot[algoritmo], 
                        marker='o', linewidth=2, markersize=8, 
                        label=algoritmo, color=self.cores[i])
        
        plt.title('⚡ Throughput dos Algoritmos (Elementos/segundo)', fontsize=14, fontweight='bold')
        plt.xlabel('Tamanho dos Dados')
        plt.ylabel('Throughput (elementos/segundo)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        
        # Adicionar contexto de jogos
        plt.text(0.02, 0.02, 'Contexto: Velocidade de processamento para atualizações de ranking em tempo real', 
                transform=plt.gca().transAxes, fontsize=10, style='italic',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('plots/throughput_algoritmos.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico de throughput salvo")
    
    def grafico_memoria_vs_tempo(self, df: pd.DataFrame):
        """Gráfico scatter de memória vs tempo"""
        if 'memoria_media' not in df.columns or 'tempo_medio' not in df.columns:
            return
            
        plt.figure(figsize=(10, 8))
        
        if 'algoritmo' in df.columns:
            for i, algoritmo in enumerate(df['algoritmo'].unique()):
                dados_algo = df[df['algoritmo'] == algoritmo]
                plt.scatter(dados_algo['tempo_medio'], dados_algo['memoria_media'], 
                           label=algoritmo, alpha=0.7, s=100, color=self.cores[i])
        
        plt.title('Relação Tempo vs Uso de Memória', fontsize=14, fontweight='bold')
        plt.xlabel('Tempo de Execução (segundos)')
        plt.ylabel('Uso de Memória (MB)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Adicionar linha de tendência
        from scipy.stats import linregress  # type: ignore
        linregress_result = linregress(df['tempo_medio'], df['memoria_media'])
        slope = float(linregress_result.slope)  # type: ignore
        intercept = float(linregress_result.intercept)  # type: ignore
        r_value = float(linregress_result.rvalue)  # type: ignore
        line = slope * df['tempo_medio'] + intercept
        plt.plot(df['tempo_medio'], line, 'r--', alpha=0.5, 
                label=f'Tendência (R² = {r_value**2:.3f})')
        
        plt.tight_layout()
        plt.savefig('plots/memoria_vs_tempo.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Gráfico memória vs tempo salvo")
    
    def grafico_interativo_3d(self, df: pd.DataFrame):
        """Gráfico 3D interativo com Plotly"""
        if not all(col in df.columns for col in ['tamanho', 'tempo_medio', 'algoritmo']):
            return
            
        fig = go.Figure()
        
        for algoritmo in df['algoritmo'].unique():
            dados_algo = df[df['algoritmo'] == algoritmo]
            
            fig.add_trace(go.Scatter3d(
                x=dados_algo['tamanho'],
                y=dados_algo.get('memoria_media', [0] * len(dados_algo)),
                z=dados_algo['tempo_medio'],
                mode='markers',
                marker=dict(size=8, opacity=0.7),
                name=algoritmo,
                text=[f'Algoritmo: {algoritmo}<br>Tamanho: {t}<br>Tempo: {tm:.4f}s' 
                      for t, tm in zip(dados_algo['tamanho'], dados_algo['tempo_medio'])],
                hovertemplate='%{text}<extra></extra>'
            ))
        
        fig.update_layout(
            title='Visualização 3D: Tamanho × Memória × Tempo',
            scene=dict(
                xaxis_title='Tamanho dos Dados',
                yaxis_title='Uso de Memória (MB)',
                zaxis_title='Tempo de Execução (s)'
            ),
            font=dict(size=12)
        )
        
        fig.write_html('plots/grafico_3d_interativo.html')
        self.logger.info("Gráfico 3D interativo salvo")
    
    def dashboard_interativo(self, df: pd.DataFrame):
        """Criar dashboard interativo com múltiplos gráficos"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Tempo por Algoritmo', 'Escalabilidade', 'Distribuição', 'Comparação'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "histogram"}, {"type": "box"}]]
        )
        
        # Gráfico de barras
        if 'algoritmo' in df.columns:
            tempo_por_algo = df.groupby('algoritmo')['tempo_medio'].mean()
            fig.add_trace(
                go.Bar(x=tempo_por_algo.index, y=tempo_por_algo.values, name='Tempo Médio'),
                row=1, col=1
            )
        
        # Escalabilidade
        if 'tamanho' in df.columns and 'algoritmo' in df.columns:
            for algoritmo in df['algoritmo'].unique():
                dados_algo = df[df['algoritmo'] == algoritmo]
                fig.add_trace(
                    go.Scatter(x=dados_algo['tamanho'], y=dados_algo['tempo_medio'], 
                             mode='lines+markers', name=f'{algoritmo}'),
                    row=1, col=2
                )
        
        # Histograma
        fig.add_trace(
            go.Histogram(x=df['tempo_medio'], name='Distribuição'),
            row=2, col=1
        )
        
        # Box plot
        if 'algoritmo' in df.columns:
            for algoritmo in df['algoritmo'].unique():
                dados_algo = df[df['algoritmo'] == algoritmo]
                fig.add_trace(
                    go.Box(y=dados_algo['tempo_medio'], name=algoritmo),
                    row=2, col=2
                )
        
        fig.update_layout(
            title_text="Dashboard Interativo - Análise de Performance",
            showlegend=True,
            height=800
        )
        
        fig.write_html('plots/dashboard_interativo.html')
        self.logger.info("Dashboard interativo salvo")
    
    def gerar_relatorio_visual(self, df: pd.DataFrame):
        """Gerar relatório visual com todos os gráficos"""
        # Criar figura com múltiplos subplots
        fig = plt.figure(figsize=(20, 24))
        
        # Grid de subplots
        gs = fig.add_gridspec(6, 3, hspace=0.3, wspace=0.3)
        
        # Título principal
        fig.suptitle('RELATÓRIO VISUAL COMPLETO - ALGORITMOS DE ORDENAÇÃO EM JOGOS ONLINE', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # Subplot 1: Comparação geral
        ax1 = fig.add_subplot(gs[0, :2])
        col_tamanho = self._obter_nome_coluna(df, ['tamanho', 'tamanho_dados'])
        if 'algoritmo' in df.columns and col_tamanho:
            dados_pivot = df.pivot_table(values='tempo_medio', index=col_tamanho, 
                                       columns='algoritmo', aggfunc='mean')
            dados_pivot.plot(kind='bar', ax=ax1, color=self.cores)
            ax1.set_title('Comparação de Performance')
        
        # Adicionar mais subplots conforme necessário...
        
        plt.savefig('plots/relatorio_visual_completo.png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white' if self.tema != 'gaming' else 'black')
        plt.close()
        
        self.logger.info("Relatório visual completo salvo")
