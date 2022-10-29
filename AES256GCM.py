from Crypto.Cipher import AES


def encrypt_AES_GCM(msg , secretKey_half):
    aesCipher = AES.new(secretKey_half, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(encrypted_msg , secretKey_half):
    (ciphertext, nonce, authTag) = encrypted_msg
    aesCipher = AES.new(secretKey_half, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext