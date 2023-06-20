/*
From: https://github.com/RustAudio/rust-jack/blob/ee1112e3b219e330b7a7a3657aa7b732f846da66/src/client/callbacks.rs#L321
*/
fn raw(b: &mut Box<Self>) -> *mut libc::c_void {
        let ptr: *mut Self = b.as_mut();
        ptr as *mut libc::c_void
}
