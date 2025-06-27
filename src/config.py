"""
Configurações centralizadas para o projeto de avaliação de algoritmos de ordenação.
Contém todos os parâmetros experimentais e configurações do sistema.
"""

import os
from typing import Dict, List

# ========== CONFIGURAÇÕES DO EXPERIMENTO ==========

# Fatores do experimento fatorial 2³
TAMANHOS_VETOR = [10000, 100000]  # Fator A: Tamanho do dataset
TIPOS_DADOS = ['exponencial', 'quase_ordenado']  # Fator B: Tipo de distribuição
ALGORITMOS_NOMES = ['merge_sort', 'quick_sort']  # Fator C: Algoritmo de ordenação

# Configurações de execução
NUM_REPETICOES = 10  # Número de repetições por combinação
TEMPO_MAXIMO_BENCHMARK = 300  # Tempo máximo em segundos para benchmark adaptativo
MIN_REPETICOES_ADAPTATIVO = 3  # Mínimo de repetições no benchmark adaptativo

# ========== PARÂMETROS DOS GERADORES DE DADOS ==========

# Distribuição exponencial (simulação de pontuações de jogos)
LAMBDA_EXPONENCIAL = 0.001  # Taxa da distribuição exponencial
ESCALA_PONTUACAO_MAX = 10000  # Pontuação máxima possível
SEED_ALEATORIO = 42  # Seed para reprodutibilidade

# Dados quase ordenados (simulação de ranking atualizado)
PERCENTUAL_PERTURBACAO = 0.1  # 10% dos dados são perturbados
TIPO_PERTURBACAO = 'swap'  # Tipo: 'swap', 'shuffle', 'reverse'

# ========== CONFIGURAÇÕES DE ARQUIVOS E PASTAS ==========

# Estrutura de diretórios
PASTA_DADOS = 'data'
PASTA_PLOTS = 'plots'
PASTA_RELATORIO = 'relatorio'
PASTA_LOGS = 'logs'
PASTA_CACHE = 'cache'

# Nomes dos arquivos de saída
ARQUIVO_RESULTADOS_JSON = 'resultados_experimento.json'
ARQUIVO_RESULTADOS_CSV = 'resultados_experimento.csv'
ARQUIVO_RESULTADOS_EXCEL = 'resultados_experimento.xlsx'
ARQUIVO_RELATORIO_STATS = 'relatorio_estatistico.json'
ARQUIVO_INFO_SISTEMA = 'info_sistema.json'
ARQUIVO_ARTIGO_MD = 'artigo_cientifico.md'

# ========== CONFIGURAÇÕES DE VISUALIZAÇÃO ==========

# Cores e estilo
CORES_ALGORITMOS = {
    'merge_sort': '#FF6B6B',    # Vermelho coral
    'quick_sort': '#4ECDC4',    # Turquesa
    'heap_sort': '#45B7D1',     # Azul claro
    'bubble_sort': '#96CEB4'    # Verde claro
}

CORES_TIPOS_DADOS = {
    'exponencial': '#FFEAA7',   # Amarelo claro
    'quase_ordenado': '#DDA0DD', # Plum
    'aleatorio': '#87CEEB',     # Sky blue
    'ordenado': '#98FB98'       # Pale green
}

# Configurações de gráficos
TEMA_VISUALIZACAO = 'gaming'  # 'gaming', 'scientific', 'corporate'
ESTILO_MATPLOTLIB = 'default'
FIGSIZE_PADRAO = (12, 8)
FIGSIZE_DASHBOARD = (16, 12)
DPI_GRAFICOS = 300
FORMATO_GRAFICOS = 'png'  # 'png', 'svg', 'pdf'

# ========== CONFIGURAÇÕES ESTATÍSTICAS ==========

# Níveis de significância
ALPHA = 0.05  # Nível de significância para testes estatísticos
CONFIANCA = 0.95  # Nível de confiança para intervalos

# Configurações de testes
TESTE_NORMALIDADE = 'shapiro'  # 'shapiro', 'anderson', 'kstest'
CORRECAO_MULTIPLA = 'bonferroni'  # 'bonferroni', 'holm', 'fdr'

