import streamlit as st
from ecdsa import SigningKey, SECP256k1

# Target public key to match
TARGET_PUBKEY = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"

# Define hex range
START_HEX = "4000000000000000000000000000000000"
END_HEX   = "7fffffffffffffffffffffffffffffffff"

def get_compressed_pubkey(k: int) -> str:
    sk = SigningKey.from_secret_exponent(k, curve=SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    prefix = '02' if y % 2 == 0 else '03'
    return prefix + format(x, '064x')

def run_brute_search(start, end, target):
    for k in range(start, end):
        pubkey = get_compressed_pubkey(k)
        if pubkey == target:
            return hex(k)
    return None

def main():
    st.title("🔐 Stateless Bitcoin Key Hunter")
    st.caption("Puzzle #135 • Match compressed public key within hex range")

    st.markdown(f"**Target Compressed Public Key:** `{TARGET_PUBKEY}`")
    
    start_hex = st.text_input("Start Hex", START_HEX)
    end_hex = st.text_input("End Hex", END_HEX)
    run_button = st.button("🚀 Start Scan")

    if run_button:
        start_int = int(start_hex, 16)
        end_int = int(end_hex, 16)
        with st.spinner("Scanning..."):
            result = run_brute_search(start_int, end_int, TARGET_PUBKEY)
            if result:
                st.success(f"🎯 MATCH FOUND! Private key: `{result}`")
            else:
                st.warning("No match found in the selected range.")

if __name__ == "__main__":
    main()