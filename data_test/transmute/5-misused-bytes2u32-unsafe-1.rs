/*
https://github.com/Canop/broot/blob/50a825687b2324921074aea9011dd8e977918f33/src/content_search/needle.rs#L96
*/

fn find_naive_4(&self, mut pos: usize, hay: &Mmap) -> Option<usize> {
        use std::mem::transmute;
        let max_pos = hay.len() - 4;
        unsafe {
            let needle: u32 = transmute::<[u8; 4], u32>((&*self.bytes).try_into().unwrap());
            while pos <= max_pos {
                if transmute::<[u8; 4], u32>((&hay[pos..pos + 4]).try_into().unwrap()) == needle {
                    return Some(pos);
                }
                pos += 1;
            }
        }
        None
    }
