#!/bin/bash

echo "🔧 COMPILANDO ARTIGO LATEX PARA PDF"
echo "=================================="

# Verificar se o arquivo existe
if [ ! -f "artigo_ieee_latex.tex" ]; then
    echo "❌ Arquivo artigo_ieee_latex.tex não encontrado!"
    exit 1
fi

echo "📄 Arquivo encontrado: artigo_ieee_latex.tex"

# Construir imagem Docker
echo "🐳 Construindo imagem Docker para LaTeX..."
docker build -f Dockerfile.latex -t latex-compiler .

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagem Docker!"
    exit 1
fi

# Compilar o documento
echo "📝 Compilando documento LaTeX..."
docker run --rm -v "$(pwd):/app" latex-compiler

if [ $? -eq 0 ]; then
    if [ -f "artigo_ieee_latex.pdf" ]; then
        echo "✅ PDF gerado com sucesso: artigo_ieee_latex.pdf"
        echo "📁 Localização: $(pwd)/artigo_ieee_latex.pdf"
    else
        echo "⚠️  Compilação executada, mas PDF não encontrado"
        echo "Verificando arquivos de log..."
        if [ -f "artigo_ieee_latex.log" ]; then
            echo "📋 Últimas linhas do log:"
            tail -20 artigo_ieee_latex.log
        fi
    fi
else
    echo "❌ Erro na compilação!"
    if [ -f "artigo_ieee_latex.log" ]; then
        echo "📋 Erros encontrados:"
        grep -i error artigo_ieee_latex.log || echo "Nenhum erro específico encontrado no log"
    fi
fi

echo "🏁 Processo concluído!"
