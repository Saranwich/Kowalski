from app.core.config import LINE_CHANNEL_SECRET
import hmac, hashlib, base64

def is_valid_line_signature (raw_body: bytes, signature : str ) -> bool:
    if signature is None : return False
    expected:str = base64.b64encode(
        hmac.new(
            LINE_CHANNEL_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).digest()
        ).decode()

    return hmac.compare_digest(expected, signature)