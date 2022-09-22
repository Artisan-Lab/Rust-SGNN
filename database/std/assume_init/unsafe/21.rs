#![allow(unused)]
#![feature(allocator_api, new_uninit)]
#![feature(get_mut_unchecked)]

fn main() { fn _inner() -> Result<(), impl core::fmt::Debug> {
    use std::rc::Rc;

    let mut five = Rc::<u32>::try_new_uninit()?;

// Deferred initialization:
    Rc::get_mut(&mut five).unwrap().write(5);

    let five = unsafe { five.assume_init() };

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())
} _inner().unwrap() }