/*
From: https://github.com/dbcfd/suricata/blob/95729e923f39b5adda31e4843a1b6ee06edbb0c8/rust/src/applayertemplate/template.rs#L287
*/
pub extern "C" fn rs_template_state_new(_orig_state: *mut std::os::raw::c_void, _orig_proto: AppProto) -> *mut std::os::raw::c_void {
    let state = TemplateState::new();
    let boxed = Box::new(state);
    return unsafe { transmute(boxed) };
}
