from Crypto.Cipher import AES
import binascii
from db import hash_pw



def encrypt_AES_GCM(msg , secretKey_half):
    aesCipher = AES.new(secretKey_half, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(encrypted_msg , secretKey_half):
    (ciphertext, nonce, authTag) = encrypted_msg
    aesCipher = AES.new(secretKey_half, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext


#print("Encryption key:", binascii.hexlify(secretKey_half))

#msg = 'Message for AES-256-GCM + Scrypt encryption'
#encryptedMsg = encrypt_AES_GCM(msg.encode("utf-8"))
#print("encryptedMsg", {'ciphertext': binascii.hexlify(encryptedMsg[0])  })
 #   'aesIV': binascii.hexlify(encryptedMsg[1]),
 #   'authTag': binascii.hexlify(encryptedMsg[2])
#})

#decryptedMsg = decrypt_AES_GCM(encryptedMsg)
#print("decryptedMsg", decryptedMsg)