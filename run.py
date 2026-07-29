"""
Single-Click Entrypoint for NovaCart Enterprise AI Assistant.
Automatically verifies Python version, installs dependencies, runs tests,
indexes synthetic documents into ChromaDB, and launches FastAPI web app.

Usage:
    python run.py
"""
import sys
import os
import subprocess
import importlib

def print_header(title):
    print("\n" + "=" * 60)
    print(f" 🚀 {title}")
    print("=" * 60)

def step_1_check_python_version():
    print_header("Step 1: Checking Python Version")
    version = sys.version_info
    print(f"Current Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print("✅ Python version requirements satisfied.")

def step_2_check_and_install_dependencies():
    print_header("Step 2: Checking Dependencies")
    required_packages = ["fastapi", "uvicorn", "chromadb", "sentence_transformers", "pytest", "httpx"]
    missing = []
    
    for pkg in required_packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}...")
        req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("✅ Dependencies installed successfully.")
    else:
        print("✅ All required dependencies are already installed.")

def step_3_check_chroma_directory():
    print_header("Step 3: Preparing Vector Store Directory")
    chroma_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    if not os.path.exists(chroma_dir):
        os.makedirs(chroma_dir, exist_ok=True)
        print(f"✅ Created ChromaDB directory: {chroma_dir}")
    else:
        print(f"✅ ChromaDB directory ready: {chroma_dir}")

def step_4_run_tests():
    print_header("Step 4: Running Automated Test Suite")
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test_api.py")
    result = subprocess.run([sys.executable, "-m", "pytest", test_file, "-v"], capture_output=False)
    if result.returncode == 0:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n⚠️ Warning: Some tests failed. Proceeding with application launch...")

def step_5_start_fastapi():
    print_header("Step 5: Ingesting Data & Launching Application")
    print("""
============================================================
 NovaCart Enterprise AI Assistant is running.

 Dashboard:
 http://localhost:8000/

 API Docs:
 http://localhost:8000/docs

 Health Check:
 http://localhost:8000/health
============================================================
""")
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    step_1_check_python_version()
    step_2_check_and_install_dependencies()
    step_3_check_chroma_directory()
    step_4_run_tests()
    step_5_start_fastapi()
