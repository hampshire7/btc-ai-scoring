import streamlit as st
from hashlib import sha256
import ecdsa

# Constants (Puzzle #135 Target)
r = int("00c86bec9faea4892fd98d718bdfc770d0d11c3d6bfd4328f25fe9b06bfadb9650", 16)
s = int("224a322e81c044d341521f65fabdfa86d84673fb55ed7533862e37f7724931fa", 16)
z = int("92886faaf53f90a5c03d6af773a726e75097179306b980e5d28772e612e00fc7", 16)
target_pubkey = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"

# ECDSA Parameters
curve = ecdsa.SECP256k1
n = curve.order

def recover_priv(r, s, z, k):
    return ((s * k - z) * pow(r, -1, n)) % n

def compress_pubkey(priv_int):
    sk = ecdsa.SigningKey.from_secret_exponent(priv_int, curve=curve)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    prefix = b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03'
    return (prefix + x.to_bytes(32, 'big')).hex()

# Streamlit Interface
st.title("🧪 Puzzle #135: k-Recovery Tester")
seed_base = st.text_input("🔑 Seed prefix", value="entropy_seed")
range_start = st.number_input("Start index", value=0)
range_end = st.number_input("End index", value=1000)

if st.button("Start Scanning"):
    with st.spinner("Scanning candidate nonces..."):
        for i in range(range_start, range_end):
            seed = f"{seed_base}_{i}"
            k_candidate = int(sha256(seed.encode()).hexdigest(), 16) % n
            priv = recover_priv(r, s, z, k_candidate)
            pubkey = compress_pubkey(priv)

            st.write(f"🔍 k index: `{i}` — PubKey: `{pubkey}`")
            if pubkey == target_pubkey:
                st.success(f"🎯 FOUND match! Private Key: `{hex(priv)}`")
                break
