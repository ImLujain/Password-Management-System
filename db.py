from active_alchemy import ActiveAlchemy
import hashlib
from AES256GCM import encrypt_AES_GCM , decrypt_AES_GCM

db = ActiveAlchemy("sqlite:///passwords.db")

def hash_pw(pw, hash_type):
    # 256 as a key to encrypt passowrds
    if hash_type == "sha256":
        hash256 = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        return hash256

    elif hash_type == "sha512":
	    # SHA-512 hash for the Main Password
        hash512 = hashlib.sha512(pw.encode('utf-8')).hexdigest()
        return hash512



class MainUser(db.Model):
    __tablename__ = "MainUser"

    main_username = db.Column(db.String(25))
    main_password = db.Column(db.String(25))


class ServicesPasswords(db.Model):
    __tablename__ = "ServicesPasswords"

    service = db.Column(db.String(25))
    service_username = db.Column(db.String(25))
    service_password = db.Column(db.String(300))
    nonce = db.Column(db.String(300))
    authTag = db.Column(db.String(300))

    


db.create_all()

