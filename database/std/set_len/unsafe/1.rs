#![allow(unused)]
fn main() {
    let mut vec = vec![vec![1, 0, 0],
                       vec![0, 1, 0],
                       vec![0, 0, 1]];
// SAFETY:
// 1. `old_len..0` is empty so no elements need to be initialized.
// 2. `0 <= capacity` always holds whatever `capacity` is.
    unsafe {
        vec.set_len(0);
    }
    assert!(vec.is_empty());
}