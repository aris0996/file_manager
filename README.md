# File Manager Server (FastAPI + React)

## Cara Jalankan (Linux)

1. Pastikan Docker & docker-compose sudah terinstall
2. Clone repo ini dan masuk ke folder project
3. Jalankan:

```bash
docker-compose up --build
```

4. Akses file manager di http://localhost:8000 (API) dan http://localhost:8000/static (UI)

## Struktur
- Backend: FastAPI (asynchronous)
- Frontend: React (Vite)
- Semua file di-manage di folder `data/` (otomatis dibuat)

## Fitur
- List, upload, download, delete, rename, preview file/folder
- UI modern, drag & drop upload
- Siap untuk deployment production 