#![allow(unused)]
fn main() {
    use std::slice;

// manifest a slice for a single element
    let x = 42;
    let ptr = &x as *const _;

    let slice = slice::from_ref(&x);

    assert_eq!(slice[0], 42);
}