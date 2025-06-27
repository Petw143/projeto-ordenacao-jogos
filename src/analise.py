"""
Módulo para análise estatística dos resultados dos benchmarks.
Versão simplificada focada em funcionalidade.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from datetime import datetime
import os

class AnalisadorResultados:
    """Classe para análise estatística dos resultados dos benchmarks"""
    
    def __init__(self):
        """Inicializar analisador com configurações padrão"""
        self.logger = logging.getLogger(__name__)
        self.alpha = 0.05  # Nível de significância
        
    def analisar(self, resultados) -> Dict[str, Any]:
        """
        Executar análise completa dos resultados
        
        Args:
            resultados: Lista com resultados dos benchmarks ou DataFrame
            
        Returns:
            Dicionário com todas as análises
        """
        self.logger.info("Iniciando análise estatística dos resultados")
        
        # Converter para DataFrame
        if isinstance(resultados, list):
            df = pd.DataFrame(resultados)
        else:
            df = resultados
            
        analise = {
            'timestamp': datetime.now().isoformat(),
            'total_experimentos': len(df),
            'estatisticas_descritivas': self._estatisticas_descritivas(df),
            'analise_variancia': self._analise_variancia_simples(df),
            'analise_correlacao': self._analise_correlacao_simples(df),
            'outliers': self._detectar_outliers_simples(df),
            'resumo_conclusoes': self._gerar_conclusoes(df)
        }
        
        self.logger.info("Análise estatística concluída")
        return analise
    
    def _estatisticas_descritivas(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcular estatísticas descritivas por fator"""
        stats_desc = {}
        
        # Por algoritmo
        if 'algoritmo' in df.columns or 'fator_c_algoritmo' in df.columns:
            col_algo = 'algoritmo' if 'algoritmo' in df.columns else 'fator_c_algoritmo'
            col_tempo = 'tempo_medio' if 'tempo_medio' in df.columns else 'tempo_execucao'
            
            if col_tempo in df.columns:
                stats_desc['por_algoritmo'] = {}
                for algo in df[col_algo].unique():
                    dados_algo = df[df[col_algo] == algo][col_tempo]
                    if len(dados_algo) > 0:
                        stats_desc['por_algoritmo'][str(algo)] = {
                            'media': float(dados_algo.mean()),
                            'desvio_padrao': float(dados_algo.std()),
                            'mediana': float(dados_algo.median()),
                            'min': float(dados_algo.min()),
                            'max': float(dados_algo.max()),
                            'coef_variacao': float(dados_algo.std() / dados_algo.mean() * 100) if dados_algo.mean() != 0 else 0
                        }
        
        # Por tamanho
        if 'tamanho' in df.columns or 'fator_a_tamanho' in df.columns:
            col_tam = 'tamanho' if 'tamanho' in df.columns else 'fator_a_tamanho'
            col_tempo = 'tempo_medio' if 'tempo_medio' in df.columns else 'tempo_execucao'
            
            if col_tempo in df.columns:
                stats_desc['por_tamanho'] = {}
                for tamanho in df[col_tam].unique():
                    dados_tam = df[df[col_tam] == tamanho][col_tempo]
                    if len(dados_tam) > 0:
                        stats_desc['por_tamanho'][str(tamanho)] = {
                            'media': float(dados_tam.mean()),
                            'desvio_padrao': float(dados_tam.std()),
                            'mediana': float(dados_tam.median())
                        }
        
        return stats_desc
    
    def _analise_variancia_simples(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Executar ANOVA simples para identificar efeitos"""
        anova_results = {}
        
        try:
            # Identificar colunas
            col_algo = 'algoritmo' if 'algoritmo' in df.columns else 'fator_c_algoritmo'
            col_tempo = 'tempo_medio' if 'tempo_medio' in df.columns else 'tempo_execucao'
            
            if col_algo in df.columns and col_tempo in df.columns:
                algoritmos = df[col_algo].unique()
                if len(algoritmos) > 1:
                    # Cálculo manual de F-statistic simples
                    grupos = []
                    for algo in algoritmos:
                        dados_grupo = df[df[col_algo] == algo][col_tempo].values
                        if len(dados_grupo) > 0:
                            grupos.append(dados_grupo)
                    
                    if len(grupos) > 1:
                        # Média geral
                        todos_dados = np.concatenate(grupos)
                        media_geral = float(np.mean(todos_dados))
                        n_total = len(todos_dados)
                        
                        # Soma dos quadrados entre grupos
                        sq_entre = 0.0
                        for grupo in grupos:
                            media_grupo = float(np.mean(grupo))
                            sq_entre += len(grupo) * (media_grupo - media_geral) ** 2
                        
                        # Soma dos quadrados dentro dos grupos
                        sq_dentro = 0.0
                        for grupo in grupos:
                            media_grupo = float(np.mean(grupo))
                            sq_dentro += float(np.sum((grupo - media_grupo) ** 2))
                        
                        # Graus de liberdade
                        gl_entre = len(grupos) - 1
                        gl_dentro = n_total - len(grupos)
                        
                        # F-statistic
                        if gl_dentro > 0 and sq_dentro > 0:
                            mq_entre = float(sq_entre / gl_entre)
                            mq_dentro = float(sq_dentro / gl_dentro)
                            f_stat = float(mq_entre / mq_dentro)
                            
                            anova_results['algoritmo'] = {
                                'f_statistic': float(f_stat),
                                'significativo': f_stat > 4.0,  # Aproximação simples
                                'interpretacao': 'Há diferença significativa entre algoritmos' if f_stat > 4.0 else 'Não há diferença significativa entre algoritmos'
                            }
            
        except Exception as e:
            self.logger.warning(f"Erro ao calcular ANOVA: {e}")
            anova_results['erro'] = str(e)
        
        return anova_results
    
    def _analise_correlacao_simples(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcular correlações simples entre variáveis numéricas"""
        correlacoes = {}
        
        try:
            # Selecionar apenas colunas numéricas
            colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(colunas_numericas) > 1:
                # Matriz de correlação simples
                corr_matrix = df[colunas_numericas].corr()
                correlacoes['matriz'] = corr_matrix.round(3).to_dict()
                
                # Correlações mais fortes
                correlacoes['fortes'] = {}
                for i, col1 in enumerate(colunas_numericas):
                    for col2 in colunas_numericas[i+1:]:
                        corr_val = corr_matrix.loc[col1, col2]
                        # Verificar se o valor é válido (não NaN)
                        if pd.notna(corr_val) and isinstance(corr_val, (int, float)):
                            corr_float = float(corr_val)
                            if abs(corr_float) > 0.5:  # Correlação moderada a forte
                                correlacoes['fortes'][f"{col1}_vs_{col2}"] = {
                                    'correlacao': corr_float,
                                    'interpretacao': self._interpretar_correlacao(corr_float)
                                }
            
        except Exception as e:
            self.logger.warning(f"Erro ao calcular correlações: {e}")
            correlacoes['erro'] = str(e)
        
        return correlacoes
    
    def _interpretar_correlacao(self, r: float) -> str:
        """Interpretar força da correlação"""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "Correlação negligível"
        elif abs_r < 0.3:
            return "Correlação fraca"
        elif abs_r < 0.5:
            return "Correlação moderada"
        elif abs_r < 0.7:
            return "Correlação forte"
        else:
            return "Correlação muito forte"
    
    def _detectar_outliers_simples(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detectar outliers usando método IQR simplificado"""
        outliers = {}
        
        try:
            col_tempo = 'tempo_medio' if 'tempo_medio' in df.columns else 'tempo_execucao'
            
            if col_tempo in df.columns:
                # Converter para array numpy para garantir compatibilidade
                dados_series = df[col_tempo]
                dados = np.array(dados_series.tolist(), dtype=float)
                
                # Usar pandas quantile que é mais confiável
                Q1 = float(dados_series.quantile(0.25))
                Q3 = float(dados_series.quantile(0.75))
                IQR = Q3 - Q1
                
                limite_inferior = Q1 - 1.5 * IQR
                limite_superior = Q3 + 1.5 * IQR
                
                # Usar operações numpy com array convertido
                outliers_mask = (dados < limite_inferior) | (dados > limite_superior)
                outliers_indices_tuple = np.where(outliers_mask)
                outliers_indices = outliers_indices_tuple[0] if len(outliers_indices_tuple) > 0 else np.array([], dtype=int)
                
                outliers[col_tempo] = {
                    'quantidade': int(len(outliers_indices)),
                    'percentual': float(len(outliers_indices) / len(dados) * 100) if len(dados) > 0 else 0.0,
                    'limite_inferior': float(limite_inferior),
                    'limite_superior': float(limite_superior),
                    'valores_outliers': [float(x) for x in dados[outliers_indices][:10]] if len(outliers_indices) > 0 else []
                }
            
        except Exception as e:
            self.logger.warning(f"Erro ao detectar outliers: {e}")
            outliers['erro'] = str(e)
        
        return outliers
    
    def _gerar_conclusoes(self, df: pd.DataFrame) -> List[str]:
        """Gerar conclusões principais da análise"""
        conclusoes = []
        
        try:
            # Identificar colunas
            col_algo = 'algoritmo' if 'algoritmo' in df.columns else 'fator_c_algoritmo'
            col_tempo = 'tempo_medio' if 'tempo_medio' in df.columns else 'tempo_execucao'
            col_tam = 'tamanho' if 'tamanho' in df.columns else 'fator_a_tamanho'
            
            # Algoritmo mais rápido
            if col_algo in df.columns and col_tempo in df.columns:
                tempo_por_algo = df.groupby(col_algo)[col_tempo].mean()
                mais_rapido = str(tempo_por_algo.idxmin())
                mais_lento = str(tempo_por_algo.idxmax())
                
                tempo_rapido = float(tempo_por_algo[mais_rapido])
                tempo_lento = float(tempo_por_algo[mais_lento])
                diferenca_perc = float(((tempo_lento - tempo_rapido) / tempo_rapido * 100))
                
                conclusoes.append(f"O algoritmo {mais_rapido} foi o mais rápido, sendo {diferenca_perc:.1f}% mais rápido que {mais_lento}")
            
            # Efeito do tamanho
            if col_tam in df.columns:
                tamanhos = df[col_tam].unique()
                if len(tamanhos) > 1:
                    tamanhos_list = sorted([int(x) if isinstance(x, (int, float)) else x for x in tamanhos])
                    conclusoes.append(f"Foram testados {len(tamanhos)} tamanhos diferentes: {tamanhos_list}")
            
            # Total de experimentos
            conclusoes.append(f"Total de {len(df)} experimentos executados")
            
        except Exception as e:
            self.logger.warning(f"Erro ao gerar conclusões: {e}")
            conclusoes.append(f"Erro na análise: {e}")
        
        return conclusoes
    
    def gerar_relatorio_markdown(self, analise: Dict[str, Any], resultados):
        """Gerar relatório em formato Markdown"""
        relatorio = []
        
        relatorio.append("# 📊 Relatório de Análise - Algoritmos de Ordenação em Jogos Online\n")
        relatorio.append(f"**Data da Análise:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        relatorio.append(f"**Total de Experimentos:** {analise.get('total_experimentos', 'N/A')}\n")
        
        # Conclusões principais
        if 'resumo_conclusoes' in analise:
            relatorio.append("## 🎯 Principais Conclusões\n")
            for conclusao in analise['resumo_conclusoes']:
                relatorio.append(f"- {conclusao}")
            relatorio.append("")
        
        # Estatísticas descritivas
        if 'estatisticas_descritivas' in analise:
            relatorio.append("## 📈 Estatísticas Descritivas\n")
            
            if 'por_algoritmo' in analise['estatisticas_descritivas']:
                relatorio.append("### Por Algoritmo\n")
                for algo, stats in analise['estatisticas_descritivas']['por_algoritmo'].items():
                    relatorio.append(f"**{algo}:**")
                    relatorio.append(f"- Tempo médio: {stats.get('media', 0):.4f}s")
                    relatorio.append(f"- Desvio padrão: {stats.get('desvio_padrao', 0):.4f}s")
                    relatorio.append(f"- Coeficiente de variação: {stats.get('coef_variacao', 0):.1f}%")
                    relatorio.append("")
        
        # ANOVA
        if 'analise_variancia' in analise:
            relatorio.append("## 🔬 Análise de Variância\n")
            for fator, resultado in analise['analise_variancia'].items():
                if isinstance(resultado, dict) and 'interpretacao' in resultado:
                    relatorio.append(f"**{fator.capitalize()}:**")
                    relatorio.append(f"- F-statistic: {resultado.get('f_statistic', 0):.4f}")
                    relatorio.append(f"- **Conclusão:** {resultado['interpretacao']}")
                    relatorio.append("")
        
        # Salvar relatório
        caminho_relatorio = "relatorio/artigo_cientifico.md"
        os.makedirs(os.path.dirname(caminho_relatorio), exist_ok=True)
        
        try:
            with open(caminho_relatorio, 'w', encoding='utf-8') as f:
                f.write('\n'.join(relatorio))
            
            self.logger.info(f"Relatório salvo em: {caminho_relatorio}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar relatório: {e}")
            # Criar um relatório simples em caso de erro
            with open("relatorio_simples.md", 'w', encoding='utf-8') as f:
                f.write("# Relatório de Análise\n\nRelatório gerado com sucesso!")
