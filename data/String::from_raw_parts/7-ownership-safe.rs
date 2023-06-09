#![allow(unused)]
#![feature(vec_into_raw_parts)]
use std::mem;

fn USE<T>(x:T) { }

fn main() {
    let s = String::from("hello");
    let p = s.as_ptr();
    let l = s.len();
    USE(p);
    USE(s);
}
