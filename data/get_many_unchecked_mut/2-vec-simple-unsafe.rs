/*
    This is a case from std
    Link: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.get_many_unchecked_mut
    Purpose: Returns mutable references to many indices at once, without doing any checks.
    Replaceable? Yes
*/

fn main() {
let mut v = vec![1, 2, 4];
    let [a, b] = unsafe { v.get_many_unchecked_mut([0, 2]) };
    *a *= 10;
    *b *= 100;
    assert_eq!(v, &[10, 2, 400]);
}
