# --- Backend ---
FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# --- Frontend ---
FROM node:20 AS frontend
WORKDIR /frontend
COPY frontend/ ./
RUN npm install && npm run build

# --- Final image ---
FROM python:3.11-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /frontend/dist /app/static
EXPOSE 8000
ENV BASE_DIR=/data
VOLUME ["/data"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 