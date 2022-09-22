#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() -> Result<(), impl core::fmt::Debug>{
    use std::alloc::System;

    let zero = Box::<u32, _>::try_new_zeroed_in(System)?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())
}