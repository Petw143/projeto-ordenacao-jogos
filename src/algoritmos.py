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

class MergeSort(AlgoritmoOrdenacao):
    """Implementação do Merge Sort"""
    
    @property
    def nome(self) -> str:
        return "Merge Sort"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """
        Algoritmo Merge Sort
        
        Complexidade: O(n log n) sempre
        Estabilidade: Estável
        Uso em jogos: Ideal para rankings oficiais onde consistência é crucial
        """
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

class QuickSort(AlgoritmoOrdenacao):
    """Implementação do Quick Sort"""
    
    @property
    def nome(self) -> str:
        return "Quick Sort"
    
    def ordenar(self, dados: List[int]) -> List[int]:
        """
        Algoritmo Quick Sort
        
        Complexidade: O(n log n) médio, O(n²) pior caso
        Estabilidade: Não estável
        Uso em jogos: Rápido para ordenações temporárias durante partidas
        """
        if len(dados) <= 1:
            return dados
        
        return self._quicksort_recursivo(dados, 0, len(dados) - 1)
    
    def _quicksort_recursivo(self, dados: List[int], inicio: int, fim: int) -> List[int]:
        """Implementação recursiva do Quick Sort"""
        if inicio < fim:
            # Particionar e obter posição do pivot
            pivot_pos = self._particionar(dados, inicio, fim)
            
            # Ordenar recursivamente as duas partições
            self._quicksort_recursivo(dados, inicio, pivot_pos - 1)
            self._quicksort_recursivo(dados, pivot_pos + 1, fim)
        
        return dados
    
    def _particionar(self, dados: List[int], inicio: int, fim: int) -> int:
        """
        Particionar array usando o último elemento como pivot
        Otimização: usar mediana de três para melhor performance
        """
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