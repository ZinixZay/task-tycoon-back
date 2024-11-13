import string
import secrets

def gen_random_string(lowercase: bool = True, uppercase: bool = True, digits: bool = True, length: int = 20) -> str:
    if not lowercase and not uppercase and not digits:
        return ''
    pool = ''
    pool += string.ascii_lowercase if lowercase else ''
    pool += string.ascii_uppercase if uppercase else ''
    pool += string.digits if digits else ''
    return ''.join(secrets.choice(pool) for _ in range(length))
