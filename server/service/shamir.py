import logging
from Crypto.Protocol.SecretSharing import Shamir
from phe import paillier
import time

# ロガーの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Paillier鍵ペアを生成
public_key, private_key = paillier.generate_paillier_keypair()

def split_private_key_for_shamir(key: str) -> list[bytes]:

    if len(key) != 64:
        raise ValueError("The key must be a 64-character hex string.")

    key_bytes1 = bytes.fromhex(key[:32])
    key_bytes2 = bytes.fromhex(key[32:])
    return [key_bytes1, key_bytes2]


def generate_shamir_keys(key: str) -> list[tuple[int, int, str]]:
    """
    シャミアの秘密分散法を使って秘密鍵を分割する
    """

    # 秘密鍵を分割
    splited_key = split_private_key_for_shamir(key)
    # シャミアの秘密分散法を使って秘密鍵を分割
    shamirs = [Shamir.split(3, 5, k, None) for k in splited_key]

    # splited_key の index と シャミアの index + 分割された秘密鍵
    r: list[tuple[int, int, str]] = []

    # 保管用の配列を作成
    for i, shamir in enumerate(shamirs):
        [r.append((i, idx, s.hex())) for idx, s in shamir]

    return r


def encrypt_shares(shares: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """
    PHEでシェアを暗号化する
    """
    encrypted_shares = []
    for i, idx, s in shares:
        encrypted_s = public_key.encrypt(int(s, 16))
        encrypted_shares.append((i, idx, str(encrypted_s.ciphertext())))  # 文字列として保存
        logger.debug(f"Encrypted share: (i={i}, idx={idx}, s={encrypted_s.ciphertext()})")
    return encrypted_shares


def decrypt_shares(encrypted_shares: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    """
    PHEで暗号化されたシェアを復号化する
    """
    decrypted_shares = []
    for i, idx, s in encrypted_shares:
        logger.debug(f"Decrypting share: (i={i}, idx={idx}, s={s})")
        decrypted_s = private_key.decrypt(paillier.EncryptedNumber(public_key, int(s)))
        decrypted_shares.append((i, idx, format(decrypted_s, 'x')))
        logger.debug(f"Decrypted share: (i={i}, idx={idx}, s={format(decrypted_s, 'x')})")
    return decrypted_shares


def recover_shamir_keys(shares: list[tuple[int, int, str]]) -> str:
    """
    シェアから復元する
    """
    s1 = []
    s2 = []

    for i, idx, s in shares:
        logger.debug(f"Recovering share: {i}, {idx}, {s}")
        if not all(c in '0123456789abcdefABCDEF' for c in s):
            raise ValueError(f"Invalid hex value: {s}")
        if i == 0:
            s1.append((idx, bytes.fromhex(s)))
            continue

        if i == 1:
            s2.append((idx, bytes.fromhex(s)))
            continue

        raise Exception(f"Invalid index: {i}")

    k1 = Shamir.combine(s1, None)
    k2 = Shamir.combine(s2, None)

    return f"{k1.hex().upper()}{k2.hex().upper()}"


def recover_shamir_keys_phe(encrypted_shares: list[tuple[int, int, str]]) -> str:
    """
    PHEで暗号化されたシェアから復元する
    """
    shares = decrypt_shares(encrypted_shares)
    logger.debug(f"Decrypted shares: {shares}")
    return recover_shamir_keys(shares)