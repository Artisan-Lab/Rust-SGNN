/*
From: https://github.com/diorahman/neon/blob/05d072448e60bba83fe7c6bcb5c5a3099e35e367/src/internal/value.rs#L266
*/

#[repr(C)]
pub struct CurlerString {
    raw: *mut u8,
    len: usize,
    capacity: usize,
}

impl Drop for CurlerString {
    fn drop(&mut self) {
        unsafe {
            drop(String::from_raw_parts(self.raw, self.len, self.capacity))
        }
    }
}
