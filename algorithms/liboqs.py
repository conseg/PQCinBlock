from time import perf_counter
import random
import string
import oqs

ALGORITHMS = {
    'mldsa': {
        2: 'ML-DSA-44',
        3: 'ML-DSA-65',
        5: 'ML-DSA-87'
    },
    'dilithium': {
        2: 'Dilithium2',
        3: 'Dilithium3',
        5: 'Dilithium5'
    },
    'sphincs-sha-s': {
        1: 'SPHINCS+-SHA2-128s-simple',
        3: 'SPHINCS+-SHA2-192s-simple',
        5: 'SPHINCS+-SHA2-256s-simple'
    },
    'sphincs-sha-f': {
        1: 'SPHINCS+-SHA2-128f-simple',
        3: 'SPHINCS+-SHA2-192f-simple',
        5: 'SPHINCS+-SHA2-256f-simple'
    },
    'sphincs-shake-s': {
        1: 'SPHINCS+-SHAKE-128s-simple',
        3: 'SPHINCS+-SHAKE-192s-simple',
        5: 'SPHINCS+-SHAKE-256s-simple'
    },
    'sphincs-shake-f': {
        1: 'SPHINCS+-SHAKE-128f-simple',
        3: 'SPHINCS+-SHAKE-192f-simple',
        5: 'SPHINCS+-SHAKE-256f-simple'
    },
    'falcon': {
        1: 'Falcon-512',
        5: 'Falcon-1024'
    },
    'falcon-padded': {
        1: 'Falcon-padded-512',
        5: 'Falcon-padded-1024'
    },
    'mayo': {
        1: 'MAYO-2',
        3: 'MAYO-3',
        5: 'MAYO-5'
    },
    'cross-rsdp-small': {
        1: 'cross-rsdp-128-small',
        3: 'cross-rsdp-192-small',
        5: 'cross-rsdp-256-small'
    },
    'cross-rsdpg-small': {
        1: 'cross-rsdpg-128-small',
        3: 'cross-rsdpg-192-small',
        5: 'cross-rsdpg-256-small'
    },
    'cross-rsdp-balanced': {
        1: 'cross-rsdp-128-balanced',
        3: 'cross-rsdp-192-balanced',
        5: 'cross-rsdp-256-balanced'
    },
    'cross-rsdpg-balanced': {
        1: 'cross-rsdpg-128-balanced',
        3: 'cross-rsdpg-192-balanced',
        5: 'cross-rsdpg-256-balanced'
    },
    'cross-rsdp-fast': {
        1: 'cross-rsdp-128-fast',
        3: 'cross-rsdp-192-fast',
        5: 'cross-rsdp-256-fast'
    },
    'cross-rsdpg-fast': {
        1: 'cross-rsdpg-128-fast',
        3: 'cross-rsdpg-192-fast',
        5: 'cross-rsdpg-256-fast'
    }
}

def time_evaluation(variant: str, runs: int):

    results = []

    # message = "This is the message to sign".encode()

    # Runs
    for i in range(runs):
        
        message = ''.join(random.choices(string.ascii_letters + string.digits, k=60)).encode("utf-8")

        with oqs.Signature(variant) as signer, oqs.Signature(variant) as verifier:

            # Signer generates its keypair
            start_keypair = perf_counter()
            signer_public_key = signer.generate_keypair()
            end_keypair = perf_counter()

            keypair_time = (end_keypair - start_keypair) * 1000

            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the signer can later be re-instantiated with the key pair:
            # secret_key = signer.export_secret_key()

            # Store key pair, wait... (session resumption):
            # signer = oqs.Signature(sigalg, secret_key)

            # Signer signs the message
            start_sign = perf_counter()
            signature = signer.sign(message)
            end_sign = perf_counter()
            
            sigSize = len(signature)
            # print(f"Signature size: {sigSize} bytes")
            private_key_size = signer.details['length_secret_key']
            public_key_size = len(signer_public_key)
            # print(f"Private key size: {private_key_size} bytes")
            # print(f"Public key size: {public_key_size} bytes")

            sign_time = (end_sign - start_sign) * 1000

            # Verifier verifies the signature
            start_verify = perf_counter()
            is_valid = verifier.verify(message, signature, signer_public_key)
            end_verify = perf_counter()

            verify_time = (end_verify - start_verify) * 1000

            if not is_valid:
                print(f"WARNING: Verification failed at iteration {i}!")

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
