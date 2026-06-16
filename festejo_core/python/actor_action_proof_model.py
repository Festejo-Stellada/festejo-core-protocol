import uuid
from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime

class Actor(BaseModel):
    id: str
    type: str

class Action(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    payload: Dict[str, Any]
    idempotency_key: str = Field(..., description="Unique key to prevent replay attacks")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Proof(BaseModel):
    type: str
    data: Dict[str, Any]
    signature: str
    idempotency_hash: str = Field(..., description="Globally unique hash for proof uniqueness")

class StellarRecord(BaseModel):
    transaction_id: str
    ledger_sequence: int
    payload_hash: str
    confirmed: bool = True

class ProtocolEnvelope(BaseModel):
    actor: Actor
    action: Action
    proof: Proof
    stellar_record: StellarRecord
