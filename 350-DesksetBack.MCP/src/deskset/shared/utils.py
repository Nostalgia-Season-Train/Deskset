# --- 生成令牌 ---
def generate_token() -> str:
    from datetime import datetime
    current: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    import os
    key: bytes = os.urandom(32)
    msg: bytes = (current).encode()

    import hmac
    import hashlib
    token: str = hmac.new(key, msg, hashlib.sha256).hexdigest()

    return token
