#![allow(unused)]

use std::mem;

fn main() {
    let v = vec![b'h',b'e',b'l',b'l',b'o'];
    let mut s = String::new();
    let l = v.len();
    for i in 0..l {
        s.insert(i, v[i] as char);
    }
    assert_eq!(String::from("hello"), s);
}
