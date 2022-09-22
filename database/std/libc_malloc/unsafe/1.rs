#![allow(unused)]
#![feature(rustc_private)]
extern crate libc;

fn main() {
    use std::mem;

    unsafe {
        let my_num: *mut i32 = libc::malloc(mem::size_of::<i32>()) as *mut i32;
        if my_num.is_null() {
            panic!("failed to allocate memory");
        }
        *my_num = 1;
        libc::free(my_num as *mut libc::c_void);
    }
}