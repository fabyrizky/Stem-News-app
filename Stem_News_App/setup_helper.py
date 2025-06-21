"""
Setup Helper untuk Future STEM News Intelligence
Script ini membantu setup otomatis untuk pemula
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class SetupHelper:
    def __init__(self):
        self.project_name = "future-stem-news"
        self.current_dir = Path.cwd()
        
    def print_header(self, text):
        print("\n" + "="*50)
        print(f"✨ {text}")
        print("="*50 + "\n")
    
    def check_python(self):
        """Check if Python is installed"""
        self.print_header("Checking Python Installation")
        try:
            version = subprocess.check_output([sys.executable, "--version"]).decode().strip()
            print(f"✅ Python terdeteksi: {version}")
            return True
        except:
            print("❌ Python tidak terdeteksi!")
            print("📌 Install Miniconda dari: https://docs.conda.io/en/latest/miniconda.html")
            return False
    
    def check_git(self):
        """Check if Git is installed"""
        self.print_header("Checking Git Installation")
        try:
            version = subprocess.check_output(["git", "--version"]).decode().strip()
            print(f"✅ Git terdeteksi: {version}")
            return True
        except:
            print("❌ Git tidak terdeteksi!")
            print("📌 Install Git dari: https://git-scm.com/downloads")
            return False
    
    def create_project_structure(self):
        """Create project folders and files"""
        self.print_header("Creating Project Structure")
        
        # Create project directory
        project_path = self.current_dir / self.project_name
        if not project_path.exists():
            project_path.mkdir()
            print(f"✅ Folder dibuat: {project_path}")
        else:
            print(f"📁 Folder sudah ada: {project_path}")
        
        # Change to project directory
        os.chdir(project_path)
        
        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env
.streamlit/secrets.toml

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.csv
temp/
"""
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ File dibuat: .gitignore")
        
        # Create README.md
        readme_content = """# Future STEM News Intelligence

🔬 Aplikasi web untuk mencari dan menganalisis berita STEM dengan rekomendasi personalisasi berdasarkan kepribadian pengguna.

## 🌟 Fitur
- 🔍 Pencarian berita STEM real-time
- 📊 Visualisasi data (grafik tren, word cloud)
- 🎯 Rekomendasi karier/proyek berdasarkan kepribadian
- 💾 Riwayat pencarian

## 🛠️ Teknologi
- Python 3.8+
- Streamlit
- NewsAPI
- Pandas, Matplotlib, Plotly

## 🚀 Demo
[Link Demo akan tersedia setelah deploy]

## 💻 Instalasi Lokal

### Prerequisites
- Python 3.8+
- Git

### Steps
1. Clone repository
```bash
git clone https://github.com/yourusername/future-stem-news.git
cd future-stem-news
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run aplikasi
```bash
streamlit run app.py
```

4. Buka browser di http://localhost:8501

## 📝 Konfigurasi
1. Dapatkan API key gratis dari [NewsAPI](https://newsapi.org)
2. Masukkan API key di sidebar aplikasi

## 👥 Kontribusi
Pull requests are welcome! Untuk perubahan besar, harap buka issue terlebih dahulu.

## 📄 Lisensi
[MIT](https://choosealicense.com/licenses/mit/)

## 🙏 Acknowledgments
- NewsAPI untuk data berita
- Streamlit untuk framework web app
- Komunitas Python Indonesia

---
Made with ❤️ by [Your Name]
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("✅ File dibuat: README.md")
        
        # Create requirements.txt
        requirements_content = """streamlit==1.31.0
