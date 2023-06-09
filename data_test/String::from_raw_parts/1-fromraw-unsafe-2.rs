/*
    From: https://github.com/hyperledger/sawtooth-core/blob/e01124bec7a8ecb7ee82afdc507d2c559697f3a8/validator/src/ffi.rs#L20
*/

#[no_mangle]
pub unsafe extern "C" fn ffi_reclaim_string(s_ptr: *mut u8, s_len: usize, s_cap: usize) -> isize {
    String::from_raw_parts(s_ptr, s_len, s_cap);
    0
}
