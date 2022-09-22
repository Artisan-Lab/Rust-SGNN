#![allow(unused)]

fn main() {
    // SAFETY: safe
    let mut m: [MaybeUninit<String>; 256] = unsafe { MaybeUninit::uninit().assume_init() };


}