#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;

fn main() {

    let mut x = 0u32;
    let ptr = Rc::new(x);
    let ref_x = ptr.deref();
    println!("{}", ref_x);
}