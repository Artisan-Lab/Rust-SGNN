/*
https://github.com/Titaniumtown/YTBN-Graphing-Software/blob/372219198e5abfa82a6287c7c02d707c2de1f135/src/math_app.rs#L181
*/
fn load_functions() -> Option<FunctionManager> {
					let data = get_localstorage().get_item(FUNC_NAME).ok()??;
					if crate::misc::HASH_LENGTH >= data.len() {
						return None;
					}
					let (commit, func_data) = crate::misc::hashed_storage_read(&data)?;

					if commit == const { unsafe { std::mem::transmute::<&str, &[u8]>(build::SHORT_COMMIT) } } {
						tracing::info!("Reading previous function data");
						let function_manager: FunctionManager = bincode::deserialize(&func_data).ok()?;
						return Some(function_manager);
					} else {
						None
					}
	}
