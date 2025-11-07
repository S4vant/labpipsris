import os
import socket
from pathlib import Path

def is_running_in_docker():
    """Надежное определение работы в Docker контейнере"""

    if os.path.exists('/.dockerenv'):
        return True
    
    try:
        with open('/proc/1/cgroup', 'r') as f:
            if 'docker' in f.read():
                return True
    except:
        pass
    
    hostname = socket.gethostname()
    if len(hostname) == 12 and all(c in '0123456789abcdef' for c in hostname):
        return True
    
    return False

def load_env(env_path=Path(__file__).resolve().parent.parent / 'backend/.env'):
    """Загружает .env файл, игнорируя форматирование."""
    try:
        with open(env_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip()
                    if key:
                        os.environ[key] = value
    except FileNotFoundError:
        print(f"Файл {env_path} не найден")
    except Exception as e:
        print(f"Ошибка при загрузке .env: {e}")


def creds():

    if is_running_in_docker():
        load_env(Path(__file__).resolve().parent.parent / '.env')
        print("Running in DOCKER")
         
    else:
        load_env()
        print("Running LOCALLY ")
    host_name = os.environ.get('DATABASE_NAME')
    user_name = os.environ.get('DATABASE_USERNAME')
    db_password = os.environ.get('DATABASE_ROOT_PASSWORD')
    db_port = os.environ.get('DATABASE_PORT')
    db_host = os.environ.get('DATABASE_HOST')
    secret_key = os.environ.get('SECRET_KEY')
    print( host_name, user_name, db_password, db_port, db_host)   
    return host_name, user_name, db_password, db_port, db_host, secret_key
