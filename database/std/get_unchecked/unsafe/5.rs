#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let index = 1;
    unsafe {
        assert_eq!(x.get_unchecked(index), &2);
    }

}