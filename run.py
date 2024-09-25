# run.py
from app.routes import app  # Ensure you import the `app` instance from `app/routes.py`

if __name__ == "__main__":
    app.run(debug=True)
