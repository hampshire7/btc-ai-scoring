import streamlit as st
import multiprocessing
from coincurve import PrivateKey
import os

# Constants
TARGET_PUBKEY = "02cbb434aa7ae1700dcd15b20b17464817ec11715050e0fa192ffe9c29a673059f"
CHECKPOINT_INTERVAL = 100_000

# ECC Derivation
def derive_compressed_pubkey(private_int):
    priv_bytes = private_int.to_bytes(32, byteorder='big')
    pubkey = PrivateKey(priv_bytes).public_key.format(compressed=True)
    return pubkey.hex()

# Worker Task
def worker_task(worker_id, start_int, end_int, target_pubkey):
    checkpoint_file = f"checkpoint_worker_{worker_id}.txt"
    scanned = 0
    current = start_int

    while current <= end_int:
        derived = derive_compressed_pubkey(current)
        if derived == target_pubkey:
            with open(f"FOUND_{worker_id}.txt", "w") as f:
                f.write(f"FOUND MATCH: {hex(current)}")
            break

        scanned += 1
        current += 1

        if scanned % CHECKPOINT_INTERVAL == 0:
            with open(checkpoint_file, "w") as f:
                f.write(f"Last scanned: {hex(current)}\n")

# Range Splitter
def split_range(start_hex, end_hex, num_workers):
    start_int = int(start_hex, 16)
    end_int = int(end_hex, 16)
    total = end_int - start_int + 1
    chunk = total // num_workers
    ranges = []

    for i in range(num_workers):
        chunk_start = start_int + i * chunk
        chunk_end = chunk_start + chunk - 1
        if i == num_workers - 1:
            chunk_end = end_int
        ranges.append((chunk_start, chunk_end))

    return ranges

# Streamlit UI
st.title("🔐 Puzzle #135 Brute-Force Scanner")

start_hex = st.text_input("Start Hex", "4000000000000000000000000000000000")
end_hex = st.text_input("End Hex", "7fffffffffffffffffffffffffffffffff")
num_workers = st.slider("Number of Workers", 1, 4, 4)

if st.button("🚀 Launch Scan"):
    st.write("Splitting range and launching workers...")
    ranges = split_range(start_hex, end_hex, num_workers)

    for i, (start, end) in enumerate(ranges):
        st.write(f"Worker {i}: {hex(start)} → {hex(end)}")

    for i, (start, end) in enumerate(ranges):
        p = multiprocessing.Process(target=worker_task, args=(i, start, end, TARGET_PUBKEY))
        p.start()