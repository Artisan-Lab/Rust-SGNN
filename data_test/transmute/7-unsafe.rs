/*
https://github.com/chain/rust-sgx-sdk/blob/6bd9d51f3c18f64c4f3c442a2f974aba65c0ea3b/sgx_rand/src/os.rs#L60
*/


fn next_u32(fill_buf: &mut FnMut(&mut [u8])) -> u32 {
    let mut buf: [u8; 4] = [0; 4];
    fill_buf(&mut buf);
    unsafe { mem::transmute::<[u8; 4], u32>(buf) }
}
