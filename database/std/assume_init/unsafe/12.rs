#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    let values = Box::<[u32]>::try_new_zeroed_slice(3).unwrap();
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0]);

}