# ========== CONFIGURAÇÕES DE LOGGING ==========

# Configurações de log
NIVEL_LOG = 'INFO'  # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
FORMATO_LOG = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
ARQUIVO_LOG = 'benchmark.log'

# ========== CONFIGURAÇÕES DE PERFORMANCE ==========

# Configurações de memória
LIMITE_MEMORIA_GB = 8  # Limite de memória em GB
FORCAR_COLETA_LIXO = True  # Forçar garbage collection entre testes

# Configurações de CPU
USAR_MULTIPROCESSING = False  # Usar processamento paralelo (experimental)
NUM_PROCESSOS = 4  # Número de processos paralelos

# ========== CONFIGURAÇÕES DE CONTEXTO (JOGOS) ==========

# Contexto do domínio de aplicação
CONTEXTO_APLICACAO = {
    'dominio': 'Jogos Online',
    'cenario': 'Rankings de Jogadores',
    'metricas_relevantes': ['tempo_resposta', 'throughput', 'escalabilidade'],
    'restricoes': {
        'tempo_maximo_atualizacao': 1.0,  # segundos
        'memoria_maxima_mb': 512,  # MB
        'usuarios_simultaneos': 100000
    }
}

# Descrições dos algoritmos no contexto
DESCRICOES_ALGORITMOS = {
    'merge_sort': {
        'nome_completo': 'Merge Sort',
        'complexidade': 'O(n log n)',
        'estabilidade': 'Estável',
        'uso_jogos': 'Rankings oficiais onde consistência é crucial',
        'vantagens': ['Complexidade garantida', 'Estável', 'Previsível'],
        'desvantagens': ['Uso extra de memória', 'Não é in-place']
    },
    'quick_sort': {
        'nome_completo': 'Quick Sort',
        'complexidade': 'O(n log n) médio, O(n²) pior caso',
        'estabilidade': 'Não estável',
        'uso_jogos': 'Ordenações temporárias durante partidas',
        'vantagens': ['Rápido na prática', 'In-place', 'Cache-friendly'],
        'desvantagens': ['Pior caso O(n²)', 'Não estável', 'Recursivo']
    }
}

# ========== FUNÇÕES UTILITÁRIAS ==========

def criar_diretorios():
    """Criar todos os diretórios necessários"""
    diretorios = [PASTA_DADOS, PASTA_PLOTS, PASTA_RELATORIO, PASTA_LOGS, PASTA_CACHE]
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)

def obter_caminho_arquivo(pasta: str, arquivo: str) -> str:
    """Obter caminho completo de um arquivo"""
    return os.path.join(pasta, arquivo)

def validar_configuracoes() -> bool:
    """Validar se todas as configurações estão corretas"""
    try:
        # Validar parâmetros numéricos
        assert all(t > 0 for t in TAMANHOS_VETOR), "Tamanhos devem ser positivos"
        assert NUM_REPETICOES > 0, "Número de repetições deve ser positivo"
        assert 0 < PERCENTUAL_PERTURBACAO < 1, "Percentual de perturbação deve estar entre 0 e 1"
        assert LAMBDA_EXPONENCIAL > 0, "Lambda da exponencial deve ser positivo"
        
        # Validar estrutura
        assert len(TIPOS_DADOS) > 0, "Deve haver pelo menos um tipo de dados"
        assert len(ALGORITMOS_NOMES) > 0, "Deve haver pelo menos um algoritmo"
        
        return True
    except AssertionError as e:
        print(f"Erro na configuração: {e}")
        return False

# Configurações específicas por ambiente
def obter_config_ambiente():
    """Obter configurações específicas do ambiente"""
    import platform
    
    config_env = {
        'sistema': platform.system(),
        'python_version': platform.python_version(),
        'arquitetura': platform.architecture()[0],
        'separador_path': '\\' if platform.system() == 'Windows' else '/',
        'cores_suportadas': 'sim'
    }
    
    return config_env

# Inicialização automática
if __name__ == "__main__":
    print("🔧 Validando configurações...")
    if validar_configuracoes():
        print("✅ Configurações válidas!")
        criar_diretorios()
        print("📁 Diretórios criados!")
    else:
        print("❌ Erro nas configurações!")