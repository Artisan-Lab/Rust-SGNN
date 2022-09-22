#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let mut values = Box::<[u32;3], _>::new([1,2,3]);

    assert_eq!(*values, [1, 2, 3])
}