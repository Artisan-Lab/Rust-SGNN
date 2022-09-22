fn drop(&mut self) {
    unsafe {
        {
            let mut p = &self.boxes_start;
            while let Some(node) = *p {
                Finalize::finalize(&(*node.as_ptr()).data);
                p = &(*node.as_ptr()).header.next;
            }
        }
    

        let _guard = DropGuard::new();
        while let Some(node) = self.boxes_start {
            let node = Box::from_raw(node.as_ptr());
            self.boxes_start = node.header.next;
        }

    }
}