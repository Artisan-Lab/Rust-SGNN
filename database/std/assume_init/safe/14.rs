#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let values = Box::<[u32;3], _>::new([0,0,0]);

    assert_eq!(*values, [0, 0, 0])
}