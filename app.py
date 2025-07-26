# app.py
import streamlit as st
import random
from hashlib import sha256, new as hashlib_new
from ecdsa import SECP256k1

# Constants
G = SECP256k1.generator
TARGET_HASH160 = "3b6f58a75a54bfd85d1bc6c51180fdc732992326"
PUBKEY_HEX = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"

# Functions
def hash160(pubkey_bytes):
    sha = sha256(pubkey_bytes).digest()
    ripemd = hashlib_new('ripemd160', sha).digest()
    return ripemd

def derive_pubkey(k):
    point = k * G
    x, y = point.x(), point.y()
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    return prefix + x.to_bytes(32, 'big')

def entropy_score(bytestr):
    return len(set(bytestr))

# App UI
st.title("🔑 AI Scoring for BTC Puzzle #135")
st.caption(f"🎯 Target Hash160: `{TARGET_HASH160}`")
st.caption(f"🔐 Known Public Key: `{PUBKEY_HEX}`")

start_hex = st.text_input("Start Hex", "4000000000000000000000000000000000")
end_hex = st.text_input("End Hex", "7fffffffffffffffffffffffffffffffff")
samples = st.slider("Number of Samples", 1000, 10000, 5000)

if st.button("Run AI Sweep"):
    START = int(start_hex, 16)
    END = int(end_hex, 16)

    random.seed(42)  # Optional: makes sweep reproducible
    results = []
    with st.spinner("Running entropy sweep..."):
        for _ in range(samples):
            k = random.randint(START, END)
            pubkey = derive_pubkey(k)
            h160 = hash160(pubkey)
            score = entropy_score(h160)

            k_hex = hex(k)
            pk_hex = pubkey.hex()
            h160_hex = h160.hex()

            is_match = h160_hex == TARGET_HASH160.lower()
            is_pubkey_match = pk_hex == PUBKEY_HEX.lower()

            marker = "🟢" if is_match or is_pubkey_match else "🔸"
            results.append((score, marker, k_hex, pk_hex, h160_hex))

    results.sort(reverse=True)
    for score, marker, k_hex, pk_hex, h160_hex in results[:100]:
        st.write(f"{marker} **{k_hex}** | Score: {score} | Pubkey: `{pk_hex}` | Hash160: `{h160_hex}`")
