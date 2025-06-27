@echo off
REM Script para executar o projeto no Windows sem make

echo 🎮 PROJETO ORDENACAO JOGOS - Setup Docker
echo ==========================================

if "%1"=="build" (
    echo 🔨 Construindo imagem Docker...
    docker-compose build
    goto end
)

if "%1"=="test" (
    echo 🧪 Executando testes do sistema...
    docker-compose run --rm test
    goto end
)

if "%1"=="run" (
    echo 🚀 Executando experimento completo...
    docker-compose run --rm run
    goto end
)

if "%1"=="shell" (
    echo 💻 Abrindo shell interativo...
    docker-compose run --rm shell
    goto end
)

if "%1"=="clean" (
    echo 🧹 Limpando containers...
    docker-compose down
    docker system prune -f
    goto end
)

if "%1"=="setup" (
    echo 🎯 Setup inicial completo...
    docker-compose build
    echo ✅ Docker build concluído!
    echo 🧪 Executando testes...
    docker-compose run --rm test
    echo 🎉 Setup concluído! Use 'run.bat run' para executar o experimento.
    goto end
)

if "%1"=="quick" (
    echo ⚡ Teste rápido...
    docker-compose build
    docker-compose run --rm test
    goto end
)

REM Se nenhum argumento ou help
echo 🎮 PROJETO ORDENAÇÃO JOGOS - Comandos Docker
echo ════════════════════════════════════════════
echo run.bat build  - Construir imagem Docker
echo run.bat test   - Testar se sistema funciona
echo run.bat run    - Executar experimento completo
echo run.bat shell  - Abrir shell interativo
echo run.bat clean  - Limpar containers
echo run.bat quick  - Build + teste rápido
echo run.bat setup  - Setup inicial completo
echo.
echo 💡 COMO USAR:
echo 1. run.bat setup    (primeira vez)
echo 2. run.bat test     (verificar se funciona)
echo 3. run.bat run      (executar experimento)

:end
