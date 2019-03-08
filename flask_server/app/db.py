import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import current_app

def get_db():
    return firestore.client()

def init_db():
    cred = credentials.Certificate(current_app.config["DATABASE"])
    firebase_admin.initialize_app(cred)
    print("DATABASE INITIALIZED")