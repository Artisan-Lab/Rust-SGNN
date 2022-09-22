#![allow(unused)]
#![feature(new_uninit)]
#![feature(get_mut_unchecked)]

fn main() {
    use std::rc::Rc;

    let mut five = Rc::<u32>::new_uninit();

// Deferred initialization:
    Rc::get_mut(&mut five).unwrap().write(5);

    let five = unsafe { five.assume_init() };

    assert_eq!(*five, 5)
}