/*
From: https://github.com/gsingh93/llvm/blob/70e2afca97cf044236a0a1a776c1a19b07e98bdc/src/module.rs#L93
*/
impl fmt::Display for Module {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        unsafe {
            let c_str = llvm::LLVMPrintModuleToString(self.ptr);
            let len = libc::strlen(c_str);
            let s = String::from_raw_parts(
                c_str as *mut u8,
                len + 1,
                len + 1
            );
            write!(f, "{}", s)
        }
    }
}
