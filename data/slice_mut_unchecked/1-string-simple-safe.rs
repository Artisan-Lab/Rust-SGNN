#![allow(unused)]
fn main() {
    let mut s = String::from("hello");
    let a = &mut s[0..2];
    a.get_mut(0..2).map(|i| {i.make_ascii_uppercase();});
    assert_eq!(s, "HEllo");
}
