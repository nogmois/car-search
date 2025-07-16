FROM python:3.12-slim

WORKDIR /app

# 2. Copia e instala deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o código
COPY . .

# 4. Expõe porta MCP
EXPOSE 5000

# 5. Comando padrão: inicia o MCP Server
CMD ["python", "-m", "app.mcp.server", "--host", "0.0.0.0", "--port", "5000"]
