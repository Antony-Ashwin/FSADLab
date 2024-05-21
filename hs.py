import jwt
a_key = "ashwinKey"
a_payload = {"data" : "completly differnet data  "}
token = jwt.encode(payload= a_payload, key = a_key, algorithm="HS256")
print()
print("payload : " + str(a_payload))
print("key : " + a_key)
print("token  : " + str(token))
print()
