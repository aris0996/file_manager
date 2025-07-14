# File Manager Flask (Docker)

## Cara Menjalankan

1. Build dan jalankan dengan Docker Compose:

```bash
docker-compose up --build
```

2. Akses di browser:

    http://localhost:5000

## Fitur
- List, upload, download, delete, rename file/folder
- UI/UX rapi (HTML+JS)
- Siap deploy di Docker

---

**Catatan:**
- Semua file/folder dikelola relatif terhadap direktori kerja container.
- Untuk keamanan, batasi volume/akses folder sesuai kebutuhan. 