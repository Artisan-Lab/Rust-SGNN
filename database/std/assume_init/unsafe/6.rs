#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() -> Result<(), impl core::fmt::Debug>{
    use std::alloc::System;

    let mut five = Box::<u32, _>::try_new_uninit_in(System)?;

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())
}