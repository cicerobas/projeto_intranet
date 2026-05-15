FROM python:3.12-slim

# Evita que o Python gere arquivos de log em buffer (melhora visualização no docker logs)
ENV PYTHONUNBUFFERED=1
# Instrui o UV a compilar o bytecode, melhorando o tempo de inicialização da aplicação
ENV UV_COMPILE_BYTECODE=1

# Copia o UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copia apenas os arquivos de dependência primeiro
COPY pyproject.toml uv.lock ./

# Usa mount de cache para evitar que o cache do uv infle o tamanho da imagem final
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copia o restante do código
COPY . .

# Sincroniza o projeto em si
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Adiciona o ambiente virtual gerado pelo UV ao PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# CMD otimizado para produção. Use "dev" apenas localmente via docker-compose, se necessário.
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
