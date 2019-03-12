from config import DevConfig
from app import create_app
from flask import Flask

app = create_app(DevConfig)
app.run(host="0.0.0.0", port=5000, debug=True)