pandas==2.0.3
matplotlib==3.7.2
wordcloud==1.9.3
requests==2.31.0
plotly==5.18.0"""
        with open("requirements.txt", "w") as f:
            f.write(requirements_content)
        print("✅ File dibuat: requirements.txt")
        
        # Create .streamlit folder and config
        streamlit_dir = Path(".streamlit")
        streamlit_dir.mkdir(exist_ok=True)
        
        config_content = """[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
headless = true
port = 8501
"""
        with open(streamlit_dir / "config.toml", "w") as f:
            f.write(config_content)
        print("✅ File dibuat: .streamlit/config.toml")
        
        print(f"\n📁 Struktur project berhasil dibuat di: {project_path}")
        return str(project_path)
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_header("Installing Dependencies")
        
        try:
            print("📦 Installing packages...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("\n✅ Semua dependencies berhasil diinstall!")
            return True
        except subprocess.CalledProcessError:
            print("\n❌ Error saat install dependencies!")
            print("📌 Coba install manual dengan: pip install -r requirements.txt")
            return False
    
    def setup_git(self):
        """Initialize Git repository"""
        self.print_header("Git Setup")
        
        try:
            # Check if already initialized
            if Path(".git").exists():
                print("📁 Git repository sudah ada")
                return True
            
            # Initialize git
            subprocess.run(["git", "init"], check=True)
            print("✅ Git repository initialized")
            
            # Add all files
            subprocess.run(["git", "add", "."], check=True)
            print("✅ Files added to git")
            
            # Initial commit
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            print("✅ Initial commit created")
            
            print("\n📌 Next steps:")
            print("1. Buat repository di GitHub")
            print("2. Jalankan perintah berikut:")
            print("   git remote add origin https://github.com/YOURUSERNAME/future-stem-news.git")
            print("   git push -u origin main")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Git error: {e}")
            return False
    
    def create_test_script(self):
        """Create a test script to verify installation"""
        self.print_header("Creating Test Script")
        
        test_content = '''"""
Test script untuk memverifikasi instalasi
"""

import sys
print("🔍 Checking installations...")

# Check Python version
print(f"\\n✅ Python version: {sys.version}")

# Check required libraries
libraries = [
    "streamlit",
    "pandas",
    "matplotlib",
    "wordcloud",
    "requests",
    "plotly"
]

failed = []
for lib in libraries:
    try:
        __import__(lib)
        print(f"✅ {lib} - OK")
    except ImportError:
        print(f"❌ {lib} - NOT FOUND")
        failed.append(lib)

if failed:
    print(f"\\n❌ Missing libraries: {', '.join(failed)}")
    print("📌 Run: pip install -r requirements.txt")
else:
    print("\\n🎉 All libraries installed successfully!")
    print("📌 You can now run: streamlit run app.py")
'''
        
        with open("test_installation.py", "w") as f:
            f.write(test_content)
        print("✅ File dibuat: test_installation.py")
        print("📌 Test dengan: python test_installation.py")
    
    def create_run_script(self):
        """Create batch/shell scripts for easy running"""
        self.print_header("Creating Run Scripts")
        
        # Windows batch file
        batch_content = """@echo off
echo Starting Future STEM News Intelligence...
echo.
streamlit run app.py
pause
"""
        with open("run_app.bat", "w") as f:
            f.write(batch_content)
        print("✅ File dibuat: run_app.bat (untuk Windows)")
        
        # Shell script for Mac/Linux
        shell_content = """#!/bin/bash
echo "Starting Future STEM News Intelligence..."
echo ""
streamlit run app.py
"""
        with open("run_app.sh", "w") as f:
            f.write(shell_content)
        
        # Make shell script executable
        try:
            subprocess.run(["chmod", "+x", "run_app.sh"], check=True)
        except:
            pass  # Windows doesn't have chmod
        
        print("✅ File dibuat: run_app.sh (untuk Mac/Linux)")
    
    def print_final_instructions(self):
        """Print final setup instructions"""
        self.print_header("Setup Complete! 🎉")
        
        print("📋 LANGKAH SELANJUTNYA:")
        print("\n1️⃣ Test instalasi:")
        print("   python test_installation.py")
        
        print("\n2️⃣ Jalankan aplikasi:")
        print("   • Windows: double-click run_app.bat")
        print("   • Atau: streamlit run app.py")
        
        print("\n3️⃣ Dapatkan API Key:")
        print("   • Kunjungi https://newsapi.org/register")
        print("   • Daftar gratis dan copy API key")
        
        print("\n4️⃣ Upload ke GitHub:")
        print("   • Buat repo baru di GitHub")
        print("   • Ikuti instruksi di panduan")
        
        print("\n5️⃣ Deploy ke Streamlit Cloud:")
        print("   • Login ke https://share.streamlit.io")
        print("   • Connect dengan GitHub")
        print("   • Deploy aplikasi")
        
        print("\n📚 RESOURCES:")
        print("   • Panduan lengkap: Lihat README.md")
        print("   • Streamlit docs: https://docs.streamlit.io")
        print("   • NewsAPI docs: https://newsapi.org/docs")
        
        print("\n✨ Happy coding! ✨")

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   Future STEM News Intelligence Setup Helper     ║
    ║              Untuk Pemula Coding                 ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    helper = SetupHelper()
    
    # Check prerequisites
    if not helper.check_python():
        return
    
    if not helper.check_git():
        print("\n⚠️  Git tidak wajib untuk testing lokal, tapi diperlukan untuk upload ke GitHub")
        response = input("\nLanjutkan tanpa Git? (y/n): ").lower()
        if response != 'y':
            return
    
    # Create project
    project_path = helper.create_project_structure()
    
    # Copy app.py if provided
    print("\n📌 IMPORTANT: Copy file app.py dari artifact ke folder project!")
    input("Press Enter setelah copy app.py...")
    
    # Install dependencies
    response = input("\nInstall dependencies sekarang? (y/n): ").lower()
    if response == 'y':
        helper.install_dependencies()
    
    # Create helper scripts
    helper.create_test_script()
    helper.create_run_script()
    
    # Git setup
    if helper.check_git():
        response = input("\nSetup Git repository? (y/n): ").lower()
        if response == 'y':
            helper.setup_git()
    
    # Final instructions
    helper.print_final_instructions()

if __name__ == "__main__":
    main()