#![allow(unused)]
fn main() {
    use std::alloc::{alloc, Layout};

    let x = unsafe {
        let ptr = alloc(Layout::new::<i32>()) as *mut i32;
        // In general .write is required to avoid attempting to destruct
        // the (uninitialized) previous contents of `ptr`, though for this
        // simple example `*ptr = 5` would have worked as well.
        ptr.write(5);
        Box::from_raw(ptr)
    };
    assert_eq!(*x,5)
}