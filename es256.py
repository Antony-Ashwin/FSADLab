import jwt
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()


private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)



print(private_key_pem.decode())

print(public_key_pem.decode())


alg = "ES256"
a_payload = {
    "name": "ashwin",
    "id": "sl93002",
    "exp": int(time.time()) + 60 * 60  
}


token = jwt.encode(payload=a_payload, key=private_key_pem, algorithm=alg)
print("----------------------------------")
print("Algorithm : ", alg)
print("Token : ", token)


decoded_token = jwt.decode(token, public_key_pem, algorithms=[alg])
print("Decoded token : ", decoded_token)
print("----------------------------------")
