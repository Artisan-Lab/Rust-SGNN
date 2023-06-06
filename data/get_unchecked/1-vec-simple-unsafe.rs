#![allow(unused)]
fn main() {
    let x = vec![1, 2, 4];
    let item = unsafe { x.get_unchecked(1) };
    assert_eq!(item, &2);
}
