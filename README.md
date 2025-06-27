# 🎮 Projeto Ordenação Jogos - Análise de Performance

Sistema completo para análise de performance de algoritmos de ordenação no contexto de jogos online.

## 🚀 Como Executar com Docker

### Opção 1: Windows (Simples)

```powershell
# 1. Setup inicial (primeira vez)
run.bat setup

# 2. Testar se funciona
run.bat test

# 3. Executar experimento completo
run.bat run
```

### Opção 2: Com Docker Compose

```powershell
# 1. Construir imagem
docker-compose build

# 2. Testar sistema
docker-compose up --rm test

# 3. Executar experimento
docker-compose up --rm run

# 4. Shell interativo (para debug)
docker-compose run --rm shell
```

### Opção 3: Com Make (se tiver make instalado)

```powershell
# Setup completo
make setup

# Teste rápido
make quick

# Executar experimento
make run
```

## 📂 Estrutura dos Resultados

Após executar, você terá:

```
📁 data/
   ├── resultados_experimento.json    # Resultados em JSON
   ├── resultados_experimento.csv     # Resultados em CSV
   ├── resultados_experimento.xlsx    # Resultados em Excel
   ├── relatorio_estatistico.json     # Análise estatística
   └── info_sistema.json              # Info do sistema

📁 plots/
   ├── comparativo_barras.png         # Gráfico comparativo
   ├── boxplots_distribuicao.png      # Box plots
   ├── escalabilidade_algoritmos.png  # Análise de escalabilidade
   ├── heatmap_correlacao.png         # Correlações
   ├── interacao_fatores.png          # Interações
   ├── throughput_algoritmos.png      # Throughput
   ├── memoria_vs_tempo.png           # Memória vs Tempo
   ├── grafico_3d_interativo.html     # Gráfico 3D interativo
   └── dashboard_interativo.html      # Dashboard completo

📁 relatorio/
   └── artigo_cientifico.md           # Artigo em Markdown

📁 logs/
   └── benchmark.log                  # Logs de execução
```

## 🎯 O que o Sistema Faz

### Experimento Fatorial 2³

**Fatores Testados:**
- **Fator A**: Tamanho (10.000 vs 100.000 elementos)
- **Fator B**: Distribuição (Exponencial vs Quase Ordenado)  
- **Fator C**: Algoritmo (Merge Sort vs Quick Sort)

**Total**: 8 combinações × 10 repetições = 80 execuções

### Contexto: Jogos Online

- **Distribuição Exponencial**: Simula pontuações reais onde poucos jogadores têm scores altos
- **Dados Quase Ordenados**: Simula rankings que são atualizados frequentemente
- **Métricas**: Tempo de execução, uso de memória, throughput

### Análises Realizadas

- ✅ Estatísticas descritivas completas
- ✅ ANOVA fatorial para identificar efeitos significativos
- ✅ Comparações par a par com correção de Bonferroni
- ✅ Cálculo de Effect Size (Cohen's d)
- ✅ Testes de normalidade
- ✅ Detecção de outliers
- ✅ Análise de correlações
- ✅ Intervalos de confiança (95%)

## 🛠️ Troubleshooting

### Se der erro no Docker:

```powershell
# Limpar containers
docker-compose down
docker system prune -f

# Rebuild
docker-compose build --no-cache
```

### Se der erro de memória:

```powershell
# Usar tamanhos menores para teste
# Edite src/main.py e mude:
TAMANHOS = [1000, 10000]  # ao invés de [10000, 100000]
```

### Ver logs em tempo real:

```powershell
docker-compose logs -f test
# ou
docker-compose logs -f run
```

## 📊 Exemplo de Saída

```
🎮 PROJETO: Avaliação de Algoritmos de Ordenação - Pontuações de Jogo Online
======================================================================

🧪 Executando testes do sistema...
✅ geradores.py - OK
✅ algoritmos.py - OK  
✅ benchmark.py - OK
✅ analise.py - OK
✅ visualizacao.py - OK

🚀 Executando experimento completo...
Experimento 1/8 (12.5%)
Testando Merge Sort com exponencial (10000 elementos)
...

🎉 Experimento concluído com sucesso!
📊 Verifique os arquivos em:
   - data/resultados_experimento.*
   - plots/ (gráficos)
   - relatorio/artigo_cientifico.md

📈 Resumo dos Resultados:
   • Total de experimentos: 8
   • Algoritmos testados: merge_sort, quick_sort
   • Tamanhos testados: 10000, 100000
   • Distribuições testadas: exponencial, quase_ordenado
   • Melhor performance: quick_sort com 0.0234s
```

## ⚙️ Configurações

Edite `src/config.py` para ajustar:

- Tamanhos dos datasets
- Número de repetições  
- Parâmetros dos geradores
- Configurações de visualização

## 🎓 Para o Artigo Científico

O sistema gera automaticamente:

1. **Dados estruturados** (JSON, CSV, Excel)
2. **Gráficos profissionais** (PNG de alta resolução)
3. **Análise estatística completa** (ANOVA, testes, correlações)
4. **Relatório base em Markdown** (para editar e expandir)
5. **Dashboards interativos** (HTML com Plotly)

## ❓ Precisa de Ajuda?

1. **Teste primeiro**: `run.bat test`
2. **Verifique logs**: `docker-compose logs test`
3. **Shell interativo**: `run.bat shell`
4. **Limpar tudo**: `run.bat clean`

---

🎮 **Contexto**: Este projeto simula cenários reais de jogos online onde é necessário ordenar rankings de jogadores com diferentes distribuições de pontuações, analisando qual algoritmo é mais eficiente para cada cenário.
