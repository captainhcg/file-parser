from app import db

class Specification(db.Model):
    __tablename__ = 'specification'
    specification_id = db.Column('id', db.Integer, primary_key=True)
    specification_name = db.Column('name', db.String(128), unique=True)


def create_all():
    db.drop_all()
    db.create_all()
