#![allow(unused)]

fn main() {
    let str: &str = "hello";
    let s: String = str.to_string();
    assert_eq!(s, "hello");
}
