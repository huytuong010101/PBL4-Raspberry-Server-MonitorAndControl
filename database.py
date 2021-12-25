from peewee import MySQLDatabase
from dotenv import load_dotenv
import os

load_dotenv()
database = MySQLDatabase(
    os.environ["DATABASE_NAME"],
    host=os.environ["DATABASE_HOST"],
    port=int(os.environ["DATABASE_PORT"]),
    user=os.environ["DATABASE_USERNAME"],
    password=os.environ["DATABASE_PASSWORD"]
)

if __name__ == "__main__":
    from models.User import User
    from models.LoginLog import LoginLog
    from models.ActivityTracking import ActivityTracking
    from models.HardwareTracking import HardwareTracking
    models = [User, LoginLog, ActivityTracking, HardwareTracking]
    database.create_tables(models)
    print(">> Created all table: ", *models, sep=" ")
    u = User.create(
        username="admin",
        fullname="Nguyen Huy Tuong",
        password="$2b$12$UJUog2XKQVSWOlPjj7ezTOboFZTTnN3HkNahIooIqGqp.JFZt/Vwa",
        is_admin=True
    )
    print(">> Created default user", u)
