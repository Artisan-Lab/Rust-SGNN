#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let mut five = Box::<u32>::new(5);


    assert_eq!(*five, 5)
}