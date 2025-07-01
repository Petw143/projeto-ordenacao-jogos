import os
import sys
import time
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/benchmark.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    print("🎮 PROJETO: Avaliação de Algoritmos de Ordenação - Pontuações de Jogo Online")
    print("=" * 70)
    
    # Importar módulos
    from geradores import GeradorDados
    from algoritmos import obter_todos_algoritmos
    from benchmark import Benchmark
    from analise import AnalisadorResultados
    from visualizacao import GeradorGraficos
    
    # Configurações do experimento
    TAMANHOS = [10000, 100000]
    TIPOS_DADOS = ['exponencial', 'quase_ordenado']
    
    # Obter TODOS os algoritmos variantes
    todos_algoritmos = obter_todos_algoritmos(cutoff=10)
    
    # Criar dicionário com chaves simplificadas para compatibilidade
    ALGORITMOS = {}
    for algo in todos_algoritmos:
        # Criar chave única baseada no nome do algoritmo
        chave = algo.nome.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('=', '_').replace('-', '_')
        ALGORITMOS[chave] = algo
    
    # Log dos algoritmos que serão testados
    logging.info(f"Algoritmos a serem testados: {list(ALGORITMOS.keys())}")
    for chave, algo in ALGORITMOS.items():
        logging.info(f"  {chave}: {algo.nome}")
    
    REPETICOES = 5  # Reduzido para 5 devido à análise completa de 6 algoritmos distintos
    
    logging.info("Iniciando experimentos...")
    
    # Inicializar componentes
    gerador = GeradorDados()
    benchmark = Benchmark()
    
    # Executar todos os experimentos
    resultados = []
    
    # Preparar dados de teste no formato correto
    dados_teste = {}
    
    for tamanho in TAMANHOS:
        for tipo_dado in TIPOS_DADOS:
            # Gerar dados
            logging.info(f"Gerando dados: tamanho={tamanho}, tipo={tipo_dado}")
            dados = gerador.gerar(tamanho, tipo_dado)
            
            # Chave no formato esperado pelo benchmark
            chave = f"{tamanho}_{tipo_dado}"
            dados_teste[chave] = dados
    
    # Executar experimento fatorial completo
    logging.info("Executando experimento fatorial...")
    df_resultados = benchmark.executar_experimento_factorial(ALGORITMOS, dados_teste, REPETICOES)
    
    # Calcular speedup
    df_resultados = benchmark.calcular_speedup(df_resultados)
    
    # Gerar relatório estatístico
    relatorio_stats = benchmark.gerar_relatorio_estatistico(df_resultados)
    
    # Salvar resultados
    logging.info("Salvando resultados...")
    benchmark.salvar_resultados(df_resultados, 'data/resultados_experimento.json', 'json')
    benchmark.salvar_resultados(df_resultados, 'data/resultados_experimento.csv', 'csv')
    benchmark.salvar_resultados(df_resultados, 'data/resultados_experimento.xlsx', 'excel')
    
    # Salvar relatório estatístico
    benchmark.salvar_resultados(relatorio_stats, 'data/relatorio_estatistico.json', 'json')
    
    # Executar análise
    logging.info("Executando análise estatística...")
    analisador = AnalisadorResultados()
    relatorio = analisador.analisar(df_resultados)  # AnalisadorResultados já aceita DataFrame
    
    # Executar análise específica das variantes de algoritmos
    logging.info("Executando análise das variantes de algoritmos...")
    relatorio_variantes = analisador.analisar_variantes_algoritmos(df_resultados)
    
    # Salvar análise das variantes
    benchmark.salvar_resultados(relatorio_variantes, 'data/analise_variantes.json', 'json')
    
    # Gerar gráficos
    logging.info("Gerando visualizações...")
    gerador_graficos = GeradorGraficos(tema='gaming')
    gerador_graficos.gerar_todos(df_resultados)  # GeradorGraficos já aceita DataFrame
    
    # Gerar relatório final
    logging.info("Gerando relatório final...")
    analisador.gerar_relatorio_markdown(relatorio, df_resultados.to_dict('records'))
    
    # Salvar informações do sistema
    info_sistema = benchmark.obter_info_sistema()
    benchmark.salvar_resultados(info_sistema, 'data/info_sistema.json', 'json')
    
    print("\nExperimento concluído com sucesso!")
    print("Verifique os arquivos em:")
    print("   - data/resultados_experimento.* (JSON, CSV, Excel)")
    print("   - data/relatorio_estatistico.json")
    print("   - data/info_sistema.json")
    print("   - plots/ (gráficos)")
    print("   - relatorio/artigo_cientifico.md")
    
    # Mostrar informações finais
    print(f"\nResumo dos Resultados:")
    print(f"   • Total de experimentos: {len(df_resultados)}")
    print(f"   • Algoritmos testados: {', '.join(df_resultados['fator_c_algoritmo'].unique())}")
    print(f"   • Tamanhos testados: {', '.join(map(str, df_resultados['fator_a_tamanho'].unique()))}")
    print(f"   • Distribuições testadas: {', '.join(df_resultados['fator_b_distribuicao'].unique())}")
    
    # Mostrar algoritmo mais rápido
    melhor_algo = df_resultados.loc[df_resultados['tempo_medio'].idxmin()]
    print(f"   • Melhor performance: {melhor_algo['fator_c_algoritmo']} com {melhor_algo['tempo_medio']:.4f}s")
    
if __name__ == "__main__":
    main()
