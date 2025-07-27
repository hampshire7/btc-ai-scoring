# Puzzle #135 Brute-Force Scanner

This Streamlit app scans a defined private key range using 4 parallel workers to find a match for a target compressed public key.

## Features
- Multiprocessing with checkpoint logging
- ECC pubkey derivation via `coincurve`
- Streamlit UI with range input and slice preview

## Usage
1. Clone repo and install dependencies: