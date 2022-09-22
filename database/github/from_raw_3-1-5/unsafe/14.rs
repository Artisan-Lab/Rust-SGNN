#![allow(unused)]

fn main() {
    let mut ptr: *mut sys::JavaVM = ::std::ptr::null_mut();
    let mut env: *mut sys::JNIEnv = ::std::ptr::null_mut();

    unsafe {
        jni_error_code_to_result(sys::JNI_CreateJavaVM(
            &mut ptr as *mut _,
            &mut env as *mut *mut sys::JNIEnv as *mut *mut c_void,
            args.inner_ptr(),
        ))?;
        let vm = Self::from_raw(ptr)?;
        java_vm_unchecked!(vm.0, DetachCurrentThread);
        Ok(vm)
    }

}