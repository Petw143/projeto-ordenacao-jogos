#!/bin/bash

echo "🔧 COMPILANDO ARTIGO LATEX PARA PDF"
echo "=================================="

# Verificar se o arquivo existe
if [ ! -f "artigo_ieee_portugues.tex" ]; then
    echo "❌ Arquivo artigo_ieee_portugues.tex não encontrado!"
    exit 1
fi

echo "📄 Arquivo encontrado: artigo_ieee_portugues.tex"

# Construir imagem Docker
echo "🐳 Construindo imagem Docker para LaTeX..."
docker build -f Dockerfile.latex -t latex-compiler .

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagem Docker!"
    exit 1
fi

# Compilar o documento
echo "📝 Compilando documento LaTeX..."
docker run --rm -v "$(pwd):/app" latex-compiler pdflatex -interaction=nonstopmode artigo_ieee_portugues.tex

if [ $? -eq 0 ]; then
    if [ -f "artigo_ieee_portugues.pdf" ]; then
        echo "✅ PDF gerado com sucesso: artigo_ieee_portugues.pdf"
        echo "📁 Localização: $(pwd)/artigo_ieee_portugues.pdf"
    else
        echo "⚠️  Compilação executada, mas PDF não encontrado"
        echo "Verificando arquivos de log..."
        if [ -f "artigo_ieee_portugues.log" ]; then
            echo "📋 Últimas linhas do log:"
            tail -20 artigo_ieee_portugues.log
        fi
    fi
else
    echo "❌ Erro na compilação!"
    if [ -f "artigo_ieee_portugues.log" ]; then
        echo "📋 Erros encontrados:"
        grep -i error artigo_ieee_portugues.log || echo "Nenhum erro específico encontrado no log"
    fi
fi

echo "🏁 Processo concluído!"
