"""
Múltiplas implementações dos algoritmos de ordenação para análise comparativa

Este módulo contém diferentes versões dos algoritmos Merge Sort e Quick Sort
para permitir análise detalhada do impacto de otimizações específicas:

1. Versões puras (sem otimizações)
2. Versões com Insertion Sort para subarrays pequenos
3. Versões com Median-of-Three (Quick Sort)
4. Versões com todas as otimizações
"""

import time
from typing import List
from abc import ABC, abstractmethod

class AlgoritmoOrdenacao(ABC):
    """Classe base para algoritmos de ordenação"""
    
    @abstractmethod
    def ordenar(self, dados: List[int]) -> List[int]:
        """Método abstrato para ordenação"""
        pass
    
    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome do algoritmo"""
        pass

# ==================== INSERTION SORT ====================

class InsertionSort(AlgoritmoOrdenacao):
    """Insertion Sort para subarrays pequenos"""
    
    @property
    def nome(self) -> str:
        return "Insertion Sort"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Implementação clássica do Insertion Sort"""
        if len(dados) <= 1:
            return dados
        
        dados_copia = dados.copy()
        for i in range(1, len(dados_copia)):
            key = dados_copia[i]
            j = i - 1
            while j >= 0 and dados_copia[j] > key:
                dados_copia[j + 1] = dados_copia[j]
                j -= 1
            dados_copia[j + 1] = key
        
        return dados_copia

# ==================== MERGE SORT VARIANTES ====================

class MergeSortPuro(AlgoritmoOrdenacao):
    """Merge Sort sem otimizações"""
    
    @property
    def nome(self) -> str:
        return "Merge Sort (Puro)"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Implementação pura do Merge Sort - sem otimizações"""
        if len(dados) <= 1:
            return dados
        
        # Dividir
        meio = len(dados) // 2
        esquerda = dados[:meio]
        direita = dados[meio:]
        
        # Conquistar (recursão)
        esquerda_ordenada = self.ordenar(esquerda)
        direita_ordenada = self.ordenar(direita)
        
        # Combinar
        return self._merge(esquerda_ordenada, direita_ordenada)
    
    def _merge(self, esquerda: List[int], direita: List[int]) -> List[int]:
        """Combinar duas listas ordenadas"""
        resultado = []
        i = j = 0
        
        # Comparar e mesclar
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

class MergeSortComInsertionSort(AlgoritmoOrdenacao):
    """Merge Sort com Insertion Sort para subarrays pequenos"""
    
    def __init__(self, cutoff: int = 10):
        self.cutoff = cutoff
        self.insertion_sort = InsertionSort()
    
    @property
    def nome(self) -> str:
        return f"Merge Sort + Insertion Sort (cutoff={self.cutoff})"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Merge Sort com otimização para subarrays pequenos"""
        if len(dados) <= self.cutoff:
            return self.insertion_sort.ordenar(dados)
        
        # Dividir
        meio = len(dados) // 2
        esquerda = dados[:meio]
        direita = dados[meio:]
        
        # Conquistar (recursão)
        esquerda_ordenada = self.ordenar(esquerda)
        direita_ordenada = self.ordenar(direita)
        
        # Combinar
        return self._merge(esquerda_ordenada, direita_ordenada)
    
    def _merge(self, esquerda: List[int], direita: List[int]) -> List[int]:
        """Combinar duas listas ordenadas"""
        resultado = []
        i = j = 0
        
        # Comparar e mesclar
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

# ==================== QUICK SORT VARIANTES ====================

