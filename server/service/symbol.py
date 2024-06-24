from symbolchain.CryptoTypes import PrivateKey


def generate_new_private_key() -> str:
    """
    秘密鍵を作成します
    """
    return str(PrivateKey.random())
