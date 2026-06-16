# FESTEJO Ecosystem

FESTEJO is a distributed, modular protocol-based ecosystem built on Stellar. It orchestrates high-performance domain services through a deterministic, Rust-backed execution layer, ensuring cryptographic integrity and logical consistency across distributed services.

## Overview

FESTEJO has transitioned from a legacy Django monorepo into a 5-repository distributed system. This architecture separates orchestration (Python) from deterministic execution (Rust), adhering to the **FRSP (FESTEJO Rust Spec Protocol)**.

## Architectural Principles

1.  **Protocol-First:** Every operation follows the immutable pipeline:
    **Actor → Action → Proof → Validation → StellarRecord → Persistence**
2.  **Deterministic Engine:** All cryptographic, hashing, and validation logic is centralized in the `festejo-frsp` crate (Rust), ensuring "same input, same output" across all domain services.
3.  **Service-Oriented:** Domain services (`events`, `identity`, `economy`) are independently deployable and communicate strictly via validated protocol objects.
4.  **Blockchain Segregation:** Stellar blockchain interactions are encapsulated exclusively within `festejo-stellar-sdk`.

## Ecosystem Components

| Component | Responsibility | Language/Tech |
| :--- | :--- | :--- |
| `festejo-frsp` | Infrastructure | Shared Rust crate implementing the FRSP v1.0 standard. |
| `festejo-core-protocol` | Orchestration | Pipeline execution engine & audit logging. |
| `festejo-stellar-sdk` | Blockchain | Interface for Stellar signing & contract interactions. |
| `festejo-events` | Domain Service | Event lifecycle management & attendance. |
| `festejo-identity` | Domain Service | Identity graph, reputation, & passport system. |
| `festejo-economy` | Domain Service | Rewards engine, grants protocol, & marketplace. |
| `apps/legacy_app` | Compatibility | Read-only routing layer for legacy web support. |

## Development & Build Workflow

FESTEJO utilizes a hybrid Python-Rust architecture. Each repository is responsible for building its own Rust extensions.

### Prerequisites
- Python 3.11+
- Rust toolchain
- `maturin`

### Build & Integration
1.  **Rust Layer:** Each repository contains a `rust/` crate.
    ```bash
    cd rust
    cargo build --release
    ```
2.  **Binding Layer:** Use `maturin` to bridge Rust into Python.
    ```bash
    # From the repository root
    maturin develop --release
    ```
3.  **Dependency Flow:** Domain repositories (`festejo-events`, etc.) define `festejo-frsp` in their `Cargo.toml`. Python orchestrators import these via local namespaces.

## Compliance
All development must adhere to the **FRSP (FESTEJO Rust Spec Protocol)**.
- **No duplication:** Cryptographic logic must never be reimplemented in Python.
- **Canonicalization:** Use `festejo-frsp` for all hashing (`SHA256(canonical_json(data))`).
- **Isolation:** No circular dependencies between repositories are permitted.
