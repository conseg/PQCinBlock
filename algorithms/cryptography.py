from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from time import perf_counter
import random
import string

ALGORITHMS = {
    'ecdsa': {
        1: 'P-256',
        3: 'P-384',
        5: 'P-521'
    },
}

def time_evaluation(variant: str, runs: int):

    curves = {
        "P-256": ec.SECP256R1(),
        "P-384": ec.SECP384R1(),
        "P-521": ec.SECP521R1(),
    }

    if variant not in curves:
        raise ValueError(f"Unknown variant {variant}. Available: {list(curves.keys())}")

    curve = curves[variant]
    results = []

    # Runs
    for i in range(runs):

        message = ''.join(random.choices(string.ascii_letters + string.digits, k=60)).encode("utf-8")

        start_keypair = perf_counter()
        sk = ec.generate_private_key(curve)
        pk = sk.public_key()
        end_keypair = perf_counter()

        keypair_time = (end_keypair - start_keypair) * 1000

        start_sign=perf_counter()
        signature = sk.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        end_sign=perf_counter()
    
        sign_time = (end_sign - start_sign) * 1000

        sigSize = len(signature)
        # print(f"Signature size: {sigSize} bytes")
        private_key_size = sk.key_size // 8
        public_key_size = pk.key_size // 8
        # print(f"Private key size: {private_key_size} bytes")
        # print(f"Public key size: {public_key_size} bytes")
        
        try:
            start_verify=perf_counter()
            pk.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            end_verify=perf_counter()
        except InvalidSignature:
            print(f"WARNING: Verification failed at iteration {i}!")
        
        verify_time = (end_verify - start_verify) * 1000

        results.append({
            "variant": variant,
            "keypair": keypair_time,
            "sign": sign_time,
            "verify": verify_time,
            "sigSize": sigSize,
            "privateKeySize": private_key_size,
            "publicKeySize": public_key_size
        })

    return results