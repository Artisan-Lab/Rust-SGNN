/*
https://github.com/Titaniumtown/YTBN-Graphing-Software/blob/372219198e5abfa82a6287c7c02d707c2de1f135/src/misc.rs#L174
*/
  
fn hashed_storage_create(&self, data: &[u8]) -> String {
		unsafe { std::mem::transmute::<Vec<u8>, String>([self, data].concat()) }
}
