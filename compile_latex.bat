@echo off
echo 🔧 COMPILANDO ARTIGO LATEX PARA PDF
echo ===================================

REM Verificar se o arquivo existe
if not exist "artigo_ieee_portugues.tex" (
    echo ❌ Arquivo artigo_ieee_portugues.tex não encontrado!
    pause
    exit /b 1
)

echo 📄 Arquivo encontrado:
echo   - artigo_ieee_portugues.tex (PORTUGUÊS)

REM Construir imagem Docker
echo 🐳 Construindo imagem Docker para LaTeX...
docker build -f Dockerfile.latex -t latex-compiler .

if %ERRORLEVEL% neq 0 (
    echo ❌ Erro ao construir imagem Docker!
    pause
    exit /b 1
)

REM Compilar o documento
echo 📝 Compilando artigo em PORTUGUÊS...
docker run --rm -v "%cd%:/app" latex-compiler pdflatex -interaction=nonstopmode artigo_ieee_portugues.tex

if %ERRORLEVEL% equ 0 (
    echo ✅ Verificando arquivo gerado...
    if exist "artigo_ieee_portugues.pdf" (
        echo ✅ PDF gerado: artigo_ieee_portugues.pdf
        echo 📁 Localização: %cd%\artigo_ieee_portugues.pdf
        echo.
        echo 🚀 Abrindo PDF...
        start artigo_ieee_portugues.pdf
    ) else (
        echo ⚠️  Compilação executada, mas PDF não encontrado
        echo Verificando arquivos de log...
        if exist "artigo_ieee_portugues.log" (
            echo 📋 Últimas linhas do log:
            powershell "Get-Content artigo_ieee_portugues.log | Select-Object -Last 20"
        )
    )
) else (
    echo ❌ Erro na compilação!
    if exist "artigo_ieee_portugues.log" (
        echo 📋 Procurando erros no log:
        findstr /i "error" artigo_ieee_portugues.log
        if %ERRORLEVEL% neq 0 (
            echo Nenhum erro específico encontrado no log
        )
    )
)

echo.
echo 🏁 Processo concluído!
pause
