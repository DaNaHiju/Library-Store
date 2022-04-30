from database import init_db
from main.models import *
from flask import Flask
from admin.routes import admin as admin_blueprint
from main.routes import main as main_blueprint

# This is the main app
app = Flask(__name__)

app.config["SECRET_KEY"] = "shihhttierat874egyfyasgdrasdjfnsdafasdfbsjf"

init_db()


app.register_blueprint(admin_blueprint, url_prefix='/admin')


app.register_blueprint(main_blueprint, url_prefix='/')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
