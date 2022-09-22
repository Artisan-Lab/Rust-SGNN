#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main()-> Result<(), impl core::fmt::Debug> {

    let zero = Box::<u32>::try_new_zeroed()?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())

}