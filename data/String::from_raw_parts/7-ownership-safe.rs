#![allow(unused)]
#![feature(vec_into_raw_parts)]
use std::mem;

fn main() {
    let s = String::from("hello");
    let p = s.as_ptr();
    let l = s.len();
    USE(p);
    USE(s);
    /*
    let slice = unsafe { std::slice::from_raw_parts(p, l) };
    assert_eq!(String::from("hello"), s);
    */
}
