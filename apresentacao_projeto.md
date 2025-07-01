# 🎮 Análise de Performance de Algoritmos de Ordenação em Rankings de Jogos Online

## Apresentação do Projeto

---

## 📋 Agenda

1. **Implementação dos Algoritmos**
   - Contexto e Motivação
   - Algoritmos Escolhidos
   - Otimizações Implementadas
   - Geradores de Dados

2. **Métricas Avaliadas**
   - Métricas de Performance
   - Experimento Fatorial 2³
   - Técnicas de Avaliação de Desempenho
   - Resultados Principais

---

# 1️⃣ IMPLEMENTAÇÃO DOS ALGORITMOS

---

## 🎯 Contexto e Motivação

### Por que Algoritmos de Ordenação em Jogos?

- **Rankings em Tempo Real**: Leaderboards dinâmicos
- **Sistemas de Matchmaking**: Pareamento por habilidade
- **Pontuações de Competições**: Torneios e eventos
- **Volume de Dados**: Milhões de jogadores simultâneos

### Desafios Específicos

- ⚡ **Latência Crítica**: Tempos de resposta < 100ms
- 📊 **Distribuições Não-Uniformes**: Poucos jogadores no topo
- 🔄 **Atualizações Frequentes**: Rankings dinâmicos
- 💾 **Restrições de Memória**: Servidores otimizados

---

## 🔧 Algoritmos Escolhidos

### Merge Sort
```python
def merge_sort_otimizado(arr):
    if len(arr) <= _THRESHOLD:
        return insertion_sort(arr)
    
    mid = len(arr) // 2
    left = merge_sort_otimizado(arr[:mid])
    right = merge_sort_otimizado(arr[mid:])
    
    return merge(left, right)
```

**Características:**
- ✅ **Estabilidade**: Preserva ordem de elementos iguais
- ✅ **Complexidade Garantida**: O(n log n) sempre
- ✅ **Previsibilidade**: Performance consistente
- ❌ **Uso de Memória**: O(n) espaço adicional

---

### Quick Sort
```python
def quick_sort_otimizado(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if high - low + 1 <= INSERTION_THRESHOLD:
        return insertion_sort_range(arr, low, high)
    
    if low < high:
        pivot = median_of_three_partition(arr, low, high)
        quick_sort_otimizado(arr, low, pivot - 1)
        quick_sort_otimizado(arr, pivot + 1, high)
```

**Características:**
- ✅ **Eficiência de Memória**: O(log n) espaço
- ✅ **Performance Média**: O(n log n)
- ✅ **Cache-Friendly**: Localidade de referência
- ❌ **Pior Caso**: O(n²) em dados ordenados

---

## ⚙️ Otimizações Implementadas

### 1. Insertion Sort para Arrays Pequenos
```python
INSERTION_THRESHOLD = 10

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

**Justificativa**: Insertion Sort é mais rápido para arrays < 10 elementos

---

### 2. Median-of-Three (Quick Sort)
```python
def median_of_three_partition(arr, low, high):
    mid = (low + high) // 2
    
    # Ordenar os três elementos
    if arr[mid] < arr[low]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[high] < arr[low]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[high] < arr[mid]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Usar mediana como pivot
    arr[mid], arr[high] = arr[high], arr[mid]
    return partition(arr, low, high)
```

**Benefícios**: Evita O(n²) em dados ordenados/reversos

---

## 📊 Geradores de Dados

### Distribuição Exponencial
```python
def gerar_exponencial(tamanho, lambda_param=0.001):
    """Simula pontuações de jogos competitivos"""
    uniform_samples = np.random.uniform(0, 1, tamanho)
    exponential_samples = -np.log(1 - uniform_samples) / lambda_param
    return np.round(exponential_samples).astype(int)
```

**Aplicação**: Rankings onde poucos jogadores têm scores altos

### Dados Quase-Ordenados (10% Perturbação)
```python
def gerar_quase_ordenado(tamanho, perturbacao=0.1):
    """Simula rankings parcialmente ordenados"""
    arr = list(range(1, tamanho + 1))
    num_trocas = int(tamanho * perturbacao)
    
    for _ in range(num_trocas):
        i, j = random.sample(range(tamanho), 2)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr
```

**Aplicação**: Leaderboards que recebem atualizações incrementais

---

# 2️⃣ MÉTRICAS AVALIADAS

---

## 📏 Métricas de Performance Coletadas

### 1. Tempo de Execução
```python
import time

