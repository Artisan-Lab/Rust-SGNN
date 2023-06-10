#![allow(unused)]
fn main() {
    let s = "hello";
    let a = &s[0..3];
    assert_eq!(a, "hel");
}
