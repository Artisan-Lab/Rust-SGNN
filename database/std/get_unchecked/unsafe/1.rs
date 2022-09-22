#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &[1, 2, 4];

    unsafe {
        assert_eq!(x.get_unchecked(1) as *const i32, x.as_ptr().add(1));
    }

}