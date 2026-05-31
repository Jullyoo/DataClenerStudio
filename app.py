from flask import Flask
from app.routes import main
import os

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

app.register_blueprint(main)

os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("logs", exist_ok=True)

if __name__ == '__main__':

    app.run(
        debug=True
    ) 