import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "src", "backend", "InvenTree")
    venv_python = os.path.join(base_dir, "src", "backend", "venv", "bin", "python")

    # Automatically use the virtual environment python if we aren't already
    if os.path.exists(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python):
        print(f"Switching to virtual environment python: {venv_python}")
        os.execv(venv_python, [venv_python] + sys.argv)

    # Set default environment variables for a simple setup
    os.environ.setdefault("INVENTREE_DB_ENGINE", "sqlite3")
    os.environ.setdefault("INVENTREE_DB_NAME", os.path.join(base_dir, "database.sqlite3"))
    os.environ.setdefault("INVENTREE_SECRET_KEY", "student-presentation-secret-key-12345")
    os.environ.setdefault("INVENTREE_DEBUG", "True")
    os.environ.setdefault("INVENTREE_MEDIA_ROOT", os.path.join(base_dir, "media"))
    os.environ.setdefault("INVENTREE_STATIC_ROOT", os.path.join(base_dir, "static"))
    os.environ.setdefault("INVENTREE_BACKUP_DIR", os.path.join(base_dir, "backup"))
    os.environ.setdefault("INVENTREE_SITE_URL", "http://127.0.0.1:8000")
    
    manage_py = os.path.join(backend_dir, "manage.py")

    print("Running database migrations...")
    subprocess.run([sys.executable, manage_py, "migrate"], check=True)

    print("Collecting static files...")
    subprocess.run([sys.executable, manage_py, "collectstatic", "--noinput"], check=True)

    print("Creating superuser...")
    create_superuser_script = (
        "from django.contrib.auth import get_user_model; "
        "User = get_user_model(); "
        "User.objects.filter(username='admin').exists() or "
        "User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
    )
    subprocess.run([sys.executable, manage_py, "shell", "-c", create_superuser_script], check=True)

    print("======================================================")
    print("Setup complete! Starting the development server...")
    print("Access the application at: http://127.0.0.1:8000")
    print("Login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("======================================================")
    
    try:
        subprocess.run([sys.executable, manage_py, "runserver", "0.0.0.0:8000"])
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
