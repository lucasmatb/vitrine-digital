from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import base64
from django.conf import settings
import uuid

crypto_key = settings.CRYPTO_KEY.encode('utf-8')

def encriptarAESGCM(string):
    nonce = get_random_bytes(12)
    
    cipher = AES.new(crypto_key, AES.MODE_GCM, nonce=nonce)

    texto_bytes = string.encode('utf-8')
    texto_encriptado, tag = cipher.encrypt_and_digest(texto_bytes)

    return base64.b64encode(nonce + texto_encriptado + tag).decode('utf-8')

def descriptarAESGCM(textoCriptografado):
    dados = base64.b64decode(textoCriptografado)
    
    nonce = dados[:12]
    tag = dados[-16:]
    texto_encriptado = dados[12:-16]

    cipher = AES.new(crypto_key, AES.MODE_GCM, nonce=nonce)
    
    texto_decriptado = cipher.decrypt_and_verify(texto_encriptado, tag)

    return texto_decriptado.decode('utf-8')

def retornaCaminhoImagemAleatorio(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename