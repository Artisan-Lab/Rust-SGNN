pub(crate) fn increment_by<T>(slice: &mut &[T], amount: usize) {
    let lifetime_hack = unsafe {
        let slice_ptr = slice.as_ptr();
        ::std::slice::from_raw_parts(slice_ptr, slice.len())
    };
    *slice = &lifetime_hack[amount..]

}