class QuickSortPuro(AlgoritmoOrdenacao):
    """Quick Sort sem otimizações"""
    
    @property
    def nome(self) -> str:
        return "Quick Sort (Puro)"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Quick Sort puro - último elemento como pivot"""
        if len(dados) <= 1:
            return dados
        
        dados_copia = dados.copy()
        return self._quicksort_recursivo(dados_copia, 0, len(dados_copia) - 1)
    
    def _quicksort_recursivo(self, dados: List[int], inicio: int, fim: int) -> List[int]:
        """Implementação recursiva do Quick Sort"""
        if inicio < fim:
            # Particionar e obter posição do pivot
            pivot_pos = self._particionar_simples(dados, inicio, fim)
            
            # Ordenar recursivamente as duas partições
            self._quicksort_recursivo(dados, inicio, pivot_pos - 1)
            self._quicksort_recursivo(dados, pivot_pos + 1, fim)
        
        return dados
    
    def _particionar_simples(self, dados: List[int], inicio: int, fim: int) -> int:
        """Particionamento simples - último elemento como pivot"""
        pivot = dados[fim]
        i = inicio - 1
        
        for j in range(inicio, fim):
            if dados[j] <= pivot:
                i += 1
                dados[i], dados[j] = dados[j], dados[i]
        
        dados[i + 1], dados[fim] = dados[fim], dados[i + 1]
        return i + 1

class QuickSortComMedianOfThree(AlgoritmoOrdenacao):
    """Quick Sort com Median-of-Three para seleção de pivot"""
    
    @property
    def nome(self) -> str:
        return "Quick Sort + Median-of-Three"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Quick Sort com median-of-three"""
        if len(dados) <= 1:
            return dados
        
        dados_copia = dados.copy()
        return self._quicksort_recursivo(dados_copia, 0, len(dados_copia) - 1)
    
    def _quicksort_recursivo(self, dados: List[int], inicio: int, fim: int) -> List[int]:
        """Implementação recursiva do Quick Sort"""
        if inicio < fim:
            # Particionar e obter posição do pivot
            pivot_pos = self._particionar_median_of_three(dados, inicio, fim)
            
            # Ordenar recursivamente as duas partições
            self._quicksort_recursivo(dados, inicio, pivot_pos - 1)
            self._quicksort_recursivo(dados, pivot_pos + 1, fim)
        
        return dados
    
    def _particionar_median_of_three(self, dados: List[int], inicio: int, fim: int) -> int:
        """Particionamento com median-of-three"""
        # Otimização: mediana de três para escolher pivot
        meio = (inicio + fim) // 2
        if dados[meio] < dados[inicio]:
            dados[inicio], dados[meio] = dados[meio], dados[inicio]
        if dados[fim] < dados[inicio]:
            dados[inicio], dados[fim] = dados[fim], dados[inicio]
        if dados[fim] < dados[meio]:
            dados[meio], dados[fim] = dados[fim], dados[meio]
        
        pivot = dados[fim]
        i = inicio - 1
        
        for j in range(inicio, fim):
            if dados[j] <= pivot:
                i += 1
                dados[i], dados[j] = dados[j], dados[i]
        
        dados[i + 1], dados[fim] = dados[fim], dados[i + 1]
        return i + 1

