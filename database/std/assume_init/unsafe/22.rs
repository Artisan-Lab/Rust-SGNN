#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() { fn _inner() -> Result<(), impl core::fmt::Debug> {
    use std::rc::Rc;

    let zero = Rc::<u32>::try_new_zeroed()?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())
} _inner().unwrap() }