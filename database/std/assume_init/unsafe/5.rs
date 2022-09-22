#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let mut five = Box::<u32, _>::new_uninit_in(System);

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
}