# File & Folder Manager Web App

Aplikasi manajemen file dan folder berbasis web untuk server Linux, dengan UI modern, keamanan ketat, dan siap deploy Docker.

## Fitur
- CRUD file & folder (create, rename, update, delete, edit file)
- Navigasi tree, breadcrumbs, search
- Keamanan JWT, validasi path, rate limit
- UI/UX modern (Tailwind), responsif, dark mode
- Logging & audit

## Struktur
- `backend/` — Flask API (Python)
- `frontend/` — React + Tailwind
- `docker-compose.yml` — Orchestration

## Cara Menjalankan
1. **Clone repo & build**
   ```bash
   docker-compose build
   docker-compose up
   ```
2. **Akses**
   - Frontend: `http://<IP Publik>:80`
   - Backend API: `http://<IP Publik>:5000`

## Konfigurasi
- Ubah `ROOT_DIR` di docker-compose untuk membatasi root file manager
- Ubah `JWT_SECRET` untuk keamanan token

## Keamanan
- Semua endpoint API dilindungi JWT
- Validasi path agar tidak bisa keluar root
- Rate limit API
- Logging setiap aksi
- Disarankan gunakan HTTPS (reverse proxy nginx)

## Catatan
- Untuk produksi, gunakan reverse proxy (nginx) dan HTTPS
- Pastikan volume `./data` hanya dapat diakses oleh user yang berwenang 