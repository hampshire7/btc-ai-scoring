import multiprocessing as mp
from ecdsa import SigningKey, SECP256k1

TARGET_PUBKEY_HEX = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
START_HEX = "4000000000000000000000000000000000"
END_HEX   = "7fffffffffffffffffffffffffffffffff"

def get_compressed_pubkey(k: int) -> str:
    sk = SigningKey.from_secret_exponent(k, curve=SECP256k1)
    vk = sk.verifying_key
    x, y = vk.pubkey.point.x(), vk.pubkey.point.y()
    prefix = '02' if y % 2 == 0 else '03'
    return prefix + format(x, '064x')

def brute_worker(start: int, end: int, target: str, flag):
    for k in range(start, end):
        if flag.is_set(): break
        pubkey = get_compressed_pubkey(k)
        if pubkey == target:
            print(f"\n🎯 MATCH FOUND!\nPrivate key: {hex(k)}")
            flag.set()
            break

def launch_scan(workers: int = 8):
    start = int(START_HEX, 16)
    end   = int(END_HEX, 16)
    chunk = (end - start) // workers
    flag = mp.Event()
    processes = []
    for i in range(workers):
        s = start + i * chunk
        e = start + (i + 1) * chunk if i < workers - 1 else end
        p = mp.Process(target=brute_worker, args=(s, e, TARGET_PUBKEY_HEX, flag))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
