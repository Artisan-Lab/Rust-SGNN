#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main()-> Result<(), impl core::fmt::Debug> {

    let zero = Box::<u32>::new(0);

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())

}