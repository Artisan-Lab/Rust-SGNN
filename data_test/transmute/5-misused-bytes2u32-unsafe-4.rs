/*
https://github.com/Pfarrer/rust-jvm/blob/702d6d40bc7aacdac12f131cabf1a3d52580e0c0/_deprecated/src/classfile/util/conv.rs#L15
*/

pub fn to_u32(val: [u8; 4]) -> u32 {
    let reversed = [val[3], val[2], val[1], val[0]];

    unsafe {
        std::mem::transmute::<[u8; 4], u32>(reversed)
    }
}
