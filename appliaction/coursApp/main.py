from app import create_app, db
import click
from app.models import Employee
from getpass import getpass

app = create_app()

@app.cli.command("create-admin")
def create_admin():
    """Создание первого администратора"""

    if Employee.query.filter_by(role="admin").first():
        click.echo("❌ Администратор уже существует")
        return

    username = input("Логин администратора: ")
    password = getpass("Пароль: ")
    password2 = getpass("Повторите пароль: ")

    if password != password2:
        click.echo("❌ Пароли не совпадают")
        return

    admin = Employee(username=username, role="admin")
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()

    click.echo("✅ Администратор успешно создан")
