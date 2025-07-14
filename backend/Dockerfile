FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY package.json ./
COPY tailwind.config.js ./
COPY index.html ./index.html
COPY src ./src
# Hapus atau komentari baris berikut jika folder public tidak ada
# COPY public ./public
EXPOSE 5000
CMD ["python", "app.py"] 