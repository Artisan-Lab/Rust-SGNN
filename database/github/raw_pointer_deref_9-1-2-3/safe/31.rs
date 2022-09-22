fn drop(&mut self) {

    let mut head = &self.boxes_start;
    while let Some(ref node) = *head {
        node.data.finalize();
        head = &node.header.next;
    }

    // Drop all allocations in the singly-linked list.
    // This could be done with `self.boxes_start = None;`,
    // but that might lead to a large number of recursive drops.
    let _guard = DropGuard::new();
    let mut head = self.boxes_start.take();
    while let Some(node) = head {
        head = node.header.next;
    }
}