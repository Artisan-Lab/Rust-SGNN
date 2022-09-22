#![allow(unused)]
fn main() {
    let mut s = String::from("Hello");
    let bytes = s.as_bytes() ;

    assert_eq!(b"Hello", bytes);
}