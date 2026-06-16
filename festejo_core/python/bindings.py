from festejo_core_rust import (
    generate_proof_hash,
    check_replay,
    emit_audit_event
)

def get_proof_hash(actor_id: str, idempotency_key: str, timestamp: str) -> str:
    return generate_proof_hash(actor_id, idempotency_key, timestamp)

def is_replay(proof_hash: str) -> bool:
    return check_replay(proof_hash)

def log_audit(event_data: str):
    emit_audit_event(event_data)
