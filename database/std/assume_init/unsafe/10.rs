#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let values = Box::<[u32]>::new_zeroed_slice(3);
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0])
}