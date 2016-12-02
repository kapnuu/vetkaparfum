import hashlib


def encrypt(password, salt):
    bb = bytes(password + salt, 'utf-8')
    for i in range(1, 600):
        bb = hashlib.sha256(bb).digest()
    return hashlib.sha256(bb).hexdigest()
