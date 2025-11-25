from app import create_app
from flask import session

app = create_app()

if __name__ == "__main__":
    app.secret_key = "supersecretkey"
    app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.run(debug=True)