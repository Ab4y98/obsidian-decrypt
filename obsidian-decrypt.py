import base64
import sys
import re
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512

def decrypt(base64_ciphertext, password, salt_len=16, iv_len=16, iterations=210000):
    raw = base64.b64decode(base64_ciphertext)
    iv = raw[:iv_len]
    salt = raw[iv_len:iv_len + salt_len]
    ciphertext = raw[iv_len + salt_len:]

    key = PBKDF2(password, salt, dkLen=32, count=iterations, hmac_hash_module=SHA512)

    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        plaintext = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
        return plaintext.decode()
    except Exception:
        return None

# === MAIN ===

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} '<🔐βBase64🔐>' wordlist.txt")
    sys.exit(1)

raw_input = sys.argv[1]
cleaned = re.sub(r"[🔐αβ%%\s]", "", raw_input)  # Strip emoji, version markers, whitespace

wordlist = sys.argv[2]

with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        password = line.strip()
        result = decrypt(cleaned, password)
        if result:
            print(f"[+] Found: {password}")
            print(f"Decrypted: {result}")
            break
    else:
        print("[-] No match found.")
