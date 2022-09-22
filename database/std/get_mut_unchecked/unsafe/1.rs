#![allow(unused)]
#![feature(get_mut_unchecked)]

fn main() {
    use std::rc::Rc;

    let mut x = Rc::new(String::new());
    unsafe {
        Rc::get_mut_unchecked(&mut x).push_str("foo")
    }
    assert_eq!(*x, "foo");
}