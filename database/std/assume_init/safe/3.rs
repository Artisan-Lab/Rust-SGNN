#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main()->Result<(),impl core::fmt::Debug> {

    let mut five = Box::<u32>::new(5);

    assert_eq!(*five, 5);

    Ok::<(), std::alloc::AllocError>(())

}