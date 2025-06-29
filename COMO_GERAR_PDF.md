# 📄 COMO GERAR PDF DO ARTIGO LATEX

## 🚀 **MÉTODOS DISPONÍVEIS**

### **💻 1. MÉTODO MAIS FÁCIL - OVERLEAF (RECOMENDADO)**

```bash
1. Acesse: https://www.overleaf.com
2. Crie conta gratuita
3. New Project → Blank Project
4. Copie o conteúdo de artigo_ieee_portugues.tex
5. Cole no main.tex do Overleaf
6. Clique "Recompile" (botão verde)
7. Download PDF pronto! ✅
```

### **🐳 2. MÉTODO COM DOCKER (LOCAL)**

#### **Windows:**
```powershell
# Gerar PDF automaticamente
.\run.bat latex

# Ou manualmente
docker-compose run --rm latex
```

#### **Linux/Mac:**
```bash
# Gerar PDF automaticamente
make latex

# Ou manualmente
docker-compose run --rm latex
```

### **🔧 3. MÉTODO MANUAL (SE TIVER LATEX INSTALADO)**

#### **Windows:**
```powershell
# Se tiver MiKTeX ou TeX Live instalado
pdflatex artigo_ieee_portugues.tex
```

#### **Linux:**
```bash
# Se tiver texlive instalado
pdflatex artigo_ieee_portugues.tex
```

## ⚡ **GUIA RÁPIDO**

### **Para quem tem Docker:**
```powershell
# 1. Compilar PDF
.\run.bat latex

# 2. PDF será gerado como: artigo_ieee_latex.pdf
# 3. Será aberto automaticamente!
```

### **Para quem não tem Docker:**
1. Use o **Overleaf** (método mais fácil)
2. Ou instale LaTeX local (mais complexo)

## 🎯 **ARQUIVOS CRIADOS**

- `artigo_ieee_portugues.tex` ← Arquivo principal LaTeX
- `compile_latex.bat` ← Script Windows para compilar
- `compile_latex.sh` ← Script Linux para compilar  
- `Dockerfile.latex` ← Docker para LaTeX
- Entrada no `docker-compose.yml` e `run.bat`

## ✅ **VERIFICAÇÃO**

Após compilar, você deve ter:
- `artigo_ieee_latex.pdf` ← **SEU ARTIGO EM PDF**
- `artigo_ieee_latex.log` ← Log da compilação
- `artigo_ieee_latex.aux` ← Arquivo auxiliar

## 🚨 **TROUBLESHOOTING**

### **Se der erro:**
1. **Overleaf**: Use sempre como fallback
2. **Docker**: Verifique se Docker está rodando
3. **Local**: Instale pacotes LaTeX faltantes

### **Pacotes necessários:**
- IEEEtran (template IEEE)
- amsmath, graphicx, booktabs
- cite, algorithmic, textcomp

## 🎓 **RESULTADO FINAL**

O PDF gerado será um **artigo científico completo** no formato IEEE Conference, pronto para submissão acadêmica!

---

**💡 DICA:** Use o **Overleaf** se quiser facilidade e garantia de que vai funcionar!
