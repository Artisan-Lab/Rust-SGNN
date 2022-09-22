pub(crate) fn increment_by<T>(slice: &mut &[T], amount: usize) {

    *slice = &core::mem::replace(slice, &[])[amount..]
}