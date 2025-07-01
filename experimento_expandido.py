"""
Experimento Expandido: Análise do Impacto Individual das Otimizações

Este script implementa um experimento rigoroso para avaliar separadamente
o impacto de cada otimização nos algoritmos de ordenação, eliminando viés
experimental e fornecendo análise estatística robusta.
"""

import time
import json
import numpy as np
import pandas as pd
from typing import List, Dict
import statistics
from pathlib import Path
import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.algoritmos_variantes import criar_todos_algoritmos
    from src.geradores import GeradorDados
except ImportError:
    print("Erro: Não foi possível importar os módulos necessários.")
    print("Verifique se os arquivos src/algoritmos_variantes.py e src/geradores.py existem.")
    sys.exit(1)

class ExperimentoExpandido:
    """Experimento para análise detalhada de otimizações"""
    
    def __init__(self, cutoff: int = 10, num_execucoes: int = 20):
        self.cutoff = cutoff
        self.num_execucoes = num_execucoes
        self.gerador = GeradorDados()
        self.resultados = []
        
        # Configuração dos tamanhos para teste (menor para execução mais rápida)
        self.tamanhos = [1000, 5000, 10000, 20000]
        
        # Tipos de dados para teste
        self.tipos_dados = ['aleatorio', 'quase_ordenado']
    
    def gerar_dados(self, tamanho: int, tipo: str) -> List[int]:
        """Gerar dados conforme o tipo especificado"""
        if tipo == 'aleatorio':
            return list(np.random.randint(1, 10000, tamanho))
        elif tipo == 'quase_ordenado':
            return self.gerador.gerar(tamanho, 'quase_ordenado')
        else:
            raise ValueError(f"Tipo de dados desconhecido: {tipo}")
    
    def medir_tempo_execucao(self, algoritmo, dados: List[int]) -> float:
        """Medir tempo de execução de um algoritmo"""
        inicio = time.perf_counter()
        _ = algoritmo.ordenar(dados.copy())
        fim = time.perf_counter()
        return (fim - inicio) * 1000  # Converter para milissegundos
    
    def executar_teste_algoritmo(self, algoritmo, tamanho: int, tipo_dados: str) -> Dict:
        """Executar múltiplas medições para um algoritmo específico"""
        tempos = []
        
        for _ in range(self.num_execucoes):
            dados = self.gerar_dados(tamanho, tipo_dados)
            tempo = self.medir_tempo_execucao(algoritmo, dados)
            tempos.append(tempo)
        
        # Calcular estatísticas
        return {
            'algoritmo': algoritmo.nome,
            'tamanho': tamanho,
            'tipo_dados': tipo_dados,
            'num_execucoes': len(tempos),
            'tempo_medio': statistics.mean(tempos),
            'tempo_mediano': statistics.median(tempos),
            'desvio_padrao': statistics.stdev(tempos) if len(tempos) > 1 else 0,
            'tempo_min': min(tempos),
            'tempo_max': max(tempos),
            'cv': (statistics.stdev(tempos) / statistics.mean(tempos)) * 100 if len(tempos) > 1 and statistics.mean(tempos) > 0 else 0
        }
    
    def executar_experimento_completo(self) -> List[Dict]:
        """Executar experimento completo com todas as variantes"""
        print("=== EXPERIMENTO EXPANDIDO: ANÁLISE DE OTIMIZAÇÕES ===")
        print(f"Cutoff para Insertion Sort: {self.cutoff}")
        print(f"Número de execuções por teste: {self.num_execucoes}")
        print(f"Tamanhos testados: {self.tamanhos}")
        print(f"Tipos de dados: {self.tipos_dados}")
        print()
        
        # Criar todas as variantes dos algoritmos
        try:
            algoritmos = criar_todos_algoritmos(self.cutoff)
        except Exception as e:
            print(f"Erro ao criar algoritmos: {e}")
            return []
        
        total_testes = len(algoritmos) * len(self.tamanhos) * len(self.tipos_dados)
        teste_atual = 0
        
        resultados = []
        
        for algoritmo in algoritmos:
            print(f"Testando: {algoritmo.nome}")
            
            for tamanho in self.tamanhos:
                for tipo_dados in self.tipos_dados:
                    teste_atual += 1
                    progresso = (teste_atual / total_testes) * 100
                    print(f"  Progresso: {teste_atual}/{total_testes} ({progresso:.1f}%) - "
                          f"Tamanho: {tamanho}, Tipo: {tipo_dados}")
                    
                    try:
                        resultado = self.executar_teste_algoritmo(algoritmo, tamanho, tipo_dados)
                        resultados.append(resultado)
                    except Exception as e:
                        print(f"    Erro no teste: {e}")
                        continue
        
        self.resultados = resultados
        return resultados
    
    def calcular_melhorias(self) -> Dict:
        """Calcular percentual de melhoria das otimizações"""
        if not self.resultados:
            return {}
        
        melhorias = {}
        
        # Converter resultados para DataFrame para facilitar análise
        df = pd.DataFrame(self.resultados)
        
        for tamanho in self.tamanhos:
            melhorias[tamanho] = {}
            
            for tipo_dados in self.tipos_dados:
                df_filtrado = df[(df['tamanho'] == tamanho) & (df['tipo_dados'] == tipo_dados)]
                
                if df_filtrado.empty:
                    continue
                
                melhorias_tipo = {}
                
                # Buscar tempos dos algoritmos base
                merge_puro = df_filtrado[df_filtrado['algoritmo'] == 'Merge Sort (Puro)']
                quick_puro = df_filtrado[df_filtrado['algoritmo'] == 'Quick Sort (Puro)']
                
                if not merge_puro.empty:
                    tempo_merge_puro = merge_puro['tempo_medio'].iloc[0]
                    
                    # Merge Sort com Insertion Sort
                    merge_insertion = df_filtrado[df_filtrado['algoritmo'].str.contains('Merge Sort \\+ Insertion Sort', na=False)]
                    if not merge_insertion.empty:
                        tempo_merge_insertion = merge_insertion['tempo_medio'].iloc[0]
                        melhoria = ((tempo_merge_puro - tempo_merge_insertion) / tempo_merge_puro) * 100
                        melhorias_tipo['merge_insertion_sort'] = melhoria
                
                if not quick_puro.empty:
                    tempo_quick_puro = quick_puro['tempo_medio'].iloc[0]
                    
                    # Quick Sort com Median-of-Three
                    quick_median = df_filtrado[df_filtrado['algoritmo'] == 'Quick Sort + Median-of-Three']
                    if not quick_median.empty:
                        tempo_quick_median = quick_median['tempo_medio'].iloc[0]
                        melhoria = ((tempo_quick_puro - tempo_quick_median) / tempo_quick_puro) * 100
                        melhorias_tipo['quick_median_of_three'] = melhoria
                    
                    # Quick Sort com Insertion Sort
                    quick_insertion = df_filtrado[df_filtrado['algoritmo'].str.contains('Quick Sort \\+ Insertion Sort', na=False)]
                    if not quick_insertion.empty:
                        tempo_quick_insertion = quick_insertion['tempo_medio'].iloc[0]
                        melhoria = ((tempo_quick_puro - tempo_quick_insertion) / tempo_quick_puro) * 100
                        melhorias_tipo['quick_insertion_sort'] = melhoria
                    
                    # Quick Sort Completo
                    quick_completo = df_filtrado[df_filtrado['algoritmo'].str.contains('Quick Sort Completo', na=False)]
                    if not quick_completo.empty:
                        tempo_quick_completo = quick_completo['tempo_medio'].iloc[0]
                        melhoria = ((tempo_quick_puro - tempo_quick_completo) / tempo_quick_puro) * 100
                        melhorias_tipo['quick_completo'] = melhoria
                
                melhorias[tamanho][tipo_dados] = melhorias_tipo
        
        return melhorias
    
    def salvar_resultados(self, arquivo_base: str = "experimento_expandido"):
        """Salvar resultados em diferentes formatos"""
        # Criar diretório de resultados se não existir
        Path("resultados_expandido").mkdir(exist_ok=True)
        
        # Salvar dados brutos em JSON
        with open(f"resultados_expandido/{arquivo_base}_dados.json", 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        # Salvar como CSV para análise
        df = pd.DataFrame(self.resultados)
        df.to_csv(f"resultados_expandido/{arquivo_base}_dados.csv", index=False, encoding='utf-8')
        
        # Calcular e salvar melhorias
        melhorias = self.calcular_melhorias()
        with open(f"resultados_expandido/{arquivo_base}_melhorias.json", 'w', encoding='utf-8') as f:
            json.dump(melhorias, f, indent=2, ensure_ascii=False)
        
        # Criar relatório resumido
        self.gerar_relatorio_resumido(f"resultados_expandido/{arquivo_base}_relatorio.md")
        
        print(f"\nResultados salvos em resultados_expandido/{arquivo_base}_*")
    
    def gerar_relatorio_resumido(self, arquivo: str):
        """Gerar relatório resumido em Markdown"""
        melhorias = self.calcular_melhorias()
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("# Relatório do Experimento Expandido\n\n")
            f.write("## Configuração do Experimento\n\n")
            f.write(f"- **Cutoff para Insertion Sort**: {self.cutoff}\n")
            f.write(f"- **Número de execuções por teste**: {self.num_execucoes}\n")
            f.write(f"- **Tamanhos testados**: {self.tamanhos}\n")
            f.write(f"- **Tipos de dados**: {self.tipos_dados}\n\n")
            
            f.write("## Análise de Melhorias (% de redução no tempo)\n\n")
            f.write("Valores positivos indicam melhoria (redução no tempo).\n")
            f.write("Valores negativos indicam piora (aumento no tempo).\n\n")
            
            for tamanho in self.tamanhos:
                f.write(f"### Tamanho: {tamanho:,} elementos\n\n")
                f.write("| Tipo de Dados | Merge+Insertion | Quick+Median | Quick+Insertion | Quick Completo |\n")
                f.write("|---------------|-----------------|--------------|-----------------|----------------|\n")
                
                for tipo_dados in self.tipos_dados:
                    if tamanho in melhorias and tipo_dados in melhorias[tamanho]:
                        m = melhorias[tamanho][tipo_dados]
                        linha = f"| {tipo_dados}"
                        linha += f" | {m.get('merge_insertion_sort', 'N/A'):.1f}%" if isinstance(m.get('merge_insertion_sort'), (int, float)) else " | N/A"
                        linha += f" | {m.get('quick_median_of_three', 'N/A'):.1f}%" if isinstance(m.get('quick_median_of_three'), (int, float)) else " | N/A"
                        linha += f" | {m.get('quick_insertion_sort', 'N/A'):.1f}%" if isinstance(m.get('quick_insertion_sort'), (int, float)) else " | N/A"
                        linha += f" | {m.get('quick_completo', 'N/A'):.1f}%" if isinstance(m.get('quick_completo'), (int, float)) else " | N/A"
                        linha += " |\n"
                        f.write(linha)
                    else:
                        f.write(f"| {tipo_dados} | N/A | N/A | N/A | N/A |\n")
                f.write("\n")
            
            f.write("## Interpretação dos Resultados\n\n")
            f.write("- **Merge+Insertion**: Impacto do Insertion Sort no Merge Sort\n")
            f.write("- **Quick+Median**: Impacto do Median-of-Three no Quick Sort\n")
            f.write("- **Quick+Insertion**: Impacto do Insertion Sort no Quick Sort\n")
            f.write("- **Quick Completo**: Impacto de todas as otimizações combinadas\n\n")
            
            # Adicionar estatísticas resumidas
            f.write("## Resumo dos Resultados\n\n")
            if self.resultados:
                df = pd.DataFrame(self.resultados)
                f.write(f"- **Total de testes executados**: {len(df)}\n")
                f.write(f"- **Algoritmos testados**: {df['algoritmo'].nunique()}\n")
                f.write(f"- **Tempo médio geral**: {df['tempo_medio'].mean():.2f} ms\n")
                f.write(f"- **Coeficiente de variação médio**: {df['cv'].mean():.1f}%\n")

def executar_experimento_rapido():
    """Executar um experimento rápido para teste"""
    print("Executando experimento expandido rápido...")
    
    experimento = ExperimentoExpandido(cutoff=10, num_execucoes=10)
    resultados = experimento.executar_experimento_completo()
    
    if resultados:
        experimento.salvar_resultados("teste_rapido")
        print(f"\nExperimento concluído! {len(resultados)} resultados obtidos.")
        
        # Mostrar alguns resultados
        print("\nPrimeiros resultados:")
        for i, resultado in enumerate(resultados[:5]):
            print(f"{i+1}. {resultado['algoritmo']}: {resultado['tempo_medio']:.2f}ms "
                  f"(tamanho: {resultado['tamanho']}, tipo: {resultado['tipo_dados']})")
    else:
        print("Nenhum resultado obtido. Verifique os erros acima.")

if __name__ == "__main__":
    executar_experimento_rapido()
