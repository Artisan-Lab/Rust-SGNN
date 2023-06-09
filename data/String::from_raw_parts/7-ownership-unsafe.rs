#![allow(unused)]
#![feature(vec_into_raw_parts)]
use std::mem;

fn USE<T>(x:T) { }

fn main() {
    let s = String::from("hello");
    let (p, l, c) = s.into_raw_parts();
    USE(p);
    unsafe { String::from_raw_parts(p,l,c); }
}
