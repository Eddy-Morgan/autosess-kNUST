from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(225),default=None)
    start_date = db.Column(db.DateTime(),default=None)
    end_date = db.Column(db.DateTime(),default=None)