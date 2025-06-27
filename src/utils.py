import os
import time
import functools
import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

def cronometrar(func):
    """Decorator para cronometrar funções"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        tempo = fim - inicio
        print(f"{func.__name__} executou em {tempo:.4f} segundos")
        return resultado
    return wrapper

def log_execucao(func):
    """Decorator para fazer log de execução de funções"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info(f"Iniciando execução de {func.__name__}")
        try:
            resultado = func(*args, **kwargs)
            logger.info(f"Execução de {func.__name__} concluída com sucesso")
            return resultado
        except Exception as e:
            logger.error(f"Erro na execução de {func.__name__}: {e}")
            raise
    return wrapper

def salvar_json(dados, caminho):
    """Salvar dados em formato JSON"""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False, default=str)

def carregar_json(caminho):
    """Carregar dados de arquivo JSON"""
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_csv(dados, caminho):
    """Salvar dados em formato CSV"""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    if isinstance(dados, pd.DataFrame):
        dados.to_csv(caminho, index=False, encoding='utf-8')
    else:
        pd.DataFrame(dados).to_csv(caminho, index=False, encoding='utf-8')

def carregar_csv(caminho):
    """Carregar dados de arquivo CSV"""
    return pd.read_csv(caminho)

def calcular_estatisticas(valores):
    """Calcular estatísticas básicas de uma lista de valores"""
    valores = np.array(valores)
    return {
        'media': float(np.mean(valores)),
        'mediana': float(np.median(valores)),
        'desvio_padrao': float(np.std(valores)),
        'minimo': float(np.min(valores)),
        'maximo': float(np.max(valores)),
        'q25': float(np.percentile(valores, 25)),
        'q75': float(np.percentile(valores, 75)),
        'amplitude': float(np.max(valores) - np.min(valores)),
        'coef_variacao': float(np.std(valores) / np.mean(valores) * 100) if np.mean(valores) != 0 else 0
    }

def calcular_intervalo_confianca(valores, confianca=0.95):
    """Calcular intervalo de confiança para uma lista de valores"""
    from scipy import stats
    valores = np.array(valores)
    n = len(valores)
    media = np.mean(valores)
    erro_padrao = stats.sem(valores)
    intervalo = stats.t.interval(confianca, n-1, loc=media, scale=erro_padrao)
    return {
        'limite_inferior': float(intervalo[0]),
        'limite_superior': float(intervalo[1]),
        'erro_padrao': float(erro_padrao),
        'margem_erro': float(intervalo[1] - media)
    }

def timestamp():
    """Retornar timestamp atual formatado"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def timestamp_arquivo():
    """Retornar timestamp formatado para nomes de arquivos"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def criar_pastas():
    """Criar pastas necessárias do projeto"""
    pastas = ['data', 'plots', 'relatorio', 'logs', 'cache']
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    print(f"✅ Pastas criadas: {', '.join(pastas)}")

