#![allow(unused)]
#![feature(allocator_api, new_uninit)]
#![feature(get_mut_unchecked)]

fn main() { fn _inner() -> Result<(), impl core::fmt::Debug> {
    use std::rc::Rc;

    let mut five = Rc::<u32>::new(5);

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())
} _inner().unwrap() }