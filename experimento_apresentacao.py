"""
Experimento Comparativo das Variantes - Resultados para Apresentação
"""

import sys
import os
import time
import json
import random
import statistics
from pathlib import Path

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.algoritmos_variantes import criar_todos_algoritmos
    from src.geradores import GeradorDados
    print("✅ Módulos importados com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

def executar_experimento_apresentacao():
    """Experimento focado para dados da apresentação"""
    print("\n=== EXPERIMENTO PARA APRESENTAÇÃO ===")
    
    # Configuração
    tamanhos = [1000, 5000, 10000]
    tipos_dados = ['aleatorio', 'quase_ordenado']
    num_execucoes = 15
    
    gerador = GeradorDados()
    algoritmos = criar_todos_algoritmos(10)
    
    print(f"Algoritmos: {len(algoritmos)}")
    print(f"Tamanhos: {tamanhos}")
    print(f"Tipos: {tipos_dados}")
    print(f"Execuções por teste: {num_execucoes}")
    
    resultados = []
    total_testes = len(algoritmos) * len(tamanhos) * len(tipos_dados)
    teste_atual = 0
    
    for algoritmo in algoritmos:
        print(f"\n🔄 Testando: {algoritmo.nome}")
        
        for tamanho in tamanhos:
            for tipo_dados in tipos_dados:
                teste_atual += 1
                progresso = (teste_atual / total_testes) * 100
                
                print(f"  [{progresso:5.1f}%] {tamanho:5d} elementos - {tipo_dados}")
                
                # Gerar dados
                if tipo_dados == 'aleatorio':
                    dados_base = list(random.sample(range(1, tamanho*10), tamanho))
                else:  # quase_ordenado
                    dados_base = gerador.gerar(tamanho, 'quase_ordenado')
                
                # Múltiplas execuções
                tempos = []
                for _ in range(num_execucoes):
                    dados = dados_base.copy()
                    random.shuffle(dados)  # Garantir aleatoriedade
                    
                    inicio = time.perf_counter()
                    resultado = algoritmo.ordenar(dados)
                    fim = time.perf_counter()
                    
                    tempo_ms = (fim - inicio) * 1000
                    tempos.append(tempo_ms)
                    
                    # Verificar ordenação
                    if resultado != sorted(dados_base):
                        print(f"    ❌ ERRO: Ordenação incorreta!")
                
                # Calcular estatísticas
                resultado_teste = {
                    'algoritmo': algoritmo.nome,
                    'tamanho': tamanho,
                    'tipo_dados': tipo_dados,
                    'tempo_medio': statistics.mean(tempos),
                    'tempo_mediano': statistics.median(tempos),
                    'desvio_padrao': statistics.stdev(tempos),
                    'tempo_min': min(tempos),
                    'tempo_max': max(tempos),
                    'cv_percent': (statistics.stdev(tempos) / statistics.mean(tempos)) * 100,
                    'num_execucoes': num_execucoes
                }
                
                resultados.append(resultado_teste)
                
                print(f"    ⏱️  {resultado_teste['tempo_medio']:.2f}ms (±{resultado_teste['desvio_padrao']:.2f})")
    
    # Salvar resultados
    Path("resultados_apresentacao").mkdir(exist_ok=True)
    
    with open("resultados_apresentacao/dados_variantes.json", 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    # Análise de melhorias
    analisar_melhorias(resultados)
    
    print(f"\n✅ Experimento concluído! {len(resultados)} resultados salvos.")
    print("📁 Dados salvos em: resultados_apresentacao/")

def analisar_melhorias(resultados):
    """Analisar melhorias percentuais das otimizações"""
    print("\n=== ANÁLISE DE MELHORIAS ===")
    
    melhorias = {}
    
    for resultado in resultados:
        tamanho = resultado['tamanho']
        tipo_dados = resultado['tipo_dados']
        algoritmo = resultado['algoritmo']
        tempo = resultado['tempo_medio']
        
        chave = f"{tamanho}_{tipo_dados}"
        if chave not in melhorias:
            melhorias[chave] = {}
        
        melhorias[chave][algoritmo] = tempo
    
    # Calcular melhorias
    relatorio = []
    
    for chave, tempos in melhorias.items():
        tamanho, tipo_dados = chave.split('_')
        
        # Baselines
        merge_puro = tempos.get('Merge Sort (Puro)')
        quick_puro = tempos.get('Quick Sort (Puro)')
        
        linha = {
            'tamanho': int(tamanho),
            'tipo_dados': tipo_dados,
            'merge_puro': merge_puro,
            'quick_puro': quick_puro
        }
        
        if merge_puro:
            merge_opt = tempos.get('Merge Sort + Insertion Sort (cutoff=10)')
            if merge_opt:
                melhoria = ((merge_puro - merge_opt) / merge_puro) * 100
                linha['merge_melhoria'] = melhoria
        
        if quick_puro:
            quick_completo = tempos.get('Quick Sort Completo (cutoff=10)')
            if quick_completo:
                melhoria = ((quick_puro - quick_completo) / quick_puro) * 100
                linha['quick_melhoria'] = melhoria
        
        relatorio.append(linha)
    
    # Mostrar relatório
    print("\n📊 MELHORIAS PERCENTUAIS:")
    print("Tamanho | Tipo | Merge+Insertion | Quick Completo")
    print("-" * 55)
    
    for linha in relatorio:
        merge_str = f"{linha.get('merge_melhoria', 0):+5.1f}%" if 'merge_melhoria' in linha else "  N/A"
        quick_str = f"{linha.get('quick_melhoria', 0):+5.1f}%" if 'quick_melhoria' in linha else "  N/A"
        
        print(f"{linha['tamanho']:6d} | {linha['tipo_dados']:12s} | {merge_str:>13s} | {quick_str:>12s}")
    
    # Salvar relatório
    with open("resultados_apresentacao/melhorias.json", 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    executar_experimento_apresentacao()