def formatar_tempo(segundos):
    """Formatar tempo em segundos para formato legível"""
    if segundos < 1:
        return f"{segundos*1000:.1f}ms"
    elif segundos < 60:
        return f"{segundos:.2f}s"
    elif segundos < 3600:
        minutos = int(segundos // 60)
        segundos_restantes = segundos % 60
        return f"{minutos}m {segundos_restantes:.1f}s"
    else:
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        return f"{horas}h {minutos}m"

def formatar_bytes(bytes_count):
    """Formatar bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"

def verificar_arquivo_existe(caminho):
    """Verificar se arquivo existe"""
    return os.path.exists(caminho)

def obter_tamanho_arquivo(caminho):
    """Obter tamanho de arquivo em bytes"""
    if os.path.exists(caminho):
        return os.path.getsize(caminho)
    return 0

def limpar_cache():
    """Limpar arquivos de cache"""
    cache_dir = 'cache'
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
        print("🧹 Cache limpo")

def gerar_relatorio_sistema():
    """Gerar relatório do sistema atual"""
    import platform
    import psutil   # type: ignore
    
    info = {
        'timestamp': timestamp(),
        'sistema': {
            'os': platform.system(),
            'versao': platform.version(),
            'arquitetura': platform.architecture()[0],
            'processador': platform.processor(),
            'python_version': platform.python_version()
        },
        'hardware': {
            'cpu_cores': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'memoria_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'memoria_disponivel_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            'uso_cpu_percent': psutil.cpu_percent(interval=1)
        },
        'disco': {
            'espaco_total_gb': round(psutil.disk_usage('.').total / (1024**3), 2),
            'espaco_livre_gb': round(psutil.disk_usage('.').free / (1024**3), 2),
            'espaco_usado_gb': round(psutil.disk_usage('.').used / (1024**3), 2)
        }
    }
    
    return info

def validar_resultados(resultados: List[Dict]) -> Dict[str, Any]:
    """Validar resultados dos experimentos"""
    if not resultados:
        return {'valido': False, 'erro': 'Lista de resultados vazia'}
    
    campos_obrigatorios = ['algoritmo', 'tamanho', 'tempo_medio']
    
    for i, resultado in enumerate(resultados):
        for campo in campos_obrigatorios:
            if campo not in resultado:
                return {
                    'valido': False, 
                    'erro': f'Campo "{campo}" ausente no resultado {i}'
                }
        
        # Validar tipos
        if not isinstance(resultado.get('tempo_medio'), (int, float)):
            return {
                'valido': False,
                'erro': f'Campo "tempo_medio" deve ser numérico no resultado {i}'
            }
        
        if resultado.get('tempo_medio', 0) <= 0:
            return {
                'valido': False,
                'erro': f'Campo "tempo_medio" deve ser positivo no resultado {i}'
            }
    
    return {
        'valido': True,
        'total_resultados': len(resultados),
        'algoritmos_unicos': len(set(r.get('algoritmo') for r in resultados)),
        'tamanhos_unicos': len(set(r.get('tamanho') for r in resultados))
    }

def criar_backup(caminho_arquivo: str, sufixo: Optional[str] = None):
    """Criar backup de um arquivo"""
    if not os.path.exists(caminho_arquivo):
        return None
    
    if sufixo is None:
        sufixo = timestamp_arquivo()
    
    nome_base, extensao = os.path.splitext(caminho_arquivo)
    caminho_backup = f"{nome_base}_backup_{sufixo}{extensao}"
    
    import shutil
    shutil.copy2(caminho_arquivo, caminho_backup)
    
    return caminho_backup

def monitorar_memoria():
    """Monitorar uso atual de memória"""
    import psutil # type: ignore
    memoria = psutil.virtual_memory()
    
    return {
        'total_gb': round(memoria.total / (1024**3), 2),
        'disponivel_gb': round(memoria.available / (1024**3), 2),
        'usado_gb': round(memoria.used / (1024**3), 2),
        'percentual_uso': memoria.percent
    }

def verificar_dependencias():
    """Verificar se todas as dependências estão instaladas"""
    dependencias = [
        'numpy', 'pandas', 'matplotlib', 'seaborn', 
        'scipy', 'plotly', 'psutil', 'tqdm'
    ]
    
    instaladas = []
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            instaladas.append(dep)
        except ImportError:
            faltando.append(dep)
    
    return {
        'instaladas': instaladas,
        'faltando': faltando,
        'todas_instaladas': len(faltando) == 0
    }

def imprimir_banner():
    """Imprimir banner do projeto"""
    banner = """
    🎮 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ 🎮
    
         ██████╗ ██████╗ ██████╗ ███████╗███╗   ██╗ █████╗  ██████╗ █████╗  ██████╗        ██╗ ██████╗  ██████╗  ██████╗ ███████╗
        ██╔═══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔═══██╗       ██║██╔═══██╗██╔════╝ ██╔═══██╗██╔════╝
        ██║   ██║██████╔╝██║  ██║█████╗  ██╔██╗ ██║███████║██║     ███████║██║   ██║       ██║██║   ██║██║  ███╗██║   ██║███████╗
        ██║   ██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║██╔══██║██║     ██╔══██║██║   ██║  ██   ██║██║   ██║██║   ██║██║   ██║╚════██║
        ╚██████╔╝██║  ██║██████╔╝███████╗██║ ╚████║██║  ██║╚██████╗██║  ██║╚██████╔╝  ╚█████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████║
         ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝    ╚════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝
                                                                                                                                    
            PROJETO: Avaliação de Algoritmos de Ordenação - Pontuações em Jogos Online 
            Análise de Performance: Merge Sort vs Quick Sort
            Fatores: Tamanho × Distribuição × Algoritmo
              
    🎮 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ 🎮
    """
    print(banner)