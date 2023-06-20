/*
https://github.com/esp-rs/rust/blob/4896f6b455b005c410fb7ef87a2f96bf5b1b73cb/library/std/src/sys_common/net.rs#L158
*/

unsafe {
                let cur = self.cur.as_ref()?;
                self.cur = cur.ai_next;
                match sockaddr_to_addr(mem::transmute(cur.ai_addr), cur.ai_addrlen as usize) {
                    Ok(addr) => return Some(addr),
                    Err(_) => continue,
                }
}
