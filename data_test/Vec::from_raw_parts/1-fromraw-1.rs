/*
    From: https://github.com/hyperledger/sawtooth-core/blob/e01124bec7a8ecb7ee82afdc507d2c559697f3a8/validator/src/ffi.rs#L25
*/

#[no_mangle]
pub unsafe extern "C" fn ffi_reclaim_vec(
    vec_ptr: *mut u8,
    vec_len: usize,
    vec_cap: usize,
) -> isize {
    Vec::from_raw_parts(vec_ptr, vec_len, vec_cap);
    0
}
