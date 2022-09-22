#![allow(unused)]

fn main() {
    let mut values = Box::<[u32;3]>::new([1,2,3]);

    assert_eq!(*values, [1, 2, 3]);

}