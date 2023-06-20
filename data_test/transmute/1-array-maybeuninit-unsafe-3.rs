/*
https://github.com/rust-lang-cn/nomicon-zh-Hans/blob/3295769d85dd1f1ece0edb9e31ec818c8569e800/src/unchecked-uninit.md?plain=1#L19
*/

use std::mem::{self, MaybeUninit};
const SIZE: usize = 10;

let x = {
    let mut x: [MaybeUninit<Box<u32>>; SIZE] = unsafe {
        MaybeUninit::uninit().assume_init()
    };
    for i in 0..SIZE {
        x[i] = MaybeUninit::new(Box::new(i as u32));
    }
    unsafe { mem::transmute::<_, [Box<u32>; SIZE]>(x) }
};
