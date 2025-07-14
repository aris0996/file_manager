# 🔧 Troubleshooting Guide - File Manager & Terminal

## 🚨 **Masalah Login**

### **Gejala: Tidak bisa login dengan admin/admin123**

#### **Solusi 1: Restart Aplikasi dengan Clean State**

**Linux/Mac:**
```bash
chmod +x restart_app.sh
./restart_app.sh
```

**Windows:**
```cmd
restart_app.bat
```

#### **Solusi 2: Test Login System**

```bash
# Test credentials dan login system
python3 test_login.py
```

#### **Solusi 3: Manual Reset**

```bash
# 1. Stop aplikasi (Ctrl+C)
# 2. Clean session files
rm -rf flask_session .flask_session session .session

# 3. Restart aplikasi
python3 app.py
```

#### **Solusi 4: Cek User Credentials**

```bash
# Generate dan cek user credentials
python3 reset_users.py
```

### **Gejala: "Invalid username or password"**

#### **Kemungkinan Penyebab:**
1. **Session cache** - Browser menyimpan session lama
2. **Aplikasi tidak restart** - Masih pakai konfigurasi lama
3. **Hash mismatch** - Password hash tidak sesuai

#### **Solusi:**
1. **Clear browser cache** - Ctrl+Shift+Delete
2. **Restart aplikasi** - Gunakan `restart_app.sh` atau `restart_app.bat`
3. **Test credentials** - Jalankan `test_login.py`

### **Gejala: "Cannot connect to localhost:5000"**

#### **Solusi:**
1. **Cek apakah aplikasi running:**
   ```bash
   # Linux/Mac
   ps aux | grep python
   
   # Windows
   tasklist | findstr python
   ```

2. **Start aplikasi:**
   ```bash
   python3 app.py
   ```

3. **Cek port:**
   ```bash
   # Linux/Mac
   netstat -tlnp | grep 5000
   
   # Windows
   netstat -an | findstr 5000
   ```

## 🔍 **Debugging Steps**

### **Step 1: Check System Compatibility**
```bash
# Linux/Mac
chmod +x check_system.sh
./check_system.sh

# Windows
check_system.bat
```

### **Step 2: Check Application Logs**
```bash
# Jika aplikasi running dengan nohup
tail -f app.log

# Jika running manual, lihat output di terminal
```

### **Step 3: Test Login API**
```bash
# Test login endpoint
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### **Step 4: Check Debug Endpoints**
```bash
# Check users
curl http://localhost:5000/debug/users

# Check session
curl http://localhost:5000/debug/session
```

## 🐳 **Docker Issues**

### **Error: "Docker Compose is not installed"**

#### **Solusi:**
1. **Install Docker Desktop** - Sudah include Docker Compose v2
2. **Update deploy.sh** - Sudah diperbaiki untuk Docker Compose v2
3. **Manual command:**
   ```bash
   docker compose up -d --build
   ```

### **Error: "Port already in use"**

#### **Solusi:**
1. **Stop existing containers:**
   ```bash
   docker compose down
   ```

2. **Change port in docker-compose.yml:**
   ```yaml
   ports:
     - "8080:5000"  # Change 5000 to 8080
   ```

3. **Restart:**
   ```bash
   docker compose up -d
   ```

## 🐍 **Python Issues**

### **Error: "Module not found"**

#### **Solusi:**
```bash
# Install dependencies
pip install -r requirements.txt

# Atau dengan virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **Error: "Permission denied"**

#### **Solusi:**
```bash
# Linux/Mac - Give execute permission
chmod +x *.sh

# Windows - Run as Administrator
```

## 🔐 **Security Issues**

### **Default Passwords Still Active**

#### **Solusi:**
1. **Login sebagai admin**
2. **Ganti password di aplikasi** (jika ada fitur)
3. **Atau edit app.py** untuk ganti password hash

### **Session Security**

#### **Solusi:**
1. **Ganti SECRET_KEY di app.py:**
   ```python
   app.config['SECRET_KEY'] = 'your-new-secret-key-here'
   ```

2. **Enable HTTPS** untuk production

## 📱 **Browser Issues**

### **Cache Problems**

#### **Solusi:**
1. **Hard refresh:** Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)
2. **Clear cache:** Ctrl+Shift+Delete
3. **Incognito/Private mode**

### **JavaScript Errors**

#### **Solusi:**
1. **Open Developer Tools:** F12
2. **Check Console tab** untuk errors
3. **Check Network tab** untuk failed requests

## 🚀 **Quick Fix Commands**

### **Complete Reset (Linux/Mac):**
```bash
# Stop everything
pkill -f python
pkill -f flask

# Clean everything
rm -rf flask_session .flask_session session .session venv

# Reinstall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start fresh
python3 app.py
```

### **Complete Reset (Windows):**
```cmd
# Stop everything
taskkill /f /im python.exe

# Clean everything
rmdir /s /q flask_session .flask_session session .session venv

# Reinstall
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Start fresh
python app.py
```

## 📞 **Still Having Issues?**

### **Check These Files:**
1. **app.py** - Main application file
2. **requirements.txt** - Dependencies
3. **templates/login.html** - Login page
4. **app.log** - Application logs

### **Common Commands:**
```bash
# Check if app is running
curl http://localhost:5000/login

# Check Python version
python3 --version

# Check installed packages
pip list

# Check system resources
top  # Linux/Mac
taskmgr  # Windows
```

### **Get Help:**
1. **Run system check:** `./check_system.sh`
2. **Test login:** `python3 test_login.py`
3. **Check logs:** `tail -f app.log`
4. **Restart clean:** `./restart_app.sh`

---

**🎯 Most Common Solution:**
```bash
# 1. Stop aplikasi
# 2. Run restart script
./restart_app.sh  # Linux/Mac
restart_app.bat   # Windows

# 3. Test login
python3 test_login.py

# 4. Access di browser
# http://localhost:5000
# admin / admin123
``` 