class QuickSortComInsertionSort(AlgoritmoOrdenacao):
    """Quick Sort com Insertion Sort para subarrays pequenos"""
    
    def __init__(self, cutoff: int = 10):
        self.cutoff = cutoff
        self.insertion_sort = InsertionSort()
    
    @property
    def nome(self) -> str:
        return f"Quick Sort + Insertion Sort (cutoff={self.cutoff})"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Quick Sort com otimização para subarrays pequenos"""
        if len(dados) <= self.cutoff:
            return self.insertion_sort.ordenar(dados)
        
        dados_copia = dados.copy()
        return self._quicksort_recursivo(dados_copia, 0, len(dados_copia) - 1)
    
    def _quicksort_recursivo(self, dados: List[int], inicio: int, fim: int) -> List[int]:
        """Implementação recursiva do Quick Sort"""
        if fim - inicio + 1 <= self.cutoff:
            # Usar insertion sort para subarrays pequenos
            subarray = dados[inicio:fim+1]
            subarray_ordenado = self.insertion_sort.ordenar(subarray)
            dados[inicio:fim+1] = subarray_ordenado
            return dados
        
        if inicio < fim:
            # Particionar e obter posição do pivot
            pivot_pos = self._particionar_simples(dados, inicio, fim)
            
            # Ordenar recursivamente as duas partições
            self._quicksort_recursivo(dados, inicio, pivot_pos - 1)
            self._quicksort_recursivo(dados, pivot_pos + 1, fim)
        
        return dados
    
    def _particionar_simples(self, dados: List[int], inicio: int, fim: int) -> int:
        """Particionamento simples - último elemento como pivot"""
        pivot = dados[fim]
        i = inicio - 1
        
        for j in range(inicio, fim):
            if dados[j] <= pivot:
                i += 1
                dados[i], dados[j] = dados[j], dados[i]
        
        dados[i + 1], dados[fim] = dados[fim], dados[i + 1]
        return i + 1

class QuickSortCompleto(AlgoritmoOrdenacao):
    """Quick Sort com todas as otimizações"""
    
    def __init__(self, cutoff: int = 10):
        self.cutoff = cutoff
        self.insertion_sort = InsertionSort()
    
    @property
    def nome(self) -> str:
        return f"Quick Sort Completo (cutoff={self.cutoff})"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """Quick Sort com todas as otimizações"""
        if len(dados) <= self.cutoff:
            return self.insertion_sort.ordenar(dados)
        
        dados_copia = dados.copy()
        return self._quicksort_recursivo(dados_copia, 0, len(dados_copia) - 1)
    
    def _quicksort_recursivo(self, dados: List[int], inicio: int, fim: int) -> List[int]:
        """Implementação recursiva do Quick Sort"""
        if fim - inicio + 1 <= self.cutoff:
            # Usar insertion sort para subarrays pequenos
            subarray = dados[inicio:fim+1]
            subarray_ordenado = self.insertion_sort.ordenar(subarray)
            dados[inicio:fim+1] = subarray_ordenado
            return dados
        
        if inicio < fim:
            # Particionar e obter posição do pivot
            pivot_pos = self._particionar_completo(dados, inicio, fim)
            
            # Ordenar recursivamente as duas partições
            self._quicksort_recursivo(dados, inicio, pivot_pos - 1)
            self._quicksort_recursivo(dados, pivot_pos + 1, fim)
        
        return dados
    
    def _particionar_completo(self, dados: List[int], inicio: int, fim: int) -> int:
        """Particionamento com median-of-three e insertion sort"""
        # Otimização: mediana de três para escolher pivot
        meio = (inicio + fim) // 2
        if dados[meio] < dados[inicio]:
            dados[inicio], dados[meio] = dados[meio], dados[inicio]
        if dados[fim] < dados[inicio]:
            dados[inicio], dados[fim] = dados[fim], dados[inicio]
        if dados[fim] < dados[meio]:
            dados[meio], dados[fim] = dados[fim], dados[meio]
        
        pivot = dados[fim]
        i = inicio - 1
        
        for j in range(inicio, fim):
            if dados[j] <= pivot:
                i += 1
                dados[i], dados[j] = dados[j], dados[i]
        
        dados[i + 1], dados[fim] = dados[fim], dados[i + 1]
        return i + 1

# ==================== FACTORY PARA CRIAR ALGORITMOS ====================

def criar_todos_algoritmos(cutoff: int = 10) -> List[AlgoritmoOrdenacao]:
    """Criar todas as variantes dos algoritmos para comparação"""
    return [
        # Insertion Sort (referência)
        InsertionSort(),
        
        # Merge Sort variantes
        MergeSortPuro(),
        MergeSortComInsertionSort(cutoff),
        
        # Quick Sort variantes
        QuickSortPuro(),
        QuickSortComMedianOfThree(),
        QuickSortComInsertionSort(cutoff),
        QuickSortCompleto(cutoff)
    ]

def criar_algoritmos_principais(cutoff: int = 10) -> List[AlgoritmoOrdenacao]:
    """Criar apenas os algoritmos principais para comparação focada"""
    return [
        MergeSortPuro(),
        MergeSortComInsertionSort(cutoff),
        QuickSortPuro(),
        QuickSortCompleto(cutoff)
    ]
