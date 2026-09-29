
import hashlib
def verify_ecp(iin: str, ecp_signature: str, data: str) -> bool:
    if not ecp_signature or len(ecp_signature) < 10:
        return False
    return "VALID" in ecp_signature or iin in ecp_signature

def create_ecp_mock(iin: str, data: str) -> str:
    h = hashlib.sha256((iin + data).encode()).hexdigest()
    return f"ECP_VALID_{iin}_{h[:20]}"
