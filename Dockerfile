FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretórios necessários
RUN mkdir -p data plots relatorio logs cache notebooks

# Copiar código fonte
COPY src/ ./src/
COPY test_sistema.py .

# Dar permissões de execução
RUN chmod +x src/main.py

# Definir variáveis de ambiente
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Comando padrão para teste
CMD ["python", "test_sistema.py"]