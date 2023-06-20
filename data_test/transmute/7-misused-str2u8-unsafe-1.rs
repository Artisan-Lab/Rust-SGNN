/*
https://github.com/PacktPublishing/Rust-Programming-Cookbook/blob/0afc39caaecd7d2c5343fc3c77bf484cbb9f761d/Chapter02/unsafe-ways/src/lib.rs#L26
*/

fn test_str_to_bytes_horribly_unsafe() {
        let bytes = unsafe { std::mem::transmute::<&str, &[u8]>("Going off the menu") };
        assert_eq!(
            bytes,
            &[
                71, 111, 105, 110, 103, 32, 111, 102, 102, 32, 116, 104, 101, 32, 109, 101, 110,
                117
            ]
        );
}
