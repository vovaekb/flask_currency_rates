from flask import Flask, _app_ctx_stack, render_template, request, jsonify, Response
from sqlalchemy.orm import scoped_session
from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

from app import views
