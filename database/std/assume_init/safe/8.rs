#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() -> Result<(), impl core::fmt::Debug>{
    use std::alloc::System;

    let zero = Box::<u32, _>::new_in(0,System);

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())
}