inicio = time.perf_counter()
algoritmo_ordenacao(dados.copy())
fim = time.perf_counter()

tempo_execucao = fim - inicio  # segundos
```

**Precisão**: Nanosegundos com `time.perf_counter()`

### 2. Uso de Memória
```python
import tracemalloc

tracemalloc.start()
algoritmo_ordenacao(dados.copy())
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

memoria_mb = peak / 1024 / 1024  # MB
```

**Medição**: Pico de memória durante execução

### 3. Throughput
```python
throughput = tamanho_dados / tempo_execucao  # elementos/segundo
```

**Interpretação**: Eficiência de processamento

---

## 🧪 Experimento Fatorial 2³

### Design Experimental

| Fator | Nível 1 | Nível 2 |
|-------|---------|---------|
| **A - Algoritmo** | Merge Sort | Quick Sort |
| **B - Tamanho** | 10.000 | 100.000 |
| **C - Distribuição** | Exponencial | Quase-ordenado |

**Total**: 2³ = 8 combinações × 10 repetições = **80 execuções**

### Combinações Testadas

1. Merge Sort + 10k + Exponencial
2. Merge Sort + 10k + Quase-ordenado
3. Merge Sort + 100k + Exponencial
4. Merge Sort + 100k + Quase-ordenado
5. Quick Sort + 10k + Exponencial
6. Quick Sort + 10k + Quase-ordenado
7. Quick Sort + 100k + Exponencial
8. Quick Sort + 100k + Quase-ordenado

---

## 📊 Técnicas de Avaliação de Desempenho

### 1. Gráficos de Médias
- **Comparação visual** entre algoritmos
- **Barras de erro** (desvio padrão)
- **Identificação rápida** de diferenças

### 2. Intervalos de Confiança (95%)
- **Precisão das estimativas**
- **Quantificação da variabilidade**
- **Confiabilidade estatística**

### 3. Box Plots
- **Distribuição completa** dos tempos
- **Detecção de outliers**
- **Análise de quartis**

### 4. ANOVA Fatorial
- **Efeitos principais** de cada fator
- **Interações entre fatores**
- **Significância estatística**

---

## 🎯 Resultados Principais

### Hierarquia de Fatores (η²)

1. **🥇 TAMANHO** (69.5% da variância)
   - Fator dominante
   - Impacto exponencial: 12x diferença

2. **🥈 ALGORITMO** (28.5% da variância)
   - Moderadamente importante
   - Varia com interações

3. **🥉 DISTRIBUIÇÃO** (14.7% da variância)
   - Menor impacto individual
   - Crucial para interações

---

### Descobertas das Interações

#### 🔄 Algoritmo × Tamanho
- **Ponto de Inversão**: ~50.000 elementos
- **Dados Pequenos**: Quick Sort 7-19% melhor
- **Dados Grandes**: Merge Sort 14-39% superior

#### 🔄 Algoritmo × Distribuição
- **Quick Sort**: 47% mais lento (exponencial vs. quase-ordenado)
- **Merge Sort**: Apenas 5% de diferença (mais robusto)

#### 🔄 Cenários Extremos
- **Pior**: Quick Sort + 100k + Exponencial (1210ms)
- **Melhor**: Quick Sort + 10k + Exponencial (52ms)
- **Razão**: 23,3x de diferença

---

## 📈 Intervalos de Confiança (95%)

| Algoritmo | Tamanho | Distribuição | Tempo (ms) | IC Inferior | IC Superior |
|-----------|---------|--------------|------------|-------------|-------------|
| Merge Sort | 10k | Exponencial | 64.27 | 62.14 | 66.41 |
| Quick Sort | 10k | Exponencial | 51.79 | 46.97 | 56.61 |
| Merge Sort | 100k | Exponencial | 742.47 | 727.35 | 757.60 |
| Quick Sort | 100k | Exponencial | 1210.07 | 1166.88 | 1253.26 |

**Observação**: Quick Sort apresenta maior variabilidade em datasets grandes

---

## 🎯 Recomendações para Sistemas de Jogos

### Cenários de Aplicação

#### 🎮 Leaderboards Dinâmicos (< 50k jogadores)
- **Algoritmo**: Quick Sort
- **Vantagem**: 7-19% mais rápido
- **Uso de Memória**: 98.9% menos memória

#### 🏆 Rankings Globais (> 50k jogadores)
- **Algoritmo**: Merge Sort
- **Vantagem**: 14-39% mais rápido
- **Estabilidade**: Performance previsível

#### ⚡ Sistemas Críticos (latência garantida)
- **Algoritmo**: Merge Sort
- **Justificativa**: Complexidade O(n log n) garantida
- **Trade-off**: Maior uso de memória

---

## 🔬 Validação dos Requisitos

### ✅ Técnicas de Avaliação de Desempenho
- Gráficos de médias com barras de erro
- Intervalos de confiança (95%)
- Análise de interações entre fatores
- Box plots e correlações
- ANOVA fatorial 2³

### ✅ Discussão de Fatores de Impacto
- Hierarquia quantificada (η²)
- Efeitos principais e interações
- Cenários extremos identificados
- Recomendações contextualizadas

---

## 🙏 Agradecimentos

Os autores agradecem à Universidade Federal de Itajubá pelo suporte institucional. Agradecemos especialmente aos professores **Edmilson Marmo Moreira** e **Bruno Tardiole Kuehne** pela orientação do desenvolvimento deste trabalho.

**Repositório**: github.com/Petw143/projeto-ordenacao-jogos

---

## ❓ Perguntas?

**Dúvidas sobre:**
- Implementação dos algoritmos
- Metodologia experimental
- Análise estatística
- Aplicações práticas

---

**Obrigado pela atenção!** 🎮📊

---

## 🔬 Análise Detalhada das Otimizações

### Múltiplas Versões Implementadas

Para eliminar viés experimental e quantificar o impacto individual de cada otimização, implementamos **6 variantes** dos algoritmos:

#### **Merge Sort - 2 Versões**
1. **Merge Sort Puro**: Implementação clássica sem otimizações
2. **Merge Sort + Insertion Sort**: Com cutoff para subarrays pequenos

#### **Quick Sort - 4 Versões**
1. **Quick Sort Puro**: Implementação clássica (último elemento como pivot)
2. **Quick Sort + Median-of-Three**: Otimização na seleção do pivot
3. **Quick Sort + Insertion Sort**: Com cutoff para subarrays pequenos
4. **Quick Sort Completo**: Todas as otimizações combinadas

#### **Insertion Sort - 1 Versão**
- **Insertion Sort**: Algoritmo base para comparação e cutoff

---

### 📊 Impacto Individual das Otimizações

#### **Teste Preliminar (100 elementos)**

| Algoritmo | Tempo (ms) | Posição | Observações |
|-----------|------------|---------|-------------|
| Quick Sort (Puro) | 0.08 | 🥇 1º | Mais rápido para dados pequenos |
| Quick Sort Completo | 0.09 | 🥈 2º | Overhead mínimo das otimizações |
| Merge Sort + Insertion | 0.16 | 🥉 3º | Benefício do cutoff visível |
| Merge Sort (Puro) | 0.18 | 4º | Baseline para comparação |

#### **Descobertas Importantes**

1. **🎯 Insertion Sort Cutoff**
   - **Merge Sort**: 11% de melhoria (0.18ms → 0.16ms)
   - **Quick Sort**: Overhead mínimo em dados pequenos
   - **Ponto ótimo**: ~10 elementos

2. **🎯 Median-of-Three (Quick Sort)**
   - **Benefício**: Evita O(n²) em dados ordenados/reversos
   - **Trade-off**: Overhead computacional em dados aleatórios
   - **Essencial**: Para dados quase-ordenados

3. **🎯 Otimizações Combinadas**
   - **Efeito sinérgico**: Nem sempre aditivo
   - **Overhead aceitável**: <13% em datasets pequenos
   - **Benefício escalonável**: Maior em datasets grandes

---

### 🧪 Metodologia de Comparação Justa

#### **Eliminação de Viés**
- **Versões puras**: Sem nenhuma otimização
- **Otimizações isoladas**: Uma por vez
- **Mesmos dados**: Identical datasets para todas as versões
- **Múltiplas execuções**: 20+ repetições por teste

#### **Cenários de Teste**
- **Dados aleatórios**: Performance média
- **Dados quase-ordenados**: Casos reais (10% perturbação)
- **Múltiplos tamanhos**: 1k, 5k, 10k, 20k elementos
- **Métricas robustas**: Tempo médio, mediano, CV%

---
