/*
    This is a case from std
    Link: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.from_raw_parts 
    Purpose: rebuild a string, a naive case
    Replaceable? Yes
*/

#![allow(unused)]
use std::mem;
use std::ptr;

fn main() {
    let s = String::from("hello");
    let mut s = mem::ManuallyDrop::new(s);

    let p = s.as_mut_ptr();
    let len = s.len();
    let capacity = s.capacity();
   
    let s = unsafe { String::from_raw_parts(p, len, capacity) }; 
    assert_eq!(String::from("hello"), s);
}
