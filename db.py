from active_alchemy import ActiveAlchemy


db = ActiveAlchemy("sqlite:///passwords.db")

class User(db.Model):
    __tablename__ = "User"

    username = db.Column(db.String(25))
    password = db.Column(db.String(25))


class Passwords(db.Model):
    __tablename__ = "Passwords"

    website = db.Column(db.String(300))
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))



db.create_all()

