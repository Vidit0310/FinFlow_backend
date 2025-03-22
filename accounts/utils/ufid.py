import hashlib
import random
import string

def generate_unique_code(param: str, length=10) -> str:
    """Generates a unique 10-digit alphanumeric code using a string parameter."""
    
    # Hash the parameter to create a unique identifier
    hash_object = hashlib.sha256(param.encode())
    hex_digest = hash_object.hexdigest()  # 64 characters hex string

    # Take a portion of the hash and add random alphanumeric characters
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - 6))

    # Generate the unique code (first 6 hash chars + 4 random chars)
    unique_code = (hex_digest[:6] + random_chars).upper()

    return unique_code[:length]


