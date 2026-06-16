use pyo3::prelude::*;
use std::collections::HashSet;
use std::sync::Mutex;
use lazy_static::lazy_static;
use sha2::{Sha256, Digest};

lazy_static! {
    static ref PROCESSED_PROOFS: Mutex<HashSet<String>> = Mutex::new(HashSet::new());
}

#[pyfunction]
fn generate_proof_hash(actor_id: String, idempotency_key: String, timestamp: String) -> PyResult<String> {
    let data = format!("{}{}{}", actor_id, idempotency_key, timestamp);
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let hash = hasher.finalize();
    Ok(format!("{:x}", hash))
}

#[pyfunction]
fn check_replay(proof_hash: String) -> PyResult<bool> {
    let mut proofs = PROCESSED_PROOFS.lock().unwrap();
    if proofs.contains(&proof_hash) {
        Ok(true) // Is a replay
    } else {
        proofs.insert(proof_hash);
        Ok(false) // Not a replay
    }
}

#[pyfunction]
fn emit_audit_event(event_data: String) -> PyResult<()> {
    // In production, this would interface with the audit log storage
    println!("AUDIT EVENT: {}", event_data);
    Ok(())
}

#[pymodule]
fn festejo_core_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_proof_hash, m)?)?;
    m.add_function(wrap_pyfunction!(check_replay, m)?)?;
    m.add_function(wrap_pyfunction!(emit_audit_event, m)?)?;
    Ok(())
}
