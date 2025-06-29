# 📄 ARTIGO CIENTÍFICO GERADO - VERSÃO COMPLETA

## ✅ **ARQUIVO CRIADO**

### **📊 Artigo com TODOS os Gráficos:**
- `artigo_ieee_portugues.pdf` ← **VERSÃO EM PORTUGUÊS** (4 páginas, 2.6MB)

### **📁 Arquivo Fonte:**
- `artigo_ieee_portugues.tex` ← Código LaTeX em português

### **🇧🇷 VERSÃO EM PORTUGUÊS (`artigo_ieee_portugues.pdf`)**
- ✅ **Resumo em português** (primeira seção)
- ✅ **Abstract em inglês** (tradução do resumo português)
- ✅ **Palavras-chave em português e inglês**
- ✅ **Conteúdo completo em português**
- ✅ **8 gráficos incluídos** (todos da pasta `plots/`)
- ✅ **Formato IEEE Conference**
- ✅ **4 páginas completas**
- ✅ **Pseudocódigos dos algoritmos**
- ✅ **Análise estatística detalhada**

## 📊 **GRÁFICOS INCLUÍDOS NO ARTIGO**

O artigo inclui **TODOS** os 8 gráficos gerados pelo projeto:

1. **`boxplots_distribuicao.png`** → Box plots por algoritmo, tamanho e distribuição
2. **`comparativo_barras.png`** → Comparação de barras entre algoritmos  
3. **`escalabilidade_algoritmos.png`** → Análise de escalabilidade
4. **`heatmap_correlacao.png`** → Heatmap de correlação entre métricas
5. **`interacao_fatores.png`** → Análise de interação entre fatores
6. **`memoria_vs_tempo.png`** → Trade-off memória vs tempo
7. **`distribuicao_tempos.png`** → Distribuição dos tempos de execução
8. **`throughput_algoritmos.png`** → Comparação de throughput

## 🚀 **COMO FORAM COMPILADOS**

```bash
# Via Docker (recomendado)
.\run.bat latex

# Ou via docker-compose
docker-compose run --rm latex pdflatex -interaction=nonstopmode artigo_ieee_latex.tex
docker-compose run --rm latex pdflatex -interaction=nonstopmode artigo_ieee_portugues.tex
```

## 📋 **ESTRUTURA COMPLETA DO ARTIGO**

### **🎯 Seções Principais:**
1. **Resumo** (português)
2. **Abstract** (inglês)
3. **Palavras-chave** (português e inglês)
4. **Introdução**
5. **Trabalhos Relacionados**
6. **Metodologia** (design experimental 2³)
7. **Implementação** (pseudocódigos)
8. **Resultados e Análise** (com TODOS os gráficos)
9. **Discussão** (implicações práticas)
10. **Conclusão** (contribuições e trabalhos futuros)
11. **Referências** (referências reais formato IEEE)

### **📈 Resultados Destacados:**
- **Quick Sort 22.6% mais rápido** em distribuições exponenciais
- **Merge Sort mais estável** em diferentes distribuições  
- **Análise estatística completa** (ANOVA, Cohen's d, IC 95%)
- **Crossover point** em ~50.000 elementos
- **Recomendações práticas** para sistemas de jogos

## 🎓 **PRONTO PARA SUBMISSÃO**

O artigo está **pronto para submissão acadêmica**:

- ✅ **Formato IEEE Conference rigoroso**
- ✅ **Figuras numeradas e referenciadas**
- ✅ **Análise estatística robusta**
- ✅ **Metodologia experimental sólida**
- ✅ **Contribuições científicas claras**
- ✅ **Bibliografia no formato IEEE**

## 🔧 **PERSONALIZAÇÃO**

Para submeter, apenas substitua:
- **Nome:** `Pedro Henrique dos Santos Barbosa` → Seu nome
- **Email:** `d2022013760@unifei.edu.br` → Seu email

## 📊 **MÉTRICAS DO ARQUIVO**

| Versão | Páginas | Tamanho | Gráficos | Idioma | Resumo |
|--------|---------|---------|----------|---------|---------|
| Português | 4 | 2.6MB | 8 | 🇧🇷 Português | Resumo (PT) + Abstract (EN) |

## 🚀 **COMO COMPILAR**

```bash
# Usando docker-compose
.\run.bat latex

# Ou diretamente
docker-compose run --rm latex pdflatex -interaction=nonstopmode artigo_ieee_portugues.tex
```

## 🎯 **PRÓXIMOS PASSOS**

1. **Revisar** o PDF gerado
2. **Personalizar** nome e email se necessário
3. **Submeter** conforme instruções do professor
4. **Celebrar** o trabalho completo! 🎉

---

**🏆 PARABÉNS! Você agora tem um artigo científico completo e profissional no formato IEEE, com todos os gráficos e análises do seu projeto!** 
