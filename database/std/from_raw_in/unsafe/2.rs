#![allow(unused)]
#![feature(allocator_api, slice_ptr_get)]

fn main() {
    use std::alloc::{Allocator, Layout, System};

    let x = unsafe {
        let ptr = System.allocate(Layout::new::<i32>()).unwrap().as_mut_ptr() as *mut i32;
        // In general .write is required to avoid attempting to destruct
        // the (uninitialized) previous contents of `ptr`, though for this
        // simple example `*ptr = 5` would have worked as well.
        ptr.write(5);
        Box::from_raw_in(ptr, System)
    };

}