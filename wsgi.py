from blog.app import create_app, db
from werkzeug.security import generate_password_hash

app = create_app()


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'peter'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True, email='admin@mail.ru', password=generate_password_hash('space'))
    peter = User(username="peter", is_staff=False, email='user1@mail.ru', password=generate_password_hash('test123'))
    db.session.add(admin)
    db.session.add(peter)
    db.session.commit()
    print("done! created users:", admin, peter)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
