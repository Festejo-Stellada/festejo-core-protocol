import uuid
from typing import Callable, Any
from festejo_core.python.actor_action_proof_model import Actor, Action, Proof, ProtocolEnvelope, StellarRecord
from festejo_core.python.bindings import get_proof_hash, is_replay, log_audit
from festejo_stellar.stellar_client import StellarClient

# Failure Model
class PipelineError(Exception): pass
class ValidationFailed(PipelineError): pass
class ProofRejected(PipelineError): pass
class StellarSubmissionFailed(PipelineError): pass
class PersistenceError(PipelineError): pass

class PipelineExecutor:
    def __init__(self):
        self.stellar = StellarClient()

    def execute(self, 
                actor_factory: Callable[[], Actor],
                action_factory: Callable[[], Action],
                proof_factory: Callable[[Action, str], Proof],
                persistence_callback: Callable[[ProtocolEnvelope], None]) -> ProtocolEnvelope:
        
        execution_id = str(uuid.uuid4())
        log_audit(f"INIT:STARTED:{execution_id}")
        
        try:
            # 1. Pipeline Execution Flow
            actor = actor_factory()
            action = action_factory()
            log_audit(f"INIT:ACTOR_ACTION_CREATED:{execution_id}")
            
            # 2. Rust-powered Proof Uniqueness Enforcement
            proof_hash = get_proof_hash(actor.id, action.idempotency_key, action.timestamp.isoformat())
            if is_replay(proof_hash):
                raise ProofRejected("Duplicate proof hash detected")
            
            # 3. Proof Creation & Validation
            proof = proof_factory(action, proof_hash)
            log_audit(f"PROOF:CREATED_AND_VALIDATED:{execution_id}:{proof_hash}")
            
            # 4. Stellar Interaction
            try:
                stellar_record = self.stellar.record_proof(proof, action)
                log_audit(f"STELLAR:SUBMISSION_SUCCESS:{execution_id}:{stellar_record.transaction_id}")
            except Exception as e:
                log_audit(f"STELLAR:FAILED:{execution_id}:{str(e)}")
                raise StellarSubmissionFailed(str(e))
            
            # 5. Construct Envelope
            envelope = ProtocolEnvelope(
                actor=actor,
                action=action,
                proof=proof,
                stellar_record=stellar_record
            )
            
            # 6. Persistence
            try:
                persistence_callback(envelope)
                log_audit(f"PERSISTENCE:SUCCESS:{execution_id}")
            except Exception as e:
                log_audit(f"PERSISTENCE:FAILED:{execution_id}:{str(e)}")
                raise PersistenceError(str(e))
                
            return envelope
            
        except PipelineError as e:
            log_audit(f"PIPELINE:HALTED:{execution_id}:{str(e)}")
            raise
        except Exception as e:
            log_audit(f"PIPELINE:CRITICAL_FAILURE:{execution_id}:{str(e)}")
            raise PipelineError(str(e))
