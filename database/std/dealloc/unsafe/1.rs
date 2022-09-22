#![allow(unused)]
fn main() {
    use std::alloc::{dealloc, Layout};
    use std::ptr;

    let x = Box::new(String::from("Hello"));
    let p = Box::into_raw(x);
    unsafe {
        ptr::drop_in_place(p);
        dealloc(p as *mut u8, Layout::new::<String>());
    }
}