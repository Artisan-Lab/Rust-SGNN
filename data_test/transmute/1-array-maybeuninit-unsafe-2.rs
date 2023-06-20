/*
https://github.com/ImageOptim/libimagequant/blob/d1d36e35350a69ac537b7dbc00b7f25549da23ab/src/rows.rs#L232
*/


#[inline(always)]
unsafe fn slice_assume_init_mut<T>(s: &mut [MaybeUninit<T>]) -> &mut [T] {
    std::mem::transmute(s)
}
