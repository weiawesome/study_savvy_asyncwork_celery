import base64
import uuid
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
def strid2byte(id):
    str_id=str(id)
    uuid_id=uuid.UUID(str_id)
    return uuid_id.bytes
def byte2strid(id):
    uuid_id=uuid.UUID(bytes=id)
    return str(uuid_id)

def base642byte(data):
    original_bytes_data = base64.b64decode(data)
    return original_bytes_data

def RSA_decrypt(encrypted_aes_key):
    with open('/Security/private_key.pem', 'rb') as f:
        pem_private = f.read()
    private_key = serialization.load_pem_private_key(
        pem_private,
        password=None,
        backend=default_backend()
    )
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return aes_key

def AES_decrypt(aes_key,encrypted_data):
    cipher_dec = AES.new(aes_key, AES.MODE_ECB)
    data_pad_dec = cipher_dec.decrypt(encrypted_data)
    data = unpad(data_pad_dec, AES.block_size)
    result = data.decode()
    return result

def decrypt(encrypted_data,encrypted_key):
    result=""
    try:
        origin_key=base642byte(encrypted_key)
        key=RSA_decrypt(origin_key)
        origin_key=base642byte(key)
        origin_data=base642byte(encrypted_data)
        result=AES_decrypt(origin_key,origin_data)
    finally:
        return result