/*
https://github.com/matklad/gingerbread/blob/8348555ebaad59110b03002636b2fbc564d2baee/crates/parser/src/parser.rs#L55
*/

#[allow(clippy::unsound_collection_transmute)]
pub(crate) fn parse(mut self, grammar: impl Fn(&mut Self)) -> (Vec<Event>, Vec<SyntaxError>) {
  grammar(&mut self);
  for event in &self.events {
    assert!(event.is_some());
  }
  (unsafe { mem::transmute::<Vec<Option<Event>>, Vec<Event>>(self.events) }, self.errors)
 }
