from flask import Flask

app = Flask(__name__)

# routes.py의 라우트를 불러옵니다
from app import routes