use pyo3::prelude::*;
use festejo_frsp::proof;

#[pyfunction]
fn check_replay(hash: String) -> PyResult<bool> { Ok(proof::check_replay(&hash)) }

#[pymodule]
fn festejo_rust_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(check_replay, m)?)?;
    Ok(())
}
