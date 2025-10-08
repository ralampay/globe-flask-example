from app import create_app, db

app = create_app(env="development")
app.app_context().push()

from tests.factories import UserFactory

def seed_users(n=10):

    with app.app_context():
        print(f"Creating {n} users...")

        # Temporarily override the persistence mode
        original_persistence = UserFactory._meta.sqlalchemy_session_persistence
        UserFactory._meta.sqlalchemy_session_persistence = "commit"
        UserFactory._meta.sqlalchemy_session = db.session

        for _ in range(n):
            UserFactory()

        UserFactory._meta.sqlalchemy_session_persistence = original_persistence
        UserFactory._meta.sqlalchemy_session = db.session

        print("Done.")

if __name__ == "__main__":
    seed_users(10)