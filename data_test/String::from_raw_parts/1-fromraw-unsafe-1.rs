/*
    From: https://github.com/fitzgen/inlinable_string/blob/f7c0a330e1ebc5223925e8c956f5e7075c13b182/src/string_ext.rs#L501
*/

unsafe fn from_raw_parts(buf: *mut u8, length: usize, capacity: usize) -> Self {
    String::from_raw_parts(buf, length, capacity)
}
