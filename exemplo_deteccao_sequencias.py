"""
Exemplo de Implementação da Detecção de Sequências Ordenadas no Merge Sort
Projeto: Análise de Algoritmos de Ordenação em Jogos Online
"""

from typing import List
import time

class MergeSortComDeteccao:
    """
    Merge Sort com detecção de sequências já ordenadas
    Otimização especial para leaderboards de jogos que são 
    frequentemente atualizados incrementalmente
    """
    
    def __init__(self):
        self.deteccoes_evitadas = 0  # Contador de merges evitados
        self.merges_realizados = 0   # Contador de merges necessários
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """
        Merge Sort com detecção de sequências ordenadas
        
        Otimização: Se esquerda[-1] <= direita[0], 
        significa que as duas metades já estão em ordem relativa,
        então podemos apenas concatenar ao invés de fazer merge.
        """
        self.deteccoes_evitadas = 0
        self.merges_realizados = 0
        
        resultado = self._merge_sort_recursivo(dados.copy())
        return resultado
    
    def _merge_sort_recursivo(self, dados: List[int]) -> List[int]:
        """Implementação recursiva com detecção"""
        if len(dados) <= 1:
            return dados
        
        # Dividir
        meio = len(dados) // 2
        esquerda = dados[:meio]
        direita = dados[meio:]
        
        # Conquistar (recursão)
        esquerda_ordenada = self._merge_sort_recursivo(esquerda)
        direita_ordenada = self._merge_sort_recursivo(direita)
        
        # 🔍 DETECÇÃO DE SEQUÊNCIA JÁ ORDENADA
        if len(esquerda_ordenada) > 0 and len(direita_ordenada) > 0:
            if esquerda_ordenada[-1] <= direita_ordenada[0]:
                # ✅ Já está ordenado! Evitar merge
                self.deteccoes_evitadas += 1
                return esquerda_ordenada + direita_ordenada
        
        # ❌ Precisa fazer merge normal
        self.merges_realizados += 1
        return self._merge(esquerda_ordenada, direita_ordenada)
    
    def _merge(self, esquerda: List[int], direita: List[int]) -> List[int]:
        """Merge tradicional quando detecção falha"""
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        # Adicionar elementos restantes
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado
    
    def get_estatisticas(self):
        """Retorna estatísticas da otimização"""
        total_operacoes = self.deteccoes_evitadas + self.merges_realizados
        if total_operacoes == 0:
            return {"eficiencia": 0, "merges_evitados": 0, "merges_realizados": 0}
        
        eficiencia = (self.deteccoes_evitadas / total_operacoes) * 100
        return {
            "eficiencia": eficiencia,
            "merges_evitados": self.deteccoes_evitadas,
            "merges_realizados": self.merges_realizados,
            "total_operacoes": total_operacoes
        }

class MergeSortClassico:
    """Merge Sort clássico para comparação"""
    
    def ordenar(self, dados: List[int]) -> List[int]:
        if len(dados) <= 1:
            return dados
        
        meio = len(dados) // 2
        esquerda = self.ordenar(dados[:meio])
        direita = self.ordenar(dados[meio:])
        
        return self._merge(esquerda, direita)
    
    def _merge(self, esquerda: List[int], direita: List[int]) -> List[int]:
        resultado = []
        i = j = 0
        
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        
        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])
        
        return resultado

def simular_leaderboard_gaming():
    """
    Simula cenários reais de leaderboards de jogos onde a
    detecção de sequências ordenadas seria mais eficaz
    """
    import random
    
    print("🎮 Simulação: Leaderboards de Jogos Online")
    print("=" * 50)
    
    # Cenário 1: Leaderboard quase ordenado (90% ordenado)
    dados_quase_ordenados = list(range(1, 1001))  # [1, 2, 3, ..., 1000]
    # Perturbar apenas 10% dos dados
    for _ in range(100):  # 10% de 1000
        i, j = random.randint(0, 999), random.randint(0, 999)
        dados_quase_ordenados[i], dados_quase_ordenados[j] = dados_quase_ordenados[j], dados_quase_ordenados[i]
    
    # Cenário 2: Dados completamente aleatórios
    dados_aleatorios = list(range(1, 1001))
    random.shuffle(dados_aleatorios)
    
    # Testar ambos os algoritmos
    merge_otimizado = MergeSortComDeteccao()
    merge_classico = MergeSortClassico()
    
    cenarios = [
        ("Leaderboard Quase-Ordenado (90%)", dados_quase_ordenados),
        ("Dados Completamente Aleatórios", dados_aleatorios)
    ]
    
    for nome_cenario, dados in cenarios:
        print(f"\n📊 {nome_cenario}")
        print("-" * 30)
        
        # Testar Merge Sort com detecção
        inicio = time.perf_counter()
        resultado_otimizado = merge_otimizado.ordenar(dados.copy())
        tempo_otimizado = time.perf_counter() - inicio
        
        # Testar Merge Sort clássico
        inicio = time.perf_counter()
        resultado_classico = merge_classico.ordenar(dados.copy())
        tempo_classico = time.perf_counter() - inicio
        
        # Verificar se resultados são iguais
        assert resultado_otimizado == resultado_classico, "Resultados diferentes!"
        
        # Estatísticas
        stats = merge_otimizado.get_estatisticas()
        melhoria = ((tempo_classico - tempo_otimizado) / tempo_classico) * 100
        
        print(f"⏱️  Tempo Clássico: {tempo_classico*1000:.2f}ms")
        print(f"⚡ Tempo Otimizado: {tempo_otimizado*1000:.2f}ms")
        print(f"📈 Melhoria: {melhoria:.1f}%")
        print(f"🔍 Eficiência da Detecção: {stats['eficiencia']:.1f}%")
        print(f"✅ Merges Evitados: {stats['merges_evitados']}")
        print(f"❌ Merges Realizados: {stats['merges_realizados']}")

def demonstrar_principio():
    """Demonstra o princípio básico da detecção"""
    print("\n🔬 Demonstração do Princípio de Detecção")
    print("=" * 40)
    
    # Exemplo simples onde detecção funciona
    dados_exemplo = [1, 3, 5, 7, 2, 4, 6, 8]
    print(f"Dados originais: {dados_exemplo}")
    
    merge_detector = MergeSortComDeteccao()
    resultado = merge_detector.ordenar(dados_exemplo)
    stats = merge_detector.get_estatisticas()
    
    print(f"Resultado ordenado: {resultado}")
    print(f"Merges evitados: {stats['merges_evitados']}")
    print(f"Merges realizados: {stats['merges_realizados']}")
    print(f"Eficiência: {stats['eficiencia']:.1f}%")

if __name__ == "__main__":
    demonstrar_principio()
    simular_leaderboard_gaming()
    
    print("\n" + "="*60)
    print("🎯 APLICAÇÃO EM JOGOS:")
    print("- Leaderboards atualizados incrementalmente")
    print("- Rankings de guilds/clãs parcialmente ordenados") 
    print("- Matchmaking com dados quase-estáveis")
    print("- Sistemas que mantêm ordem aproximada")
    print("="*60)
