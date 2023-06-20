/*
https://github.com/mobilecoinfoundation/mc-oblivious/blob/42fa076dc69ec61625cbdf23f24c51a51ad7bb95/aligned-cmov/src/cmov_impl_asm.rs#L82
*/

#[inline]
pub fn cmov_i32(condition: bool, src: &i32, dest: &mut i32) {
    let src_transmuted = unsafe { core::mem::transmute::<&i32, &u32>(src) };
    let dest_transmuted = unsafe { core::mem::transmute::<&mut i32, &mut u32>(dest) };

    cmov_u32(condition, src_transmuted, dest_transmuted);
}
