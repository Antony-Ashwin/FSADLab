import jwt
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# i am generating a private key here 
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# enocde method throws exception when i directly try to send the private key, thats why i am serializing it
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

#similarly i am generating for a public key which is needed while decoding
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(private_key_pem.decode())
print(public_key_pem.decode())

alg = "RS256"
a_payload = {
    "name": "ashwin",
    "id": "sl93002",
    "exp": int(time.time()) + 60 * 60   #using the same payload i used for HS256
}


token = jwt.encode(payload=a_payload, key=private_key_pem, algorithm=alg)
print("----------------------------------")
print("Algorithm : ", alg)
print("Token : ", token)


decoded_token = jwt.decode(token, public_key_pem, algorithms=[alg])
print("Decoded token : ", decoded_token)
print("----------------------------------")
