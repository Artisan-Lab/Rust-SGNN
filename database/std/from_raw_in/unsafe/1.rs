#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::System;

    let y = Box::new_in(5, System);
    let (ptr, alloc) = Box::into_raw_with_allocator(y);
    let x = unsafe { Box::from_raw_in(ptr, alloc) };
}