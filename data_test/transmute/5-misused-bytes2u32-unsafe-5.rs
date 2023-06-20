/*
https://github.com/brkho/3d-engine-rust/blob/f5d6b38566639488c48f52890afedf73d49eccb4/src/util/bmp.rs#L56
*/

fn read_dword(data: &Vec<u8>, cursor: &mut usize) -> Result<u32, String> {
    let bytes = try!(read_n_bytes(data, cursor, 4));
    let mut barr = [0; 4];
    for i in 0..4 {
        barr[i] = match bytes.get(i) {
            Some(v) => *v,
            None => return Err("Incorrect byte access.".to_string()),
        }
    }
    unsafe { Ok(mem::transmute::<[u8; 4], u32>(barr)) }
}
