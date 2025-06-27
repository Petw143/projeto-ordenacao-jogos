.PHONY: build test run shell clean logs help

# Construir a imagem Docker
build:
	@echo "🔨 Construindo imagem Docker..."
	docker-compose build

# Testar se o sistema funciona
test:
	@echo "🧪 Executando testes do sistema..."
	docker-compose run --rm test

# Executar experimento completo
run:
	@echo "🚀 Executando experimento completo..."
	docker-compose run --rm run

# Abrir shell interativo no container
shell:
	@echo "💻 Abrindo shell interativo..."
	docker-compose run --rm shell

# Ver logs em tempo real
logs:
	@echo "📋 Visualizando logs..."
	docker-compose logs -f

# Limpar containers parados
clean:
	@echo "🧹 Limpando containers..."
	docker-compose down
	docker system prune -f

# Remover tudo (cuidado!)
nuke:
	@echo "💥 Removendo tudo..."
	docker-compose down -v
	docker system prune -af
	docker volume prune -f

# Executar teste rápido (apenas build e test)
quick:
	@echo "⚡ Teste rápido..."
	docker-compose build
	docker-compose run --rm test

# Setup inicial completo
setup:
	@echo "🎯 Setup inicial completo..."
	docker-compose build
	@echo "✅ Docker build concluído!"
	@echo "🧪 Executando testes..."
	docker-compose run --rm test
	@echo "🎉 Setup concluído! Use 'make run' para executar o experimento."

# Ajuda
help:
	@echo "🎮 PROJETO ORDENAÇÃO JOGOS - Comandos Docker"
	@echo "════════════════════════════════════════════"
	@echo "make build  - Construir imagem Docker"
	@echo "make test   - Testar se sistema funciona"
	@echo "make run    - Executar experimento completo"
	@echo "make shell  - Abrir shell interativo"
	@echo "make logs   - Ver logs em tempo real"
	@echo "make clean  - Limpar containers"
	@echo "make quick  - Build + teste rápido"
	@echo "make setup  - Setup inicial completo"
	@echo "make help   - Mostrar esta ajuda"