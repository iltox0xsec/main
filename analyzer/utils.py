import jwt

def decode_jwt(token):
    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})
        return header, payload, True
    except jwt.InvalidTokenError:
        return None, None, False
