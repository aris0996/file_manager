FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
COPY static/ ./static/
COPY templates/ ./templates/
EXPOSE 5000
CMD ["python", "backend/app.py"] 