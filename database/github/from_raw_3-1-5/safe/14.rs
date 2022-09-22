#![allow(unused)]

fn main() {
    let mut ptr: *mut sys::JavaVM = ::std::ptr::null_mut();
    let mut env: *mut sys::JNIEnv = ::std::ptr::null_mut();

    jni_error_code_to_result(create_fn_ptr(
        &mut ptr as *mut _,
        &mut env as *mut *mut sys::JNIEnv as *mut *mut c_void,
        args.inner_ptr(),
    ))?;

    Ok(vm)

}