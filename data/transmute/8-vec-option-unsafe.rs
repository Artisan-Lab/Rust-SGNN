/*
From: https://doc.rust-lang.org/std/mem/fn.transmute.html
*/
#![allow(unused)]
fn main() {
    let store = [0, 1, 2, 3];
    let v_orig = store.iter().collect::<Vec<&i32>>();
    let v_clone = v_orig.clone();
    let v_transmuted = unsafe {
        std::mem::transmute::<Vec<&i32>, Vec<Option<&i32>>>(v_clone)
    };
}
