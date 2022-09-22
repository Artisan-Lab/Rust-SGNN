#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let index = 1;

    if index>=0 && index <x.len(){
        assert_eq!(x[index], 2);
    }

}