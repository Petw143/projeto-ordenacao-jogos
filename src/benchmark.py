import time
import json
import gc
import psutil  # type: ignore
import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from algoritmos import AlgoritmoOrdenacao
from scipy import stats  # type: ignore
import logging
from datetime import datetime

class Benchmark:
    """Classe para medição precisa de performance dos algoritmos"""
    
    def __init__(self):
        self.resultados = []
        self.historico_memoria = []
        self.metricas_detalhadas = []
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def medir_tempo_e_memoria(self, algoritmo: AlgoritmoOrdenacao, dados: List[int]) -> Dict[str, Any]:
        """
        Medir tempo de execução e uso de memória de um algoritmo
        
        Args:
            algoritmo: Instância do algoritmo a ser testado
            dados: Dados para ordenar
            
        Returns:
            Dicionário com métricas detalhadas
        """
        # Forçar coleta de lixo antes do teste
        gc.collect()
        
        # Registrar uso de memória antes
        processo = psutil.Process(os.getpid())
        memoria_antes = processo.memory_info().rss / 1024 / 1024  # MB
        
        # Medir tempo com alta precisão
        inicio = time.perf_counter()
        
        # Executar algoritmo
        resultado = algoritmo.ordenar(dados.copy())
        
        # Finalizar medição
        fim = time.perf_counter()
        tempo_execucao = fim - inicio
        
        # Registrar uso final de memória
        memoria_depois = processo.memory_info().rss / 1024 / 1024  # MB
        uso_memoria = memoria_depois - memoria_antes
        
        # Verificar se resultado está correto
        if not self._verificar_ordenacao(resultado):
            raise ValueError(f"Algoritmo {algoritmo.nome} não ordenou corretamente!")
        
        # Calcular métricas adicionais
        tamanho_dados = len(dados)
        throughput = tamanho_dados / tempo_execucao if tempo_execucao > 0 else 0
        
        return {
            'nome_algoritmo': algoritmo.nome,
            'tamanho_dados': tamanho_dados,
            'tempo_execucao': tempo_execucao,
            'memoria_usada': uso_memoria,
            'throughput': throughput,
            'timestamp': datetime.now().isoformat()
        }
    
    def _verificar_ordenacao(self, dados: List[int]) -> bool:
        """Verificar se os dados estão ordenados corretamente"""
        return all(dados[i] <= dados[i + 1] for i in range(len(dados) - 1))
    
    def medir_tempo(self, algoritmo: AlgoritmoOrdenacao, dados: List[int]) -> float:
        """
        Medir apenas o tempo de execução (para compatibilidade)
        """
        metricas = self.medir_tempo_e_memoria(algoritmo, dados)
        return metricas['tempo_execucao']
    
    def executar_experimento_completo(self, algoritmos: Dict[str, AlgoritmoOrdenacao], 
                                    dados_teste: Dict[str, List[int]], 
                                    repeticoes: int = 10) -> List[Dict]:
        """
        Executar experimento completo com todos os algoritmos e dados
        
        Args:
            algoritmos: Dicionário com algoritmos a testar
            dados_teste: Dicionário com diferentes conjuntos de dados
            repeticoes: Número de repetições por teste
            
        Returns:
            Lista com todos os resultados
        """
        resultados = []
        
        for nome_dados, dados in dados_teste.items():
            for nome_algo, algoritmo in algoritmos.items():
                print(f"Testando {algoritmo.nome} com {nome_dados} ({len(dados)} elementos)")
                
                tempos = []
                for i in range(repeticoes):
                    # Criar cópia dos dados para cada execução
                    dados_copia = dados.copy()
                    
                    # Medir tempo
                    tempo = self.medir_tempo(algoritmo, dados_copia)
                    tempos.append(tempo)
                    
                    print(f"  Execução {i+1}: {tempo:.4f}s")
                
                # Calcular estatísticas
                resultado = {
                    'algoritmo': algoritmo.nome,
                    'tipo_dados': nome_dados,
                    'tamanho': len(dados),
                    'repeticoes': repeticoes,
                    'tempos': tempos,
                    'tempo_medio': sum(tempos) / len(tempos),
                    'tempo_min': min(tempos),
                    'tempo_max': max(tempos),
                    'desvio_padrao': (sum((t - sum(tempos)/len(tempos))**2 for t in tempos) / len(tempos))**0.5
                }
                
                resultados.append(resultado)
                print(f"  Resultado: {resultado['tempo_medio']:.4f}s ± {resultado['desvio_padrao']:.4f}s\n")
        
        return resultados
    
    def executar_benchmark_completo(self, algoritmo: AlgoritmoOrdenacao, dados: List[int], 
                                   repeticoes: int = 10) -> Dict[str, Any]:
        """
        Executar benchmark completo com múltiplas execuções e análise estatística
        
        Args:
            algoritmo: Algoritmo a ser testado
            dados: Dados para ordenar
            repeticoes: Número de execuções
            
        Returns:
            Dicionário com estatísticas completas
        """
        self.logger.info(f"Iniciando benchmark: {algoritmo.nome} com {len(dados)} elementos")
        
        tempos = []
        memorias = []
        throughputs = []
        
        for i in range(repeticoes):
            self.logger.debug(f"Execução {i+1}/{repeticoes}")
            
            # Executar medição
            metricas = self.medir_tempo_e_memoria(algoritmo, dados)
            
            tempos.append(metricas['tempo_execucao'])
            memorias.append(metricas['memoria_usada'])
            throughputs.append(metricas['throughput'])
            
            # Armazenar métricas detalhadas
            self.metricas_detalhadas.append(metricas)
            
            # Pequena pausa para estabilidade
            time.sleep(0.01)
        
        # Calcular estatísticas
        estatisticas = self._calcular_estatisticas(tempos, memorias, throughputs)
        
        resultado = {
            'algoritmo': algoritmo.nome,
            'tamanho_dados': len(dados),
            'repeticoes': repeticoes,
            'timestamp': datetime.now().isoformat(),
            **estatisticas
        }
        
        self.logger.info(f"Benchmark concluído: {resultado['tempo_medio']:.4f}s ± {resultado['tempo_desvio']:.4f}s")
        
        return resultado
    
    def _calcular_estatisticas(self, tempos: List[float], memorias: List[float], 
                              throughputs: List[float]) -> Dict[str, Any]:
        """Calcular estatísticas detalhadas das métricas"""
        tempos_np = np.array(tempos)
        memorias_np = np.array(memorias)
        throughputs_np = np.array(throughputs)
        
        # Calcular intervalos de confiança (95%)
        alpha = 0.05
        n = len(tempos)
        
        # Tempo
        tempo_media = np.mean(tempos_np)
        tempo_desvio = np.std(tempos_np, ddof=1)
        tempo_erro_padrao = tempo_desvio / np.sqrt(n)
        tempo_ic = stats.t.interval(1-alpha, n-1, loc=tempo_media, scale=tempo_erro_padrao)
        
        # Memória
        memoria_media = np.mean(memorias_np)
        memoria_desvio = np.std(memorias_np, ddof=1)
        
        # Throughput
        throughput_medio = np.mean(throughputs_np)
        throughput_desvio = np.std(throughputs_np, ddof=1)
        
        return {
            # Estatísticas de tempo
            'tempo_medio': tempo_media,
            'tempo_desvio': tempo_desvio,
            'tempo_min': np.min(tempos_np),
            'tempo_max': np.max(tempos_np),
            'tempo_mediana': np.median(tempos_np),
            'tempo_q1': np.percentile(tempos_np, 25),
            'tempo_q3': np.percentile(tempos_np, 75),
            'tempo_ic_inferior': tempo_ic[0],
            'tempo_ic_superior': tempo_ic[1],
            
            # Estatísticas de memória
            'memoria_media': memoria_media,
            'memoria_desvio': memoria_desvio,
            'memoria_min': np.min(memorias_np),
            'memoria_max': np.max(memorias_np),
            
            # Estatísticas de throughput
            'throughput_medio': throughput_medio,
            'throughput_desvio': throughput_desvio,
            'throughput_min': np.min(throughputs_np),
            'throughput_max': np.max(throughputs_np),
            
            # Dados brutos
            'tempos_brutos': tempos,
            'memorias_brutas': memorias,
            'throughputs_brutos': throughputs
        }
    
    def executar_experimento_factorial(self, algoritmos: Dict[str, AlgoritmoOrdenacao], 
                                     dados_teste: Dict[str, List[int]], 
                                     repeticoes: int = 10) -> pd.DataFrame:
        """
        Executar experimento fatorial completo (2³ design)
        
        Args:
            algoritmos: Dicionário com algoritmos
            dados_teste: Dicionário com conjuntos de dados
            repeticoes: Número de repetições
            
        Returns:
            DataFrame com todos os resultados
        """
        self.logger.info("Iniciando experimento fatorial completo")
        
        resultados = []
        total_experimentos = len(algoritmos) * len(dados_teste)
        experimento_atual = 0
        
        for nome_dados, dados in dados_teste.items():
            # Extrair informações do nome dos dados
            partes = nome_dados.split('_')
            tamanho = int(partes[0])
            tipo_distribuicao = partes[1]
            
            for nome_algo, algoritmo in algoritmos.items():
                experimento_atual += 1
                progresso = (experimento_atual / total_experimentos) * 100
                
                self.logger.info(f"Experimento {experimento_atual}/{total_experimentos} ({progresso:.1f}%)")
                self.logger.info(f"Testando {algoritmo.nome} com {nome_dados}")
                
                # Executar benchmark
                resultado = self.executar_benchmark_completo(algoritmo, dados, repeticoes)
                
                # Adicionar fatores experimentais
                resultado.update({
                    'fator_a_tamanho': tamanho,
                    'fator_b_distribuicao': tipo_distribuicao,
                    'fator_c_algoritmo': nome_algo,
                    'nome_dados': nome_dados
                })
                
                resultados.append(resultado)
        
        # Converter para DataFrame
        df_resultados = pd.DataFrame(resultados)
        
        self.logger.info("Experimento fatorial concluído")
        
        return df_resultados
    
    def calcular_speedup(self, df_resultados: pd.DataFrame, algoritmo_referencia: str = 'merge_sort_implementacao_classica') -> pd.DataFrame:
        """
        Calcular speedup relativo entre algoritmos
        
        Args:
            df_resultados: DataFrame com resultados
            algoritmo_referencia: Algoritmo usado como referência
            
        Returns:
            DataFrame com speedups calculados
        """
        df_speedup = df_resultados.copy()
        
        # Agrupar por tamanho e distribuição
        grupos = df_resultados.groupby(['fator_a_tamanho', 'fator_b_distribuicao'])
        
        speedups = []
        
        for (tamanho, distribuicao), grupo in grupos:
            # Verificar se o algoritmo de referência existe no grupo
            ref_rows = grupo[grupo['fator_c_algoritmo'] == algoritmo_referencia]
            if ref_rows.empty:
                # Se não encontrar o algoritmo de referência, usar o primeiro algoritmo do grupo
                ref_tempo = grupo['tempo_medio'].iloc[0]
            else:
                ref_tempo = ref_rows['tempo_medio'].iloc[0]
            
            for _, row in grupo.iterrows():
                speedup = ref_tempo / row['tempo_medio']
                speedups.append(speedup)
        
        df_speedup['speedup'] = speedups
        
        return df_speedup
    
    def gerar_relatorio_estatistico(self, df_resultados: pd.DataFrame) -> Dict[str, Any]:
        """
        Gerar relatório estatístico completo
        
        Args:
            df_resultados: DataFrame com resultados
            
        Returns:
            Dicionário com análises estatísticas
        """
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'total_experimentos': len(df_resultados),
            'algoritmos_testados': df_resultados['fator_c_algoritmo'].unique().tolist(),
            'tamanhos_testados': df_resultados['fator_a_tamanho'].unique().tolist(),
            'distribuicoes_testadas': df_resultados['fator_b_distribuicao'].unique().tolist()
        }
        
        # Estatísticas descritivas por algoritmo
        relatorio['estatisticas_por_algoritmo'] = {}
        for algoritmo in df_resultados['fator_c_algoritmo'].unique():
            dados_algo = df_resultados[df_resultados['fator_c_algoritmo'] == algoritmo]
            
            relatorio['estatisticas_por_algoritmo'][algoritmo] = {
                'tempo_medio_geral': dados_algo['tempo_medio'].mean(),
                'tempo_desvio_geral': dados_algo['tempo_medio'].std(),
                'memoria_media_geral': dados_algo['memoria_media'].mean(),
                'throughput_medio_geral': dados_algo['throughput_medio'].mean()
            }
        
        # Análise de variância (ANOVA)
        try:
            from scipy.stats import f_oneway
            
            grupos_tempo = [
                df_resultados[df_resultados['fator_c_algoritmo'] == algo]['tempo_medio'].values
                for algo in df_resultados['fator_c_algoritmo'].unique()
            ]
            
            f_stat, p_value = f_oneway(*grupos_tempo)
            
            relatorio['anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significativo': p_value < 0.05
            }
            
        except Exception as e:
            self.logger.warning(f"Erro ao calcular ANOVA: {e}")
            relatorio['anova'] = None
        
        # Matriz de correlação
        colunas_numericas = ['fator_a_tamanho', 'tempo_medio', 'memoria_media', 'throughput_medio']
        matriz_corr = df_resultados[colunas_numericas].corr()
        relatorio['matriz_correlacao'] = matriz_corr.to_dict()
        
        return relatorio
    
    def salvar_resultados(self, resultados: Any, caminho: str, formato: str = 'json'):
        """
        Salvar resultados em diferentes formatos
        
        Args:
            resultados: Dados para salvar (Dict, DataFrame, etc.)
            caminho: Caminho do arquivo
            formato: Formato do arquivo ('json', 'csv', 'excel')
        """
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        try:
            if formato == 'json':
                if isinstance(resultados, pd.DataFrame):
                    resultados.to_json(caminho, orient='records', indent=2)
                else:
                    with open(caminho, 'w', encoding='utf-8') as f:
                        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
                        
            elif formato == 'csv':
                if isinstance(resultados, pd.DataFrame):
                    resultados.to_csv(caminho, index=False, encoding='utf-8')
                else:
                    pd.DataFrame(resultados).to_csv(caminho, index=False, encoding='utf-8')
                    
            elif formato == 'excel':
                if isinstance(resultados, pd.DataFrame):
                    resultados.to_excel(caminho, index=False)
                else:
                    pd.DataFrame(resultados).to_excel(caminho, index=False)
            
            self.logger.info(f"Resultados salvos em: {caminho}")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar resultados: {e}")
            raise
    
    def carregar_resultados(self, caminho: str) -> pd.DataFrame:
        """
        Carregar resultados salvos anteriormente
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            DataFrame com os resultados
        """
        try:
            if caminho.endswith('.json'):
                return pd.read_json(caminho)
            elif caminho.endswith('.csv'):
                return pd.read_csv(caminho)
            elif caminho.endswith('.xlsx') or caminho.endswith('.xls'):
                return pd.read_excel(caminho)
            else:
                raise ValueError(f"Formato de arquivo não suportado: {caminho}")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar resultados: {e}")
            raise
    
    def limpar_cache(self):
        """Limpar cache e histórico de resultados"""
        self.resultados.clear()
        self.historico_memoria.clear()
        self.metricas_detalhadas.clear()
        gc.collect()
        self.logger.info("Cache limpo com sucesso")
    
    def obter_info_sistema(self) -> Dict[str, Any]:
        """
        Obter informações do sistema para contexto dos benchmarks
        
        Returns:
            Dicionário com informações do sistema
        """
        import platform
        
        return {
            'sistema_operacional': platform.system(),
            'versao_so': platform.version(),
            'arquitetura': platform.architecture()[0],
            'processador': platform.processor(),
            'python_versao': platform.python_version(),
            'nucleos_cpu': psutil.cpu_count(logical=False),
            'nucleos_logicos': psutil.cpu_count(logical=True),
            'memoria_total_gb': psutil.virtual_memory().total / (1024**3),
            'memoria_disponivel_gb': psutil.virtual_memory().available / (1024**3),
            'timestamp': datetime.now().isoformat()
        }
    
    def benchmark_adaptativo(self, algoritmo: AlgoritmoOrdenacao, dados: List[int], 
                           tempo_maximo: float = 60.0, min_repeticoes: int = 3) -> Dict[str, Any]:
        """
        Benchmark adaptativo que ajusta o número de repetições baseado no tempo disponível
        
        Args:
            algoritmo: Algoritmo para testar
            dados: Dados para ordenar
            tempo_maximo: Tempo máximo em segundos
            min_repeticoes: Mínimo de repetições
            
        Returns:
            Resultado do benchmark
        """
        self.logger.info(f"Iniciando benchmark adaptativo: {algoritmo.nome} (max {tempo_maximo}s)")
        
        tempo_inicio = time.time()
        tempos = []
        memorias = []
        throughputs = []
        
        repeticao = 0
        
        while True:
            # Verificar se ainda temos tempo
            tempo_decorrido = time.time() - tempo_inicio
            if tempo_decorrido >= tempo_maximo and repeticao >= min_repeticoes:
                break
                
            # Estimar tempo restante baseado na média atual
            if repeticao > 0:
                tempo_medio_execucao = np.mean(tempos)
                tempo_estimado_proxima = tempo_medio_execucao * 2  # Buffer de segurança
                
                if tempo_decorrido + tempo_estimado_proxima > tempo_maximo and repeticao >= min_repeticoes:
                    break
            
            # Executar medição
            metricas = self.medir_tempo_e_memoria(algoritmo, dados)
            
            tempos.append(metricas['tempo_execucao'])
            memorias.append(metricas['memoria_usada'])
            throughputs.append(metricas['throughput'])
            
            repeticao += 1
            
            # Log de progresso
            if repeticao % 5 == 0:
                self.logger.debug(f"Repetição {repeticao}, tempo decorrido: {tempo_decorrido:.1f}s")
        
        # Calcular estatísticas
        estatisticas = self._calcular_estatisticas(tempos, memorias, throughputs)
        
        resultado = {
            'algoritmo': algoritmo.nome,
            'tamanho_dados': len(dados),
            'repeticoes_executadas': repeticao,
            'tempo_total_benchmark': time.time() - tempo_inicio,
            'timestamp': datetime.now().isoformat(),
            **estatisticas
        }
        
        self.logger.info(f"Benchmark adaptativo concluído: {repeticao} repetições em {resultado['tempo_total_benchmark']:.1f}s")
        
        return resultado
