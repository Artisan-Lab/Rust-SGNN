#![allow(unused)]
fn main() {
    use std::rc::Rc;

    let x = Rc::new("hello".to_owned());
    let y = Rc::clone(&x);
    let x_ptr = Rc::as_ptr(&x);
    assert_eq!(x_ptr, Rc::as_ptr(&y));
    assert_eq!(unsafe { &*x_ptr }, "hello");
}