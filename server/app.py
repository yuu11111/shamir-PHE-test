from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from server.service.symbol import generate_new_private_key
from server.service.shamir import generate_shamir_keys, recover_shamir_keys, encrypt_shares, decrypt_shares, recover_shamir_keys_phe, generate_shamir_keys_phe
from fastapi.responses import FileResponse
import os
import logging
import time

app = FastAPI()

# ログ設定
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG
logger = logging.getLogger(__name__)

class KeyShares(BaseModel):
    shares: List[Tuple[int, int, str]]


class KeySharesPHE(BaseModel):
    shares: List[Tuple[int, int, str]]


@app.post("/generate_shamir_keys")
def generate_keys():
    key = generate_new_private_key()
    try:
        shamir_keys = generate_shamir_keys(key)
        return {"original_key": key, "shamir_keys": shamir_keys}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/generate_shamir_keys_phe")
def generate_keys_phe():
    key = generate_new_private_key()
    try:
        shamir_keys = generate_shamir_keys_phe(key)
        encrypted_shamir_keys = encrypt_shares(shamir_keys)
        logger.debug(f"Encrypted Shamir keys: {encrypted_shamir_keys}")
        return {"original_key": key, "shamir_keys": encrypted_shamir_keys}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/recover_shamir_keys")
def recover_keys(key_shares: KeyShares):
    try:
        logger.info(f"Received shares: {key_shares.shares}")
        recovered_key = recover_shamir_keys(key_shares.shares)
        return {"recovered_key": recovered_key}
    except Exception as e:
        logger.error(f"Error recovering key: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/recover_shamir_keys_phe")
def recover_keys_phe(key_shares: KeySharesPHE):
    try:
        logger.info(f"Received encrypted shares: {key_shares.shares}")
        for share in key_shares.shares:
            logger.debug(f"Share: {share}")
        decrypted_shares = decrypt_shares(key_shares.shares)
        recovered_key = recover_shamir_keys_phe(decrypted_shares)
        return {"recovered_key": recovered_key}
    except Exception as e:
        logger.error(f"Error recovering key with PHE: {e}")
        raise HTTPException(status_code=400, detail=str(e))


script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static", "index.html")


@app.get("/")
async def read_root():
    return FileResponse(static_dir)