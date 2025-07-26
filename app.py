# app.py
import streamlit as st
import random
from hashlib import sha256, new as hashlib_new
from ecdsa import SECP256k1

G = SECP256k1.generator

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

st.title("🔑 AI Scoring for BTC Puzzle #72")
start_hex = st.text_input("Start Hex", "4000000000000000000000000000000000")
end_hex = st.text_input("End Hex", "7fffffffffffffffffffffffffffffffff")
samples = st.slider("Number of Samples", 1000, 10000, 5000)

if st.button("Run AI Sweep"):
    START = int(start_hex, 16)
    END = int(end_hex, 16)

    results = []
    with st.spinner("Running entropy sweep..."):
        for _ in range(samples):
            k = random.randint(START, END)
            pubkey = derive_pubkey(k)
            h160 = hash160(pubkey)
            score = entropy_score(h160)
            results.append((score, hex(k), pubkey.hex(), h160.hex()))

    results.sort(reverse=True)
    for score, k_hex, pk_hex, h160_hex in results[:100]:
        st.write(f"🔸 **{k_hex}** | Score: {score} | Pubkey: `{pk_hex}` | Hash160: `{h160_hex}`")
