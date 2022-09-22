#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let zero = Box::<u32, _>::new_in(0,System);

    assert_eq!(*zero, 0)
}