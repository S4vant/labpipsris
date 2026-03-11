import os
import socket
from pathlib import Path

def is_running_in_docker():
    """Надежное определение работы в Docker контейнере"""
    
    # Способ 1: Проверка наличия .dockerenv файла
    if os.path.exists('/.dockerenv'):
        print("Docker detected: /.dockerenv exists")
        return True
    
    # Способ 2: Проверка cgroup (наиболее надежный для Linux)
    try:
        with open('/proc/1/cgroup', 'r') as f:
            cgroup_content = f.read()
            if any(x in cgroup_content for x in ['docker', 'kubepods', 'lxc']):
                print("Docker detected: cgroup contains docker/kubepods/lxc")
                return True
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error reading cgroup: {e}")
    
    # Способ 3: Проверка hostname (для container-id)
    try:
        hostname = socket.gethostname()
        # Docker container IDs обычно 12 или 64 символа hex
        if (len(hostname) == 12 and all(c in '0123456789abcdef' for c in hostname)) or \
           (len(hostname) == 64 and all(c in '0123456789abcdef' for c in hostname)):
            print(f"Docker detected: hostname {hostname} looks like container ID")
            return True
    except Exception as e:
        print(f"Error checking hostname: {e}")
    
    # Способ 4: Проверка наличия Docker-specific переменных окружения
    docker_env_vars = ['DOCKER_ENV', 'container', 'DOCKER_CONTAINER']
    for var in docker_env_vars:
        if os.environ.get(var):
            print(f"Docker detected: {var} environment variable exists")
            return True
    
    # Способ 5: Проверка наличия /run/secrets (Docker secrets)
    if os.path.exists('/run/secrets'):
        print("Docker detected: /run/secrets exists")
        return True
    
    # Способ 6: Проверка наличия .dockerinit (старый способ)
    if os.path.exists('/.dockerinit'):
        print("Docker detected: /.dockerinit exists")
        return True
    
    # Способ 7: Проверка специфичных для Docker mount точек
    try:
        with open('/proc/mounts', 'r') as f:
            mounts = f.read()
            if 'docker' in mounts or 'overlay' in mounts:
                print("Docker detected: overlay or docker in mounts")
                return True
    except:
        pass
    
    print("Running LOCALLY (no Docker indicators found)")
    return False


def load_env(env_path=Path(__file__).resolve().parent.parent / 'backend/.env'):
    """Загружает .env файл, игнорируя форматирование."""
    try:
        print(f"Loading env from: {env_path}")
        with open(env_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip()
                    if key:
                        os.environ[key] = value
                        print(f"Set env: {key}={value[:20]}...")  # скрываем пароль
    except FileNotFoundError:
        print(f"Файл {env_path} не найден")
    except Exception as e:
        print(f"Ошибка при загрузке .env: {e}")


def creds():
    # Сначала проверяем существующие переменные окружения
    print("Current environment variables:")
    print(f"DATABASE_HOST: {os.environ.get('DATABASE_HOST', 'not set')}")
    print(f"DATABASE_PORT: {os.environ.get('DATABASE_PORT', 'not set')}")
    
    in_docker = is_running_in_docker()
    
    if in_docker:
        # В Docker загружаем .env из родительской директории
        env_path = Path(__file__).resolve().parent.parent /'backend/.env' 
        load_env(env_path)
        print("Running in DOCKER")
    else:
        # Локально загружаем .env из backend папки
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_env(env_path)
        print("Running LOCALLY")
    
    # Получаем значения из переменных окружения
    host_name = os.environ.get('DATABASE_NAME', 'coursapp')
    user_name = os.environ.get('DATABASE_USERNAME', 'coursapp')
    db_password = os.environ.get('DATABASE_ROOT_PASSWORD', 'password')
    db_port = os.environ.get('DATABASE_PORT', '3306')
    
    # ВАЖНО: В Docker используем имя сервиса, а не localhost
    if in_docker:
        db_host = os.environ.get('DATABASE_HOST', 'db')  # по умолчанию 'db'
    else:
        db_host = os.environ.get('DATABASE_HOST', 'localhost')
    
    secret_key = os.environ.get('SECRET_KEY', 'default-secret-key-change-me')
    
    print(f"Final config - DB: {host_name}, User: {user_name}, Port: {db_port}, Host: {db_host}, Docker: {in_docker}")
    
    return host_name, user_name, db_password, db_port, db_host, secret_key