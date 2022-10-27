from active_alchemy import ActiveAlchemy
import hashlib

db = ActiveAlchemy("sqlite:///passwords.db")

def hash_main_pw(main_pw, hash_type):
    if hash_type == "sha256":
	    # SHA-256 hash of the password
        hash256 = hashlib.sha256(main_pw.encode('utf-8')).hexdigest()
        return hash256
    elif hash_type == "sha512":
	    # SHA-512 hash of the password
        hash512 = hashlib.sha512(main_pw.encode('utf-8')).hexdigest()
        return hash512


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

