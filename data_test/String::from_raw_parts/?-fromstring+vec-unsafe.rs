/*
    From: https://github.com/timothee-haudebourg/iref/blob/3d09f00b356e032c0854c9e0a893c83900902dcd/src/iri/buffer.rs#L45
*/

pub fn from_string(buffer: String) -> Result<Self, (Error, String)> {
		let iri_ref = IriRefBuf::from_string(buffer)?;
		if iri_ref.scheme().is_some() {
			Ok(Self(iri_ref))
		} else {
			Err(unsafe {
				let mut vec = iri_ref.into_bytes();
				let ptr = vec.as_mut_ptr();
				let len = vec.len();
				let capacity = vec.capacity();
				std::mem::forget(vec);
				(
					Error::MissingScheme,
					String::from_raw_parts(ptr, len, capacity),
				)
			})
		}
	}
