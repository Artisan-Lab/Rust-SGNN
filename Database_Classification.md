# 保留字

**操作符：**<br>
\*（char: '\*'）<br>
&  （char: '&'）（and_token: And,）<br>
[]（ Group {）（Array( ）<br>
<>（lt_token: Lt, gt_token: Gt,）<br>
::<br>
..  (char: '.'  char: '.')<br>
**类型和容器：**<br>
Box<br>
MaybeUninit<br>
Arc<br>
Vec<br>
slice<br>
vec！<br>
String<br>
struct<br>
Unsafecell<br>
Option<br>
Result<br>
Some<br>
NonZero..<br>
NonNull<br>
mut<br>
const<br>
**函数和方法：**<br>
add<br>
alloc<br>
array_assume_init<br>
as_bytes_mut<br>
as_chunks_unchecked 、 as_chunks_unchecked_mut<br>
as_ptr、as_mut_ptr<br>
as_ref 、as_uninit_ref<br>
assume_init<br>
as_mut<br>
clone<br>
dealloc 、 deallocate<br>
drop 和 drop_in_place<br>
downcast_unchecked<br>
expect<br>
forget<br>
free<br>
from_le_bytes<br>
from_raw 、 from_raw_in<br>
from_raw_parts 、 from_raw_parts_mut<br>
get、get_mut_unchecked、get_unchecked 、 get_unchecked_mut<br>
into<br>
into_raw 、 into_raw_with_allocator<br>
len<br>
libc<br>
malloc<br>
new_unchecked<br>
new_uninit<br>
new_uninit_slice<br>
new、new_in<br>
new_zeroed、new_zeroed_slice<br>
offset<br>
offset_from<br>
set_len<br>
swap_unchecked<br>
split_at_unchecked<br>
split_at_mut_unchecked<br>
slice_unchecked<br>
sub<br>
transmute<br>
to_int_unchecked<br>
to_owned<br>
uninit<br>
uninit_array<br>
unwrap_unchecked<br>
unwrap_err_unchecked<br>
unwrap<br>
unchecked_mul<br>
unchecked_add<br>
wrapping_offset<br>
wrapping_add<br>
wrapping_sub<br>
write<br>
zeroed<br>
**其他**<br>
mem<br>
key<br>
ptr<br>
self<br>
str<br>


## array_assume_init(2)(1)
- unsafe2 与1不同于unsafe修改后的应用场景
  - 修改方法均为预先对array初始化
  
unsafe1
```
#![allow(unused)]
#![feature(maybe_uninit_uninit_array)]
#![feature(maybe_uninit_array_assume_init)]
fn main() {
    use std::mem::MaybeUninit;

    let mut array: [MaybeUninit<i32>; 3] = MaybeUninit::uninit_array();
    // 对数组中的元素进行写入操作
    array[0].write(0);
    array[1].write(1);
    array[2].write(2);

    let array = unsafe {
    // 使用unsafe块将可能未初始化的数组转化为已初始化的数组
        MaybeUninit::array_assume_init(array)
    };

    assert_eq!(array, [0, 1, 2]);

}
```
对应 safe1
```
#![allow(unused)]
// fn main() {
//     let array = [0, 1, 2];
//     assert_eq!(array, [0, 1, 2]);
// }


fn main() {
    let mut array: [i32; 3] = [0; 3];
    // 对数组中的元素进行写入操作
    array[0] = 0;
    array[1] = 1;
    array[2] = 2;

    assert_eq!(array, [0, 1, 2]);
}

```
扩充 unsafe2 
```
#![feature(maybe_uninit_uninit_array)]
#![feature(maybe_uninit_array_assume_init)]

use std::mem::MaybeUninit;

fn main(){
    let mut a:[MaybeUninit<u8>; 4] = MaybeUninit::uninit_array();
    a[0].write(0);
    a[1].write(1);
    a[2].write(2);
    a[3].write(3);
    let b = u32::from_le_bytes(unsafe { MaybeUninit::array_assume_init(a) });
}
```
对应 safe2
```
fn main(){
    let mut a:[u8; 4]=[0,1,2,4];
    let b = u32::from_le_bytes(a);
    println!("{}",b);
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

github unsafe（与上std unsafe2 对应)
```
#[inline]
fn decode(decoder: &mut Decoder<'a>) -> Result<IntEncodedWithFixedSize, String> {
    let mut bytes = MaybeUninit::uninit_array();
    let _start_pos = decoder.position();
    decoder.read_raw_bytes(&mut bytes)?;

    let _end_pos = decoder.position();
    debug_assert_eq!((_end_pos - _start_pos), IntEncodedWithFixedSize::ENCODED_SIZE);

    let value = u64::from_le_bytes(unsafe { MaybeUninit::array_assume_init(bytes) });

    Ok(IntEncodedWithFixedSize(value))
}
```
github safe
```
#[inline]
fn decode(decoder: &mut Decoder<'a>) -> Result<IntEncodedWithFixedSize, String> {
    let mut bytes = MaybeUninit::uninit_array();
    let _start_pos = decoder.position();
    decoder.read_raw_bytes(&mut bytes)?;

    let _end_pos = decoder.position();
    debug_assert_eq!((_end_pos - _start_pos), IntEncodedWithFixedSize::ENCODED_SIZE);

    let value = u64::from_le_bytes(unsafe { MaybeUninit::array_assume_init(bytes) });

    Ok(IntEncodedWithFixedSize(value))
}
```
## as_bytes_mut
- unsafe1 调用 String 类型的 as_bytes_mut() 方法，并将其返回的可变字节数组绑定到变量上
  - safe方式使用 as_bytes 方法来获取不可变的字节数组引用
- unsafe2 相比1来说多了对字符的修改操作
  - safe 方式先将字符串 s 转换为可变字符串，再替换字符，最后将字符串转换为不可变的
  
unsafe 1
```
#![allow(unused)]
fn main() {
    // 创建一个可变的 String 类型变量 s 并将其初始化为 "Hello"
    let mut s = String::from("Hello");
    // 使用 unsafe 关键字调用 String 类型的 as_bytes_mut() 方法，并将其返回的可变字节数组绑定到 bytes 变量上
    let bytes = unsafe { s.as_bytes_mut() };
    // 使用 assert_eq! 宏断言 bytes 数组的值等于 b"Hello"
    assert_eq!(b"Hello", bytes);
}

```
safe 1
```
#![allow(unused)]
fn main() {
    let mut s = String::from("Hello");
    let bytes = s.as_bytes() ;

    assert_eq!(b"Hello", bytes);
}

/*
as_bytes_mut 方法返回的是字符串的底层字节数组的可变引用
safe 的方式可以使用 as_bytes 方法来获取不可变的字节数组引用
*/
```

补充 unsafe 2
```
fn main(){
    let mut s = String::from("🗻∈🌏");
    unsafe {
        let bytes = s.as_bytes_mut();
        bytes[0] = 0xF0;
        bytes[1] = 0x9F;
        bytes[2] = 0x8D;
        bytes[3] = 0x94;
    }
    assert_eq!("🍔∈🌏", s);
}
```
对应 safe 2
```
fn main(){
    let mut s = String::from("🗻∈🌏");
// 将字符串转换为可变字符串
    let mut chars = s.chars().collect::<Vec<_>>();
// 替换第一个字符
    chars[0] = '🍔';
// 将字符数组转换为字符串
    s = chars.into_iter().collect();
    assert_eq!("🍔∈🌏", s);
}
```
## as_chunks_unchecked 
- unsafe1 as_chunks_unchecked 方法来将一个字符切片分成多个固定大小的块，并返回一个数组的引用
  - safe方式使用chunks_exact方法对切片进行切分，确保每个切片块的长度都相等且不超过原始切片的长度
 
unsafe 1
```
#![allow(unused)]
#![feature(slice_as_chunks)]
fn main() {
    // 创建一个字符切片
    let slice: &[char] = &['l', 'o', 'r', 'e', 'm', '!'];
    // 使用 as_chunks_unchecked 方法将字符切片分成大小为 1 的块，并返回一个由大小为 1 的数组组成的数组的引用
    let chunks: &[[char; 1]] =
        unsafe { slice.as_chunks_unchecked() };
    assert_eq!(chunks, &[['l'], ['o'], ['r'], ['e'], ['m'], ['!']]);
    // 使用 as_chunks_unchecked 方法将字符切片分成大小为 3 的块，并返回一个由大小为 3 的数组组成的数组的引用
    let chunks: &[[char; 3]] =
        unsafe { slice.as_chunks_unchecked() };
    assert_eq!(chunks, &[['l', 'o', 'r'], ['e', 'm', '!']]);
}
```
safe 1
```
#![allow(unused)]
#![feature(slice_as_chunks)]
fn main() {
    let slice: &[char] = &['l', 'o', 'r', 'e', 'm', '!'];

    let mut chunks = Vec::new();
    const N1:usize = 1;
    if N1!= 0 && slice.len()%N1 ==0{
        let mut iter = slice.chunks_exact(N1);
        let mut c = iter.next();
        while !c.is_none(){
            chunks.push(c.unwrap());
            c = iter.next();
        }
        assert_eq!(chunks, &[['l'], ['o'], ['r'], ['e'], ['m'], ['!']]);
    }

    let mut chunks = Vec::new();
    const N2:usize = 3;
    if N2!= 0 && slice.len()%N2 ==0{
        let mut iter = slice.chunks_exact(N2);
        let mut c = iter.next();
        while !c.is_none(){
            chunks.push(c.unwrap());
            c = iter.next();
        }
        assert_eq!(chunks, &[['l', 'o', 'r'], ['e', 'm', '!']]);
    }

}
```

## as_chunks_unchecked_mut
- unsafe1 创建一个可变的字符 slice使用as_chunks_unchecked_mut 方法来将一个字符切片分成多个固定大小的块,
  - safe方式使用chunks_exact方法对切片进行切分

unsafe 1
```
#![allow(unused)]
#![feature(slice_as_chunks)]
fn main() {
    // 
    let slice: &mut [char] = &mut ['l', 'o', 'r', 'e', 'm', '!'];

    // 将 slice 转化为一组由 [char; 1] 组成的 slice，这里用到了 unsafe
    let chunks: &mut [[char; 1]] =
        unsafe { slice.as_chunks_unchecked_mut() };

    // 修改第一个 chunk 的值为 ['L']
    chunks[0] = ['L'];

    // 断言 chunks 数组的值为 [['L'], ['o'], ['r'], ['e'], ['m'], ['!']]
    assert_eq!(chunks, &[['L'], ['o'], ['r'], ['e'], ['m'], ['!']]);

    // 将 slice 转化为一组由 [char; 3] 组成的 slice，这里用到了 unsafe
    let chunks: &mut [[char; 3]] =
        unsafe { slice.as_chunks_unchecked_mut() };

    // 修改第二个 chunk 的值为 ['a', 'x', '?']
    chunks[1] = ['a', 'x', '?'];

    // 断言 slice 的值为 ['L', 'o', 'r', 'a', 'x', '?']
    assert_eq!(slice, &['L', 'o', 'r', 'a', 'x', '?']);
}

```
safe 1
```
#![allow(unused)]
#![feature(slice_as_chunks)]
fn main() {
    let slice: &mut [char] = &mut ['l', 'o', 'r', 'e', 'm', '!'];

    let mut chunks = Vec::new();
    const N1:usize = 1;
    if N1!= 0 && slice.len()%N1 ==0{
        let mut iter = slice.chunks_exact(N1);
        let mut c = iter.next();
        while !c.is_none(){
            chunks.push(c.unwrap());
            c = iter.next();
        }
        chunks[0] = &['L'];

        assert_eq!(chunks, &[['L'], ['o'], ['r'], ['e'], ['m'], ['!']]);
    }
    slice[0] = 'L';

    let mut chunks = Vec::new();
    const N2:usize = 3;
    if N2!= 0 && slice.len()%N2 ==0{
        let mut iter = slice.chunks_exact(N2);
        let mut c = iter.next();
        while !c.is_none(){
            chunks.push(c.unwrap());
            c = iter.next();
        }
        chunks[1] = &['a', 'x', '?'];
        assert_eq!(chunks, &[['L', 'o', 'r'], ['a', 'x', '?']]);
    }
    slice[3]='a';
    slice[4]='x';
    slice[5]='?';
    assert_eq!(slice, &['L', 'o', 'r', 'a', 'x', '?']);

}
```

## as_ref
- unsafe1 通过as_ref()方法将不可变指针转化为Option<&T>类型
  - safe方式创建一个指向u8类型变量10的不可变指针，并将其封装到Rc中，通过Deref trait获取指针所指向的值
- unsafe2 使用as_ref()方法将NonNull类型的指针转化为引用类型
  - safe方式将变量包装成一个引用计数智能指针Rc，使用deref()方法获取指针内部数据的引用
  -  - 1、2 修改方式无区别
unsafe 1
```
#![allow(unused)]
fn main() {
    let ptr: *const u8 = &10u8 as *const u8;

    unsafe {
        // 如果指针不为null，则通过as_ref()方法将指针转化为Option<&T>类型，并获取其中的值
        if let Some(val_back) = ptr.as_ref() {
            println!("We got back the value: {}!", val_back);
        }
    }
}

/*
不安全原因：使用指针可能会导致悬垂指针、内存泄漏、非法内存访问指针也可能指向未初始化的内存。
 */
```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;

fn main() {
    // 创建一个指向u8类型变量10的不可变指针，并将其封装到一个引用计数智能指针中
    let ptr = Rc::new(10u8 as *const u8);
    // 通过Deref trait获取指针所指向的值
    let val_back = ptr.deref();
    println!("We got back the value: {:?}!", val_back);
}

```
unsafe 2
```
fn main() {
    // 导入NonNull类型
    use std::ptr::NonNull;
    // 创建一个u32类型变量x并初始化为0
    let mut x = 0u32;
    // 将x的可变指针转化为NonNull类型的指针，并检查是否为null
    let ptr = NonNull::new(&mut x as *mut _).expect("ptr is null!");
    // 使用as_ref()方法将NonNull类型的指针转化为引用类型，并打印引用的值
    let ref_x = unsafe { ptr.as_ref() };
    println!("{}", ref_x);
}

```
safe 2
```
use std::ops::Deref;

fn main() {
    // 创建一个u32类型的变量
    let mut x = 0u32;
    // 将该变量包装成一个引用计数智能指针
    let ptr = Rc::new(x);
    // 使用deref()方法获取指针内部数据的引用
    let ref_x = ptr.deref();
    // 打印引用指向的数据
    println!("{}", ref_x);
}

```

## as_uninit_ref
- unsafe1 将指针转化为Option<MaybeUninit<&T>>类型
  - safe方式 new()然后deref()

unsafe 1
```
#![allow(unused)]
#![feature(ptr_as_uninit)]

fn main() {
    let ptr: *const u8 = &10u8 as *const u8;

    unsafe {
        // 将指针转化为Option<MaybeUninit<&T>>类型，并获取其中的值
        if let Some(val_back) = ptr.as_uninit_ref() {
            // 对MaybeUninit<&T>进行assume_init()方法调用，将其转换为&T类型的引用
            println!("We got back the value: {}!", val_back.assume_init());
        }
    }
}

```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
fn main() {
    let ptr = Rc::new(10u8 as *const u8);
    let val_back = ptr.deref();
    println!("We got back the value: {:?}!", val_back);
}
```

## assume_init
- unsafe1 (原1 3 15 5 6)  Box::<u32>::new_uninit()
- unsafe19 （原19 25 21）  Rc::<u32>::new_uninit()
- unsafe17 （原17 18）     UnsafeCell<i32>::uninit()
- unsafe2  （原2 4 7 8）  Box::<u32>::new_zeroed()
- unsafe10 （原10 12 14） Box new_zeroed_slice(3) 
- unsafe20 （原20 22 ）   Rc::<u32>::new_zeroed() 
- unsafe24               Rc new_zeroed_slice(3)
- unsafe9  （原9 16 11 13 ） Box new_uninit_slice
- unsafe23               Rc new_uninit_slice
- unsafe26               MaybeUninit::uninit().assume_init()
   - 方法均为直接new不再延迟初始化 


*Box::<u32>::new_uninit()*
  
unsafe 1
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let mut five = Box::<u32>::new_uninit();

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
}
```
unsafe 3
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main()->Result<(),impl core::fmt::Debug> {
    let mut five = Box::<u32>::try_new_uninit()?;

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())

}
```
unsafe 15
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let mut five = Box::<u32>::new_uninit();

    let five: Box<u32> = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5)
}
```
unsafe 5 
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let mut five = Box::<u32, _>::new_uninit_in(System);

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
}
```
unsafe 6
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() -> Result<(), impl core::fmt::Debug>{
    use std::alloc::System;

    let mut five = Box::<u32, _>::try_new_uninit_in(System)?;

    let five = unsafe {
        // Deferred initialization:
        five.as_mut_ptr().write(5);

        five.assume_init()
    };

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())
}
```
  
*Rc::<u32>::new_uninit()*
  
unsafe 19
```
#![allow(unused)]
#![feature(new_uninit)]
#![feature(get_mut_unchecked)]

fn main() {
    use std::rc::Rc;

    let mut five = Rc::<u32>::new_uninit();

// Deferred initialization:
    Rc::get_mut(&mut five).unwrap().write(5);

    let five = unsafe { five.assume_init() };

    assert_eq!(*five, 5)
}
```
unsafe 25(同19重复)
unsafe 21
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]
#![feature(get_mut_unchecked)]

fn main() { fn _inner() -> Result<(), impl core::fmt::Debug> {
    use std::rc::Rc;

    let mut five = Rc::<u32>::try_new_uninit()?;

// Deferred initialization:
    Rc::get_mut(&mut five).unwrap().write(5);

    let five = unsafe { five.assume_init() };

    assert_eq!(*five, 5);
    Ok::<(), std::alloc::AllocError>(())
} _inner().unwrap() }
```

*UnsafeCell<i32>::uninit()*
  
unsafe 17
```
#![allow(unused)]
fn main() {
    use std::cell::UnsafeCell;
    use std::mem::MaybeUninit;

    let m = MaybeUninit::<UnsafeCell<i32>>::uninit();
    unsafe { UnsafeCell::raw_get(m.as_ptr()).write(5); }
    let mut uc = unsafe { m.assume_init() };

    assert_eq!(uc.into_inner(), 5);

}
```
unsafe 18
```
#![allow(unused)]
fn main() {
    use std::cell::UnsafeCell;
    use std::mem::MaybeUninit;

    let m = MaybeUninit::<UnsafeCell<i32>>::uninit();
    unsafe { UnsafeCell::raw_get(m.as_ptr()).write(5); }
    let uc = unsafe { m.assume_init() };

    assert_eq!(uc.into_inner(), 5);

}
```

*Box::<u32>::new_zeroed()*
  
unsafe 2
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let zero = Box::<u32>::new_zeroed();
    let zero = unsafe { zero.assume_init() };
    assert_eq!(*zero, 0);

}
```
unsafe 4
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main()-> Result<(), impl core::fmt::Debug> {

    let zero = Box::<u32>::try_new_zeroed()?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())

}

```
unsafe 7
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let zero = Box::<u32, _>::new_zeroed_in(System);
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0)
}
```
unsafe 8
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() -> Result<(), impl core::fmt::Debug>{
    use std::alloc::System;

    let zero = Box::<u32, _>::try_new_zeroed_in(System)?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())
}
```

*Box new_zeroed_slice(3)*
  
unsafe 10
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let values = Box::<[u32]>::new_zeroed_slice(3);
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0])
}
```
unsafe 12
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    let values = Box::<[u32]>::try_new_zeroed_slice(3).unwrap();
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0]);

}
```
unsafe 14
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let values = Box::<[u32], _>::new_zeroed_slice_in(3, System);
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0])
}
```

*Rc::<u32>::new_zeroed()*
  
unsafe 20
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    use std::rc::Rc;

    let zero = Rc::<u32>::new_zeroed();
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0)
}
```
unsafe 22
```
#![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() { fn _inner() -> Result<(), impl core::fmt::Debug> {
    use std::rc::Rc;

    let zero = Rc::<u32>::try_new_zeroed()?;
    let zero = unsafe { zero.assume_init() };

    assert_eq!(*zero, 0);
    Ok::<(), std::alloc::AllocError>(())
} _inner().unwrap() }
```

*Rc::<[u32]>::new_zeroed_slice*

unsafe 24
```
#![allow(unused)]
#![feature(new_uninit)]

fn main() {
    use std::rc::Rc;

    let values = Rc::<[u32]>::new_zeroed_slice(3);
    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [0, 0, 0])
}
```
*Box new_uninit_slice*
  
unsafe 9
 ```
 #![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let mut values = Box::<[u32]>::new_uninit_slice(3);

    let values = unsafe {
        // Deferred initialization:
        values[0].as_mut_ptr().write(1);
        values[1].as_mut_ptr().write(2);
        values[2].as_mut_ptr().write(3);

        values.assume_init()
    };

    assert_eq!(*values, [1, 2, 3]);
}
 ```
unsafe 16
 ```
 #![allow(unused)]
#![feature(new_uninit)]

fn main() {
    let mut values = Box::<[u32]>::new_uninit_slice(3);

    let values = unsafe {
        // Deferred initialization:
        values[0].as_mut_ptr().write(1);
        values[1].as_mut_ptr().write(2);
        values[2].as_mut_ptr().write(3);

        values.assume_init()
    };

    assert_eq!(*values, [1, 2, 3])
}
 ```
unsafe 11
 ```
 #![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    let mut values = Box::<[u32]>::try_new_uninit_slice(3).unwrap();
    let values = unsafe {
        // Deferred initialization:
        values[0].as_mut_ptr().write(1);
        values[1].as_mut_ptr().write(2);
        values[2].as_mut_ptr().write(3);
        values.assume_init()
    };

    assert_eq!(*values, [1, 2, 3]);

}
 ```
 unsafe 13
 ```
 #![allow(unused)]
#![feature(allocator_api, new_uninit)]

fn main() {
    use std::alloc::System;

    let mut values = Box::<[u32], _>::new_uninit_slice_in(3, System);

    let values = unsafe {
        // Deferred initialization:
        values[0].as_mut_ptr().write(1);
        values[1].as_mut_ptr().write(2);
        values[2].as_mut_ptr().write(3);

        values.assume_init()
    };

    assert_eq!(*values, [1, 2, 3])
}
 ```

*Rc new_uninit_slice*
  
unsafe 23
```
#![allow(unused)]
#![feature(new_uninit)]
#![feature(get_mut_unchecked)]

fn main() {
    use std::rc::Rc;

    let mut values = Rc::<[u32]>::new_uninit_slice(3);

// Deferred initialization:
    let data = Rc::get_mut(&mut values).unwrap();
    data[0].write(1);
    data[1].write(2);
    data[2].write(3);

    let values = unsafe { values.assume_init() };

    assert_eq!(*values, [1, 2, 3])
}
```
   
补充unsafe26（与GitHub case对应）
```
use std::mem::MaybeUninit;

fn main() {
    let mut v: [MaybeUninit<Vec<i32>>; 10] = unsafe { MaybeUninit::uninit().assume_init() };
}

```
对应 safe26
```
fn main() {
    const EMPTY_VEC: Vec<i32> = Vec::new();
    let mut m = [EMPTY_VEC; 10];
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Github unsafe（与上std unsafe26 对应)
```
#![allow(unused)]
use std::mem::MaybeUninit;
fn main() {
    let mut m: [MaybeUninit<String>; 256] = unsafe { MaybeUninit::uninit().assume_init() };
}
```
Github safe
```
#![allow(unused)]
fn main() {
    const EMPTY_STRING: String = String::new();
    let mut m = [EMPTY_STRING; 256];
}
```
### dealloc

- unsafe1 把 Box 转换成裸指针，使用drop_in_place 手动调用指针指向对象的析构函数，然后使用 dealloc 函数释放指针指向的内存
  - safe方式为 drop(p)
- unsafe2 将 Box 转化为裸指针和分配器 Box::into_raw_with_allocator(x)最后释放分配器中的内存alloc.deallocate
  - safe方式为drop(ptr)、drop(alloc)
  - -  1、2的主要区别是分配方式和释放函数不同<br>

unsafe 1
```
#![allow(unused)]
fn main() {
    use std::alloc::{dealloc, Layout};
    use std::ptr;

    // 分配一个堆上的字符串
    let x = Box::new(String::from("Hello"));
    // 把 Box 转换成裸指针
    let p = Box::into_raw(x);

    unsafe {
        // 手动调用指针指向对象的析构函数
        ptr::drop_in_place(p);

        // 使用正确的布局释放内存
        dealloc(p as *mut u8, Layout::new::<String>());
    }
}

// dealloc 用于释放任何类型的内存，drop_in_place 只能用于实现了 Drop trait 的类型
// dealloc 需要传递一个额外的 Layout 对象，以便确定内存块的大小和对齐方式，而 drop_in_place 不需要
/* 
首先使用 ptr::drop_in_place 函数手动调用指针指向对象的析构函数，以确保在释放内存之前对象的资源得到正确的清理。
然后使用 dealloc 函数释放指针指向的内存，并使用 Layout::new::<String>() 函数来确定要释放的内存的正确布局
*/

/*调用了 ptr::drop_in_place 函数销毁 String 实例，然后使用 dealloc 函数将分配的内存释放回去 */

```
safe 1
```
#![allow(unused)]
fn main() {
    use std::alloc::{dealloc, Layout};
    use std::ptr;

    let x = Box::new(String::from("Hello"));
    let p = Box::into_raw(x);
    drop(p);

}
```
unsafe 2
```
#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::{Allocator, Layout, System};
    use std::ptr::{self, NonNull};

    // 在 System 分配器上分配一个字符串的堆空间，将其放在 Box 中并将 Box 放入 x 中
    let x = Box::new_in(String::from("Hello"), System);
    // 将 Box 转化为裸指针和分配器
    let (ptr, alloc) = Box::into_raw_with_allocator(x);

    unsafe {
        // 析构 Box 内存中的值，但不释放分配器
        ptr::drop_in_place(ptr);

        // 创建一个非空指针
        let non_null = NonNull::new_unchecked(ptr);

        // 释放分配器中的内存
        // 需要指定释放的内存的布局，即字符串的大小和对齐方式
        alloc.deallocate(non_null.cast(), Layout::new::<String>());
    }
}



/*
调用 ptr::drop_in_place 函数，显式地销毁了 String 实例，然后使用 alloc 实例的 deallocate 方法，将分配的内存释放回去
*/
```
safe 2
```
#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::{Allocator, Layout, System};
    use std::ptr::{self, NonNull};

    let x = Box::new_in(String::from("Hello"), System);
    let (ptr, alloc) = Box::into_raw_with_allocator(x);
    drop(ptr);
    drop(alloc);
}
```
### downcast_unchecked
- unsafe1 使用了 downcast_unchecked() 方法来将变量类型是 Box\<dyn Any> 的x中的值转换成 usize 类型
  - safe方式为使用 if let 和 downcast() 方法

unsafe 1
```
#![allow(unused)]
#![feature(downcast_unchecked)]

fn main() {
    use std::any::Any;

    // 创建了一个 Box 指针，指向一个 usize 类型的整数 1。
    // 这个 Box 指针的类型是 Box<dyn Any>，它可以持有任何实现了 Any trait 的类型的值。
    let x: Box<dyn Any> = Box::new(1_usize);
    // trait 对象的类型是不确定的，因此需要使用 dyn 关键字来表示

    unsafe {
        // 调用 downcast_unchecked 方法，将 Box<dyn Any> 类型的值转换为 usize 类型的值。
        // 这个方法的返回值是一个裸指针 *mut T，它指向了 Box 中持有的实际值的内存位置。
        assert_eq!(*x.downcast_unchecked::<usize>(), 1);
    }
}
```
safe 1
```
#![allow(unused)]
#![feature(downcast_unchecked)]

fn main() {
    use std::any::Any;

    let x: Box<dyn Any> = Box::new(1_usize);

    if let Ok(value) = x.downcast::<usize>() {
        assert_eq!(*value, 1);
    }

}


```

### drop_in_place
- unsafe1 释放指向实现了 Drop trait 的string的指针 
- unsafe2 释放基本类型 i32  的指针 
- unsafe3..18 释放余下16基本类型的指针
- unsafe19 释放自定义类型Vec<u8> 
- unsafe20 释放包含在Vec容器中的对象（上述容器均为Box）
---------------------------------------修改方法均为drop
  
unsafe 1
```
#![allow(unused)]
fn main() {
    use std::alloc::{dealloc, Layout};
    use std::ptr;

    let x = Box::new(String::from("Hello"));
    let p = Box::into_raw(x);
    unsafe {
        ptr::drop_in_place(p);
        dealloc(p as *mut u8, Layout::new::<String>());
        // 由于 String 类型并没有显式实现 Drop trait，因此需要手动调用 std::alloc::dealloc() 函数来释放指向 Box<String> 的内存，同时也需要传递适当的布局信息 Layout::new::<String>()，以确保正确的内存大小和对齐方式
    }
}



// 同delloc 1
// std::ptr::drop_in_place() 函数可以用于释放指向实现了 Drop trait 的数据类型的指针
// 数据类型包括 Rust 内建的基本类型，以及标准库和用户自定义的复杂数据类型，例如 String、Vec<T>、HashMap<K, V>、Rc<T>、Arc<T> 等

// 此代码 1 释放string 
// 扩充：2 释放基本类型 i32   
// 扩充：19 释放自定义类型Vec<u8>
// 扩充： 20 释放包含Vec容器中的对象


/*
Rust 的基本类型（如整数、浮点数、布尔值等）并不需要实现 Drop trait，因为它们的生命周期和所有权都是由编译器自动管理的，它们的内存分配和释放都是在编译时处理的。因此，基本类型的实例可以在离开作用域时自动被释放，不需要手动调用 drop() 方法来释放它们的资源
对于包含基本类型的结构体或枚举等自定义类型，如果它们包含需要释放的资源（如堆上分配的内存），则需要实现 Drop trait 来释放这些资源
*/

// 在 Rust 中，一般情况下不需要手动释放容器。一些特殊情况如使用 Box::into_raw 将一个对象转换为原始指针后，需要手动释放内存
        
```
safe 1
```
#![allow(unused)]
fn main() {
    use std::alloc::{dealloc, Layout};
    use std::ptr;

    let x = Box::new(String::from("Hello"));
    let p = Box::into_raw(x); // 可以不要
    drop(p);

}
```
补充 unsafe 2.rs
```
fn main() {
    let mut x = 123;
    let p = &mut x as *mut i32;
    // 通过 &mut x 取出 x 的可变引用，并将其转换成了一个 *mut i32 类型的原始指针 p，表示指向 x 所在的内存地址

    unsafe {
        std::ptr::drop_in_place(p);
        // 手动释放了 i32 类型对象所占用的内存
    }
}

```
对应 safe 2.rs 
```
fn main() {
    let mut x = 123;
    std::mem::drop(x);
}
```
补充 unsafe 19.rs
```
// 定义一个包含 Vec<u8> 数据的自定义类型 MyStruct
struct MyStruct {
    data: Vec<u8>,
}

// 为 MyStruct 类型实现 Drop trait
impl Drop for MyStruct {
    fn drop(&mut self) {
        // 在对象被释放时打印一条消息
        println!("Dropping MyStruct");
    }
}

fn main() {
    // 创建一个 MyStruct 对象并初始化它的 data 字段
    let my_struct = MyStruct {
        data: vec![1, 2, 3],
    };

    // 将 MyStruct 对象转换为 Box，并获取它的原始指针
    let ptr = Box::into_raw(Box::new(my_struct));

    // 使用 unsafe 块和 drop_in_place 函数释放指针所指向的对象的内存
    unsafe {
        std::ptr::drop_in_place(ptr);
    }
}

```
对应 safe 19.rs 
```
struct MyStruct {
    data: Vec<u8>,
}
impl Drop for MyStruct {
    fn drop(&mut self) {
        println!("Dropping MyStruct");
    }
}

fn main() {
    let my_struct = MyStruct {
        data: vec![1, 2, 3],
    };
    let ptr = Box::leak(Box::new(my_struct));
    std::mem::drop(ptr);
}

```
补充 unsafe 20.rs
```
fn main() {
    let mut v = Vec::new();
    v.push(1);
    v.push(2);
    v.push(3);
    let p = v.as_mut_ptr();
    let len = v.len();
    // 强制忘记这个 Vec，使内存不会被自动释放
    std::mem::forget(v);

    unsafe {
        for i in 0..len {
            std::ptr::drop_in_place(p.add(i));
        }
        std::alloc::dealloc(p as *mut u8, std::alloc::Layout::new::<i32>());
    }
}

```
对应 safe 20.rs
```
fn main() {
    let mut v = Vec::new();
    v.push(1);
    v.push(2);
    v.push(3);
    let mut v = std::mem::take(&mut v); // 通过take函数获取Vec中的所有权并将其置为空，避免使用forget函数
    while let Some(val) = v.pop() {  // 通过pop函数获取Vec中的元素并释放
        drop(val);
    }
}

```

## from_raw
- unsafe1  创建Box\<i32>，into_raw转换，from_raw转换后 drop
  - safe方式为drop裸指针
- unsafe2  创建Box\<i32>，into_raw转换，from_raw转换后使用
  - safe方式为into_raw与from_raw成对删除 new后直接使用
- unsafe4  创建Box\<string>，into_raw转换，from_raw转换后使用
  - safe方式为into_raw与from_raw成对删除 new后直接使用
- 扩充unsafe6 创建Rc\<i32>，into_raw转换，from_raw转换后使用
  - safe方式为into_raw与from_raw成对删除 new后直接使用
- unsafe5  创建Rc\<String>，into_raw转换，from_raw转换后使用
  - safe方式为into_raw与from_raw成对删除 new后直接使用
- unsafe3  将alloc返回的裸指针强制转换指向 i32 类型的指针，from_raw转换成Box\<i32>后使用
  - safe方式为删除alloc与from_raw new后直接使用
- 扩充unsafe7 将alloc返回的裸指针强制转换指向 i32 类型的指针，from_raw转换成Rc\<i32>后使用
  - safe方式为删除alloc与from_raw new后直接使用

unsafe 1
```
#![allow(unused)]
fn main() {
    // 创建一个堆上分配的 i32 类型的 Box，其值为 88
    let my_speed: Box<i32> = Box::new(88);
    // 把 Box 转换为指向内存地址的裸指针
    let my_speed: *mut i32 = Box::into_raw(my_speed);
    unsafe {
        // 用 drop 函数释放内存，在释放内存之前，使用 Box::from_raw 函数从裸指针重新创建 Box 类型对象
        drop(Box::from_raw(my_speed));
    }
}
```
safe 1
```
#![allow(unused)]
fn main() {
    let my_speed: Box<i32> = Box::new(88);
    let my_speed: *mut i32 = Box::into_raw(my_speed);
    drop(my_speed);
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    let ptr = Box::into_raw(Box::new(5));
    let x = unsafe { Box::from_raw(ptr) };
    assert_eq!(*x,5)
}
```
safe 2
```
#![allow(unused)]
fn main() {
    let x = Box::new(5);
    assert_eq!(*x,5)
}
```
unsafe 3
```
#![allow(unused)]
fn main() {
    use std::alloc::{alloc, Layout};

    let x = unsafe {
        let ptr = alloc(Layout::new::<i32>()) as *mut i32;
        ptr.write(5);
        Box::from_raw(ptr)
    };
    assert_eq!(*x,5)
}


// 1 2 4 5 into_raw和from_raw成对出现
```
safe 3
```
#![allow(unused)]
fn main() {
    use std::alloc::{alloc, Layout};

    let x = Box::new(5);
    assert_eq!(*x,5)
}
```
unsafe 4
```
#![allow(unused)]
fn main() {
    let x = Box::new(String::from("Hello"));
    let ptr = Box::into_raw(x);
    let x = unsafe { Box::from_raw(ptr) };
}
```
safe 4
```
#![allow(unused)]
fn main() {
    let x = Box::new(String::from("Hello"));

}
```
unsafe 5
```
#![allow(unused)]
fn main() {
    use std::rc::Rc;

    let x = Rc::new("hello".to_owned());
    //to_owned() 方法会将传入的 &str 转换成 String 类型的字符串
    let x_ptr = Rc::into_raw(x);

    unsafe {
        let x = Rc::from_raw(x_ptr);
        assert_eq!(&*x, "hello");
    }
}
```

修改 safe5 
```
#![allow(unused)]
use std::ops::Deref;
fn main() {
    use std::rc::Rc;

    let x = Rc::new("hello".to_owned());

    assert_eq!( &*x , "hello");
    // assert_eq!(x.deref(), "hello");
    // x.deref() 和 &*x 都是将 Rc<String> 转换为 &str 类型的引用
    // 原unsafe代码此处为&*x 不需要修改 

}
```

扩充 unsafe6
```
use std::alloc::{alloc, Layout};
use std::rc::Rc;

fn main() {
    let x = Rc::new(42);
    x_ptr = Rc::into_raw(x.clone());
    x = unsafe { Rc::from_raw(x_ptr) };
    assert_eq!(*x, 42);

}
```
对应 safe6
```
use std::rc::Rc;

fn main() {
    let x = Rc::new(42);
    //  let x_clone = x.clone();
    //  let x = Rc::clone(&x_clone);
    assert_eq!(*x, 42);
}

```
扩充 unsafe7
```
use std::alloc::{alloc, Layout};
use std::rc::Rc;

fn main() {
    let ptr = unsafe { alloc(Layout::new::<i32>()) } as *mut i32;
    unsafe { ptr.write(42) };
    let rc = unsafe { Rc::from_raw(ptr) };
    assert_eq!(*rc, 42);
}
```
对应 safe7
```
use std::rc::Rc;

fn main() {
    let rc = Rc::new(42);
    assert_eq!(*rc, 42);
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
github unsafe（???没看懂）
```
#![allow(unused)]

fn main() {
    let mut ptr: *mut sys::JavaVM = ::std::ptr::null_mut();
    let mut env: *mut sys::JNIEnv = ::std::ptr::null_mut();

    unsafe {
        jni_error_code_to_result(sys::JNI_CreateJavaVM(
            &mut ptr as *mut _,
            &mut env as *mut *mut sys::JNIEnv as *mut *mut c_void,
            args.inner_ptr(),
        ))?;
        let vm = Self::from_raw(ptr)?;
        java_vm_unchecked!(vm.0, DetachCurrentThread);
        Ok(vm)
    }

}
```
github safe
```
#![allow(unused)]

fn main() {
    let mut ptr: *mut sys::JavaVM = ::std::ptr::null_mut();
    let mut env: *mut sys::JNIEnv = ::std::ptr::null_mut();

    jni_error_code_to_result(create_fn_ptr(
        &mut ptr as *mut _,
        &mut env as *mut *mut sys::JNIEnv as *mut *mut c_void,
        args.inner_ptr(),
    ))?;

    Ok(vm)

}
```
## from_raw_in
- unsafe1  new_in使用 System 分配器创建Box\<i32>,into_raw_with_allocator获得指向内存地址的原始裸指针和分配器,from_raw_in
  - safe方式为直接new_in
- unsafe2  allocate后转成i32裸指针后from_raw_in
  - safe方式为直接new_in
- unsafe3  new_in使用 System 分配器创建Box\<string>,into_raw_with_allocator获得指向内存地址的原始裸指针和分配器,from_raw_in
  - safe方式为直接new_in

unsafe 1
```
#![allow(unused)]
#![feature(allocator_api)]

use std::alloc::System;

fn main() {
    // 使用 System 分配器来创建一个 i32 类型的 Box
    let y = Box::new_in(5, System);

    // 获得指向内存地址的原始裸指针和分配器
    let (ptr, alloc) = Box::into_raw_with_allocator(y);

    // 将一个 Box 从裸指针中重建，指定相应的分配器
    let x = unsafe { Box::from_raw_in(ptr, alloc) };
}


// 当使用 System 分配器时，Rust的内存管理方式类似于C语言，需要手动管理内存的分配和释放
```
safe 1
```
#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::System;

    let x = Box::new_in(5, System);

}
```
unsafe 2
```
#![allow(unused)]
#![feature(allocator_api, slice_ptr_get)]

fn main() {
    use std::alloc::{Allocator, Layout, System};

    let x = unsafe {
        let ptr = System.allocate(Layout::new::<i32>()).unwrap().as_mut_ptr() as *mut i32;
        ptr.write(5);
        Box::from_raw_in(ptr, System)
    };

}
```
safe 2
```
#![allow(unused)]
#![feature(allocator_api, slice_ptr_get)]

fn main() {
    use std::alloc::{Allocator, Layout, System};

    let x = Box::new_in(5,System);

}
```
unsafe 3
```
#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::System;

    let x = Box::new_in(String::from("Hello"), System);
    let (ptr, alloc) = Box::into_raw_with_allocator(x);
    let x = unsafe { Box::from_raw_in(ptr, alloc) };
}
```
safe 3
```
#![allow(unused)]
#![feature(allocator_api)]

fn main() {
    use std::alloc::System;

    let x = Box::new_in(String::from("Hello"), System);

}
```
## from_raw_parts
- unsafe1 使用了裸指针来获取一个变量的地址并将其转换为切片
  - safe方式使用slice::from_ref方法将变量的引用转换为切片
- 扩充unsafe2 将一个数组的指针转换为切片
  - safe方式直接使用数组的切片方法[..]来获取一个数组的切片
- 扩充unsafe3（与github中的unsafe2对应）
  - from_raw_parts 函数来创建切片的方式改为直接引用结构体中的内部字段来创建切片
- 扩充unsafe4（与github中的unsafe1对应）
  - 修改使用 mem::replace 函数替换了 slice 变量的值

unsafe 1
```
#![allow(unused)]
fn main() {
    use std::slice;

    let x = 42;
    let ptr = &x as *const _;
    // 创建一个指向 x 的指针 ptr
    let slice = unsafe { slice::from_raw_parts(ptr, 1) };
    // 从 ptr 创建一个只包含 x 的 slice     from_raw_parts 函数将裸指针转换成 slice 

    assert_eq!(slice[0], 42);

}
```
safe 1
```
#![allow(unused)]
fn main() {
    use std::slice;

    let x = 42;
    let slice = slice::from_ref(&x);
    assert_eq!(slice[0], 42);
}
```
  
补充 unsafe2
```
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let ptr = arr.as_ptr(); // 获取数组的指针
    let len = arr.len(); // 获取数组的长度
    unsafe {
        let slice = std::slice::from_raw_parts(ptr, len); // 使用from_raw_parts方法将指针转换为切片
        println!("{:?}", slice); 
    }
}

```
对应 safe2
```
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[..]; // 获取数组的切片
    println!("{:?}", slice); // 打印切片
}

```
补充 unsafe3（修改模式与github中的unsafe2对应）
```
struct MyStruct {
    data: [i32; 5],
}

impl MyStruct {
    fn get_slice(&self) -> &[i32] {
        &self.data[..]
    }
}

fn main() {
    let arr = [1, 2, 3, 4, 5];
    let ptr = arr.as_ptr();
    let len = arr.len();
    let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
    println!("{:?}", slice);
}

```
对应 safe3
```
struct MyStruct {
    data: [i32; 5],
}

impl MyStruct {
    fn get_slice(&self) -> &[i32] {
        &self.data[..]
    }
}

fn main() {
    let my_struct = MyStruct {
        data: [1, 2, 3, 4, 5],
    };
    let slice = my_struct.get_slice();
    println!("{:?}", slice);
}
```
补充 unsafe4（修改模式与github中的unsafe1对应）
```
fn main() {
    let mut data = [1, 2, 3, 4, 5];
    let ptr = data.as_ptr();
    let len = data.len();
    let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
    let new_slice = &slice[1..4];
    println!("{:?}", new_slice);
}
```
对应 safe4
```
fn main() {
    let mut data = [1, 2, 3, 4, 5];
    let mut slice = &mut data[..];
    let new_slice = std::mem::replace(&mut slice, &mut []);
    let replaced_slice = &new_slice[1..4];
    println!("{:?}", replaced_slice);
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

github unsafe1
```
pub(crate) fn increment_by<T>(slice: &mut &[T], amount: usize) {
    let lifetime_hack = unsafe {
        // 先切片中的前 amount 个元素移除
        let slice_ptr = slice.as_ptr();
        ::std::slice::from_raw_parts(slice_ptr, slice.len())
        // 使用了 from_raw_parts 函数，将一个指针和长度转换为切片
    };
    *slice = &lifetime_hack[amount..]

}
```
github safe1
```
pub(crate) fn increment_by<T>(slice: &mut &[T], amount: usize) {
    //使用了 mem::replace 函数替换了 slice 变量的值。mem::replace 函数会返回变量之前的值，并将变量的新值设置为传入的值。在这里将 slice 变量替换为一个空切片 &[]，并通过切片操作 [amount..] 从这个空切片中获取了一个新的切片，从而达到unsafe类似的目的

    *slice = &core::mem::replace(slice, &[])[amount..]
    // 直接对结构体中的内部字段进行了引用，并使用了 mem::replace 函数来替换原先的空切片
}
```
github unsafe2（对应std unsafe3）
```
impl AsRef<[u8]> for Inner {
    fn as_ref(&self) -> &[u8] {
        unsafe { std::slice::from_raw_parts(self.ptr, self.len) }
        
    }
}
```
github safe2
```
impl AsRef<[u8]> for Inner {
    fn as_ref(&self) -> &[u8] {
        
        self.buf()
    }
}
```
## from_raw_parts_mut
- unsafe1 from_raw_parts_mut(ptr, 1)
  - safe方式 使用from_mut替换from_raw_parts_mut，因为此代码创建的切片只包含一个元素
- 扩充unsafe2 （与github中的unsafe1对应）
- 扩充unsafe3 （与github中的unsafe2对应）
  - 扩充的2、3与from_raw_parts相似，修改为可变引用的切片

unsafe 1
```
#![allow(unused)]
fn main() {
    use std::slice;

// manifest a slice for a single element
    let mut x = 42;
    let mut ptr =&mut x as &mut i32;
    let slice = unsafe { slice::from_raw_parts_mut(ptr, 1) };
    // safe方式，使用from_mut替换from_raw_parts_mut，因为此代码创建的切片只包含一个元素

    assert_eq!(slice[0], 42);

}
```
safe 1
```
#![allow(unused)]
fn main() {
    use std::slice;

// manifest a slice for a single element
    let mut x = 42;
    let mut ptr =&mut x as &mut i32;

    let slice = slice::from_mut(ptr);
    assert_eq!(slice[0], 42);

}
```

补充 unsafe2（修改模式与github中的unsafe1对应）
```
fn main() {
    let mut data = [1, 2, 3, 4, 5];
    let ptr = data.as_mut_ptr();
    let len = data.len();
    let slice = unsafe { std::slice::from_raw_parts_mut(ptr, len) };
    let new_slice = &mut slice[1..4];
    println!("{:?}", new_slice);
}

```
对应 safe2
```
fn main() {
    let mut data = [1, 2, 3, 4, 5];
    let mut slice = &mut data[..];
    let new_slice = std::mem::replace(&mut slice, &mut []);
    let replaced_slice = &mut new_slice[1..4];
    println!("{:?}", replaced_slice);
}

```
补充 unsafe3（修改模式与github中的unsafe2对应）
```
struct MyStruct {
    data: [i32; 5],
}

impl MyStruct {
    fn get_slice(&mut self) -> &mut [i32] {
        &mut self.data[..]
    }
}

fn main() {
    let mut my_struct = MyStruct { data: [0; 5] };
    let ptr = my_struct.get_slice().as_mut_ptr();
    let len = my_struct.get_slice().len();
    let slice = unsafe { std::slice::from_raw_parts_mut(ptr, len) };
    slice.copy_from_slice(&[1, 2, 3, 4, 5]);
    println!("{:?}", my_struct.data);
}


```
对应 safe3
```
struct MyStruct {
    data: [i32; 5],
}

impl MyStruct {
    fn get_slice_mut(&mut self) -> &mut [i32] {
        &mut self.data[..]
    }
}

fn main() {
    let mut my_struct = MyStruct {
        data: [1, 2, 3, 4, 5],
    };
    let slice = my_struct.get_slice_mut();
    slice[0] = 10;
    println!("{:?}", slice);
}

```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
github unsafe1
```
pub(crate) fn increment_by_mut<T>(slice: &mut &mut [T], amount: usize) {
    let lifetime_hack = unsafe {
        let slice_ptr = slice.as_mut_ptr();
        ::std::slice::from_raw_parts_mut(slice_ptr, slice.len())
    };
    *slice = &mut lifetime_hack[amount..]

}
```
github safe1
```
pub(crate) fn increment_by_mut<T>(slice: &mut &mut [T], amount: usize) {

    *slice = &mut core::mem::replace(slice, &mut [])[amount..]
}
```
github unsafe2
```
impl AsMut<[u8]> for Inner {
    fn as_mut(&mut self) -> &mut [u8] {
        unsafe { std::slice::from_raw_parts_mut(self.ptr, self.len) }
        
    }
}
```
github safe2
```
impl AsMut<[u8]> for Inner {
    fn as_mut(&mut self) -> &mut [u8] {
        
        self.buf_mut()
    }
}
```

## from_u32_unchecked
- unsafe1 将 u32 类型的值转换成chart
- unsafe2 将 u32 类型的值转换成chart
  - safe方式均为将from_u32_unchecked改为from_u32
  - 1、2区别在于Unicode 1无效2有效，本质没区别
 
unsafe 1
```
#![allow(unused)]
// Undefined behaviour
fn main() {
unsafe { char::from_u32_unchecked(0x110000) };
}
```

修改 safe1
```
/*
fn main() {
    char::from_u32(0x110000);
}
*/
fn main() {
    let c = char::from_u32(0x110000);
    if let Some(c) = c {
        println!("Valid Unicode character: {}", c);
    } else {
        println!("Invalid Unicode character");
    }
}

```
unsafe 2
```
#![allow(unused)]
fn main() {
    use std::char;
    let c = unsafe { char::from_u32_unchecked(0x2764) };

    assert_eq!('❤', c);
}
```
safe 2
```
#![allow(unused)]
fn main() {
    use std::char;

    let c = char::from_u32(0x2764);

    assert_eq!('❤', c);
}
```

## get_mut_unchecked
- unsafe 调用 get_mut_unchecked() 方法获取Rc的可变引用，在 unsafe 代码块中改 String 对象
  - safe方式调用Rc::get_mut方法获取可变引用

unsafe 1
```
#![allow(unused)]
#![feature(get_mut_unchecked)]

fn main() {
    use std::rc::Rc;

    let mut x = Rc::new(String::new());
    unsafe {
        //  使用 unsafe 块来使用 get_mut_unchecked 方法，强制获取 Rc 智能指针的可变引用，并调用 push_str 方法添加字符串 "foo"
        Rc::get_mut_unchecked(&mut x).push_str("foo")
    }
    assert_eq!(*x, "foo");
}
```
safe 1
```
#![allow(unused)]
use std::ops::Deref;

fn main() {
    use std::rc::Rc;

    let mut x = Rc::new(String::new());
    
    Rc::get_mut(&mut x).expect("REASON").push_str("foo");

    assert_eq!(*x, "foo");
}
```
## get_unchecked
- unsafe2（合并1 2 3 5）在不进行边界检查的情况下获取一个数组中的元素
- unsafe4 在不进行边界检查的情况下获取Unicode字符的slice
- 扩充unsafe6 在不进行边界检查的情况下获取一个slice中的元素
- 扩充unsafe7 在不进行边界检查的情况下获取指定索引位置上的key
- 扩充unsafe8 进行边界检查的情况下获取指定索引位置上的value


unsafe 2
```
#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];

    unsafe {
        assert_eq!(x.get_unchecked(1), &2);
    }
}
```
safe 2
```
#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &[1, 2, 4];

    assert_eq!(&x[1], &2);
}
```
unsafe 1
```
#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &[1, 2, 4];

    unsafe {
        assert_eq!(x.get_unchecked(1) as *const i32, x.as_ptr().add(1));
    }

}
```
safe 1
```
#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &[1, 2, 4];

    assert_eq!(x[1], (*x)[1]);
}
```
unsafe 3
```
#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let x_ptr = x.as_ptr();

    unsafe {
        for i in 0..x.len() {
            assert_eq!(x.get_unchecked(i), &*x_ptr.add(i));
        }
    }
}
```
safe 3
```
#![allow(unused)]

fn main() {
    let x = &[1, 2, 4];

    for i in 0..x.len() {
        assert_eq!(x[i], (*x)[i]);
    }
}
```
unsafe 5
```
#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let index = 1;
    unsafe {
        assert_eq!(x.get_unchecked(index), &2);
    }

}
```
safe 5
```
#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let index = 1;

    if index>=0 && index <x.len(){
        assert_eq!(x[index], 2);
    }

}
```
unsafe 4
```
#![allow(unused)]
fn main() {
    let v = "🗻∈🌏";
    unsafe {
        assert_eq!("🗻", v.get_unchecked(0..4));
        assert_eq!("∈", v.get_unchecked(4..7));
        assert_eq!("🌏", v.get_unchecked(7..11));
    }
}
```
safe 4
```
#![allow(unused)]
fn main() {
    let v = "🗻∈🌏";
    assert_eq!("🗻", &v[0..4]);
    assert_eq!("∈", &v[4..7]);
    assert_eq!("🌏", &v[7..11]);
}
```


补充 unsafe6
```
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4]; // 获取数组 arr 中索引 1 到 3 的 slice
    // 使用 get_unchecked 方法获取 slice 中的元素，这里获取索引为 1 的元素
    let element = unsafe { slice.get_unchecked(1) };
    println!("{}", element);
}
```
对应 safe6
```
fn main() {
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4]; 
    let element = slice.get(1); // 使用 get 方法替代 get_unchecked 方法
    if let Some(e) = element {
        println!("{}", e);
    } else {
        println!("Failed");
    }
}

```

补充 unsafe7（与github unsafe1 对应）
```
fn main() {
    struct MyStruct<K, V> {
        map: Vec<(K, V)>,
        idx: usize,
    }

    impl<K, V> MyStruct<K, V> {
        pub fn key(&self) -> &K {
            unsafe {
                let (key, _) = self.map.get_unchecked(self.idx);
                key
            }
        }
    }

    let my_struct = MyStruct {
        map: vec![("foo", 42)],
        idx: 0,
    };
    println!("{}", my_struct.key()); // output: "foo"
}

```
对应 safe7
```
fn main() {
    struct MyStruct<K, V> {
        map: Vec<(K, V)>,
        idx: usize,
    }

    impl<K, V> MyStruct<K, V> {
        pub fn key(&self) -> &K {
            let (key, _) = &self.map[self.idx];
            // 接使用 & 取出 self.map 中对应索引位置上的key用 get_unchecked 函数
            key
        }
    }

    let my_struct = MyStruct {
        map: vec![("foo", 42)],
        idx: 0,
    };
    println!("{}", my_struct.key()); // output: "foo"
}

```
补充 unsafe8（与github unsafe2对应））
```
// 声明一个包含两个泛型参数 K 和 V 的结构体 MyStruct
struct MyStruct<K, V> {
    map: Vec<(K, V)>, // 存储键值对的 Vec
    idx: usize, // 记录要访问的键值对在 Vec 中的索引
}

impl<K, V> MyStruct<K, V> {
    // 定义一个公共方法 get，返回当前实例指定索引位置上的值的不可变引用
    pub fn get(&self) -> &V {
        unsafe {
            let (_, value) = self.map.get_unchecked(self.idx); // 获取指定索引位置上的值
            value // 返回值的不可变引用
        }
    }
}
// 创建一个 MyStruct 实例，并输出它在指定索引位置上的值
let my_struct = MyStruct {
    map: vec![("foo", 42)], // 创建包含一组键值对的 Vec
    idx: 0, // 指定要访问的键值对的索引
};
println!("{}", my_struct.get()); 


```
对应 safe8
```
fn main() {
    struct MyStruct<K, V> {
        map: Vec<(K, V)>,
        idx: usize,
    }

    impl<K, V> MyStruct<K, V> {
        pub fn get(&self) -> &V {
        // 直接使用 & 取出 self.map 中对应索引位置上的value，，无需使用 get_unchecked 函数
            let (_, value) = &self.map[self.idx];
            value
        }
    }

    let my_struct = MyStruct {
        map: vec![("foo", 42)],
        idx: 0,
    };
    println!("{}", my_struct.get()); // output: 42
}


```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
github unsafe1（与上std unsafe7对应)
```
##[inline]
pub fn key(&self) -> &K {
    // 调用了 get_unchecked 方法，从 self.map.store 中获取索引为 self.idx 的元素的 key 字段
    unsafe { &self.map.store.get_unchecked(self.idx).key }

}
```
github safe1
```
#[inline]
pub fn key(&self) -> &K {

    match &*self.pair {
        Some(pair) => &pair.key,
        None => unreachable!(),
    }
}
```
github unsafe2（与上std unsafe7对应)
```
#[inline]
pub fn get(&self) -> &V {
    unsafe { 
        // get_unchecked()绕过运行时索引检查来获取指定索引位置上的值
        if let Node { value: Some(v), .. } = self.map.store.get_unchecked(self.idx) {
            v
        } else {
            unreachable!()
        }

    }
}
```
github safe2
```
#[inline]
pub fn get(&self) -> &V {

    match &*self.pair {
        Some(pair) => &pair.value,
        None => unreachable!(),
    }
}
```
## get_unchecked_mut
- unsafe1 获取可变引用的指定位置上的元素，并将其地址与原数组中的地址进行比较
- unsafe2 修改一个可变切片中指定位置的值
- unsafe3  使用get_unchecked_mut获取可变字符串的指定子串
- 扩充unsafe4 使用 get_unchecked_mut 方法获取整型的 Vec 对象从下标 1 到 2 的切片，并将该切片中的元素都加 1

unsafe 1
```
#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &mut [1, 2, 4];
    let index = 1;
    unsafe {
        assert_eq!(x.get_unchecked_mut(index) as *mut i32, x.as_mut_ptr().add(index));
    }
}   
```
safe 1
```
#![allow(unused)]
#![feature(slice_ptr_get)]

fn main() {
    let x = &mut [1, 2, 4];
    let index = 1;

    assert_eq!(x[index], (*x)[index]);
}
```

unsafe 2
```
#![allow(unused)]
fn main() {
    let x = &mut [1, 2, 4];
    let index = 1;

    unsafe {
        let elem = x.get_unchecked_mut(index);
        *elem = 13;
    }
    assert_eq!(x, &[1, 13, 4]);
}
```
safe 2
```
#![allow(unused)]

fn main() {
    let x = &mut [1, 2, 4];
    let index = 1;
    x[index] = 13;
    assert_eq!(x, &[1, 13, 4]);
}
```

unsafe 3
```
#![allow(unused)]
fn main() {
    let mut v = String::from("🗻∈🌏");
    unsafe {
        assert_eq!("🗻", v.get_unchecked_mut(0..4));
        assert_eq!("∈", v.get_unchecked_mut(4..7));
        assert_eq!("🌏", v.get_unchecked_mut(7..11));
    }
}
```
safe 3
```
#![allow(unused)]
fn main() {
    let mut v = "🗻∈🌏";
    assert_eq!("🗻", &v[0..4]);
    assert_eq!("∈", &v[4..7]);
    assert_eq!("🌏", &v[7..11]);
}
```


补充 unsafe4
```
fn main() {
    let mut vec = vec![1, 2, 3];
    // 创建了一个 Vec 对象，并使用 get_unchecked_mut 方法获取一个元素切片
    let slice = unsafe { vec.get_unchecked_mut(1..3) };
    for elem in slice {
        *elem += 1;
    }
    println!("{:?}", vec); 
}
```
对应 safe4
```
fn main() {
    let mut vec = vec![1, 2, 3];
    if let Some(slice) = vec.get_mut(1..3) {
        for elem in slice {
            *elem += 1;
        }
        println!("{:?}", vec); 
    }
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## libc_malloc
- unsafe1 使用 libc::malloc 分配了堆上的内存空间，需要使用 libc::free 来释放
  - safe方式 引用获取堆栈上的内存空间，使用 drop 释放指针

unsafe 1
```
// 允许未使用的代码和使用 unstable 的 rustc 特性
#![allow(unused)]
#![feature(rustc_private)]

// 导入 libc 和 mem 模块
extern crate libc;
use std::mem;

fn main() {
    unsafe {
        // 申请分配一块大小为 i32 类型的内存块，返回值为 *mut i32 类型的指针
        let my_num: *mut i32 = libc::malloc(mem::size_of::<i32>()) as *mut i32;
        // 判断申请的内存块是否为 null 指针，如果是，抛出错误信息
        if my_num.is_null() {
            panic!("failed to allocate memory");
        }
        // 将申请到的内存块赋值为 1
        *my_num = 1;
        // 释放申请的内存块，由于类型为 i32，需要将其转为 *mut libc::c_void 类型
        libc::free(my_num as *mut libc::c_void);
    }
}

```
safe 1
```
#![allow(unused)]
#![feature(rustc_private)]

fn main() {
    use std::mem;
    let mut y: i32 = 1;
    let my_num: *mut i32 = y as *mut i32;
    if my_num.is_null() {
        panic!("failed to allocate memory");
    }

    drop(my_num);
}
```
## transmute
- unsafe1 将字节数组转换为无符号整数
  - safe方式使用from_be_bytes将字节数组转换为整数类型
- unsafe2 将指向i32类型变量的指针转换为一个usize类型的值
  - safe方式使用as操作符来将指针转换为整数类型
- 扩充unsafe3 将一个 u32 类型的数字转换为一个 i32 类型的数字

unsafe 1
```
#![allow(unused)]
fn main() {
    let raw_bytes = [0x78, 0x56, 0x34, 0x12];
    let num = unsafe {
        std::mem::transmute::<[u8; 4], u32>(raw_bytes)
    };

}
```
safe 1
```
#![allow(unused)]
fn main() {
    let raw_bytes = [0x78, 0x56, 0x34, 0x12];

    let num = u32::from_be_bytes(raw_bytes);
    assert_eq!(num, 0x78563412);
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    let ptr = &0;
    let ptr_num = unsafe {
        std::mem::transmute::<&i32, usize>(ptr)
    };

}
```
safe  2
```
#![allow(unused)]
fn main() {
    let ptr = &0;
    let ptr_num = ptr as *const i32 as usize;
}
```
补充 unsafe3
```
fn main() {
    let x: u32 = 12345;
    let y: i32 = unsafe { std::mem::transmute(std::num::NonZeroU32::new_unchecked(x)) };
    println!("{} as i32 is {}", x, y);
}
```
对应 safe3
```
use std::convert::TryFrom;

fn main() {
    let x: u32 = 12345;
    let y = i32::try_from(x).unwrap();//try_from失败就返回一个result
    println!("{} as i32 is {}", x, y);
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## set_len
- unsafe1 set_len将一个二维向量的长度设置为0
  - safe方式使用 Vec::clear() 方法来安全地清空向量
- unsafe2 对 vec 进行截断，只保留前两个元素
  - safe方式使用Vec.truncate() 将 vec 截断
  
unsafe 1
```
fn main() {
    // 创建一个二维向量，表示单位矩阵
    let mut vec = vec![vec![1, 0, 0],
                       vec![0, 1, 0],
                       vec![0, 0, 1]];
    // 使用 `set_len` 方法将向量长度设置为 0，因此向量中不再包含任何元素
    unsafe {
        vec.set_len(0);
    }
    assert!(vec.is_empty());
}

```
safe 1
```
#![allow(unused)]
fn main() {
    let mut vec = vec![vec![1, 0, 0],
                       vec![0, 1, 0],
                       vec![0, 0, 1]];
    vec.clear();
    assert!(vec.is_empty());
}
```


补充 unsafe2
```
fn main() {
    let mut vec = vec![1, 2, 3];
    unsafe {
       vec.set_len(2);
       }
       assert_eq!(vec, vec![1, 2]);
}
```
对应 safe2
```
fn main(){
    let mut vec = vec![1, 2, 3];
    // 使用 vec.truncate(2) 将 vec 截断为长度为 2。这意味着第三个元素将从 vec 中移除
    vec.truncate(2);
    assert_eq!(vec, vec![1, 2]);
}
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
  
  
  
  


## mem_zeroed

mem::zeroed() 初始化

保留字：mem\zeroed\struct\ptr

- 初始化变量
- 初始化结构体
- 初始化指针

unsafe 1
```
#![allow(unused)]
fn main() {
    use std::mem;

    let x: i32 = unsafe { mem::zeroed() };
    assert_eq!(0, x);
}
```
safe 1
```
#![allow(unused)]
fn main() {

    let x: i32 = 0;
    assert_eq!(0, x);
}
```

扩充unsafe 2
```
use std::mem;

struct MyStruct {
    x: i32,
    y: bool,
    z: [u8; 16],
}

fn main() {
    let mut s: MyStruct = unsafe { mem::zeroed() };
}
```

对应safe 2
```
struct MyStruct {
    x: i32,
    y: bool,
    z: [u8; 16],
}

fn main() {
    let s = MyStruct {
        x: 0,
        y: false,
        z: [0; 16],
    };
}
```

扩充unsafe 3
```
use std::mem;

fn main() {
    let ptr: *mut i32 = unsafe { mem::zeroed() };
    println!("ptr is {:?}", ptr);
}

```
对应safe 3
```
fn main() {
    let ptr: Option<*mut i32> = None;
    println!("ptr is {:?}", ptr);
}

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

github unsafe 1/2
```
let mut value = unsafe { mem::zeroed() } ;//1
let mut v = unsafe { mem::zeroed() } ; //2

```
github safe 1/2
```
let mut value = mem::zeroed(); //1
//???
let mut v = mem::zeroed(); //2
//???

```
github unsafe 3
```
pub fn start<P: AsRef<Path>>(p: P) -> Result<Heap> {
    let mut slabs: [MaybeUninit<Slab>; 32] = unsafe { std::mem::zeroed() };
    // std::mem::zeroed()来初始化数组。这将为每个Slab对象分配内存

    for slab_id in 0..32 {
        let slab = Slab::start(&p, slab_id)?;
        slabs[slab_id as usize] = MaybeUninit::new(slab);

    }

    Ok(Heap { slabs: unsafe { transmute(slabs) } })

}

```
github safe 3
```
pub fn start<P: AsRef<Path>>(p: P) -> Result<Heap> {

    let mut slabs = vec![];

    for slab_id in 0..32 {
        let slab = Slab::start(&p, slab_id)?;

        slabs.push(slab);
    }

    let slabs: [Slab; 32] = slabs.try_into().unwrap();

    Ok(Heap { slabs })
}
```
github unsafe 4
```
#![allow(unused)]

fn main() {
    let mut raw_status = unsafe { mem::zeroed::<winsvc::SERVICE_STATUS_PROCESS>() };

}

```
github safe 4
```
#![allow(unused)]

fn main() {
    let mut raw_status = mem::MaybeUninit::<winsvc::SERVICE_STATUS_PROCESS>::zeroed();
}
```

## new_unchecked

new_unchecked用于创建某些类型的实例
new_unchecked() 生成的是 NonNull\<T>

- 通过 NonNull\<T> 和 new_unchecked() 生成指针类型
  - T的类型 可以进一步进行划分，其中 T 可以是 MaybeUninit\<U> 类型
  


unsafe 1
  
```
#![allow(unused)]
fn main() {
    use std::ptr::NonNull;

    let mut x = 0u32;
    let ptr = unsafe { NonNull::new_unchecked(&mut x as *mut _) };
}
```
safe 1
```
#![allow(unused)]
fn main() {
    use std::ptr::NonNull;

    let mut x = 0u32;

    let ptr = NonNull::<u32>::new(&mut x as *mut _).expect("ptr is null!");
} 
```
unsafe 2
```
#![allow(unused)]
fn main() {
    use std::ptr::NonNull;

// NEVER DO THAT!!! This is undefined behavior.
    let ptr = unsafe { NonNull::<u32>::new_unchecked(std::ptr::null_mut()) };
}
```
safe 2
```
#![allow(unused)]
fn main() {
    use std::ptr::NonNull;

// NEVER DO THAT!!! This is undefined behavior.
    let ptr =  NonNull::<u32>::new(std::ptr::null_mut()).expect("ptr is null!");
}
```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
github unsafe 1
```
pub fn new<F>(future: F) -> Self
    where
        F: Future<Output = T> + Send + 'static,
    {
        let boxed: Box<dyn Future<Output = T> + Send> = Box::new(future);

        let boxed = Box::into_raw(boxed);

        // SAFETY: Box::into_raw does not return null pointers.
        let boxed = unsafe { NonNull::new_unchecked(boxed) };
        Self { boxed }
    }
```
github safe 1
```
pub fn new<F>(future: F) -> Self
    where
        F: Future<Output = T> + Send + 'a,
    {
        let boxed: Box<dyn Future<Output = T> + Send + 'a> = Box::new(future);


        let boxed = NonNull::from(Box::leak(boxed));
        Self { boxed }
    }
   
```

## slice_unchecked
slice_unchecked 是一个 unsafe 方法，它的作用是返回一个slice
slice_unchecked 方法需要手动检查切片的起始和结束位置是否有效

safe方式将 slice_unchecked 方法替换为使用 Rust 的索引语法来完成的。在代码二中，使用 & 操作符对字符串进行切片，使用 \[start..end] 索引从字符串中提取子字符串

unsafe 1
```
#![allow(unused)]
fn main() {
    let s = "Löwe 老虎 Léopard";

    unsafe {
        assert_eq!("Löwe 老虎 Léopard", s.slice_unchecked(0, 21));
    }

    let s = "Hello, world!";

    unsafe {
        assert_eq!("world", s.slice_unchecked(7, 12));
    }
}
```
safe 1
```
#![allow(unused)]

fn main() {
    let s = "Löwe 老虎 Léopard";

    assert_eq!("Löwe 老虎 Léopard", &s[0..21]);

    let s = "Hello, world!";

    assert_eq!("world", &s[7..12]);
}
```

## split_at_unchecked

split_at_unchecked用于将 slice 分割成两个不重叠的部分，必须保证传入的分割位置是有效的

safe方式为将 split_at_unchecked 方法替换为 split_at 方法

**如果是在循环中反复调用 split_at在这种情况下使用 split_at_unchecked 可以减少一些性能开销**

unsafe 1
```
#![allow(unused)]
#![feature(slice_split_at_unchecked)]

fn main() {
    let v = [1, 2, 3, 4, 5, 6];

    unsafe {
        let (left, right) = v.split_at_unchecked(0);
        assert_eq!(left, []);
        assert_eq!(right, [1, 2, 3, 4, 5, 6]);
    }

    unsafe {
        let (left, right) = v.split_at_unchecked(2);
        assert_eq!(left, [1, 2]);
        assert_eq!(right, [3, 4, 5, 6]);
    }

    unsafe {
        let (left, right) = v.split_at_unchecked(6);
        assert_eq!(left, [1, 2, 3, 4, 5, 6]);
        assert_eq!(right, []);
    }
}
```
safe 1
```
#![allow(unused)]

fn main() {
    let v = [1, 2, 3, 4, 5, 6];

    let (left, right) = v.split_at(0);
    assert_eq!(left, []);
    assert_eq!(right, [1, 2, 3, 4, 5, 6]);


    let (left, right) = v.split_at(2);
    assert_eq!(left, [1, 2]);
    assert_eq!(right, [3, 4, 5, 6]);


    let (left, right) = v.split_at(6);
    assert_eq!(left, [1, 2, 3, 4, 5, 6]);
    assert_eq!(right, []);
}
```

## split_at_mut_unchecked

split_at_unchecked 作用将一个可变切片划分成两个可变切片
safe方式将split_at_mut_unchecked()替换为split_at_mut()

**待补充：**需要极高性能且确认传递的分割位置是合法的时候，才应该使用 split_at_mut_unchecked()


unsafe 1
```
#![allow(unused)]
#![feature(slice_split_at_unchecked)]

fn main() {
    let mut v = [1, 0, 3, 0, 5, 6];
// scoped to restrict the lifetime of the borrows
    unsafe {
        let (left, right) = v.split_at_mut_unchecked(2);
        assert_eq!(left, [1, 0]);
        assert_eq!(right, [3, 0, 5, 6]);
        left[1] = 2;
        right[1] = 4;
    }
    assert_eq!(v, [1, 2, 3, 4, 5, 6]);
}
```
safe 1
```
#![allow(unused)]
#![feature(slice_split_at_unchecked)]

fn main() {
    let mut v = [1, 0, 3, 0, 5, 6];
// scoped to restrict the lifetime of the borrows

    let (left, right) = v.split_at_mut(2);
    assert_eq!(left, [1, 0]);
    assert_eq!(right, [3, 0, 5, 6]);
    left[1] = 2;
    right[1] = 4;

    assert_eq!(v, [1, 2, 3, 4, 5, 6]);
}
```

## swap_unchecked

swap_unchecked用于交换两个指针所指向的内存位置的值,函数需要确保指针指向的内存地址有效，并且交换的数据类型是合法的

safe方式将swap_unchecked(,) 替换为 swap(,) 来进行转换的

**待补充：**在需要极高的性能时且已经确定了要交换的索引是有效的可以使用 swap_unchecked

unsafe 1
```
#![allow(unused)]
#![feature(slice_swap_unchecked)]

fn main() {
    let mut v = ["a", "b", "c", "d"];
// SAFETY: we know that 1 and 3 are both indices of the slice
    unsafe { v.swap_unchecked(1, 3) };
    assert!(v == ["a", "d", "c", "b"]);
}
```
safe 1
```
#![allow(unused)]
#![feature(slice_swap_unchecked)]

fn main() {
    let mut v = ["a", "b", "c", "d"];
// SAFETY: we know that 1 and 3 are both indices of the slice
    v.swap(1, 3);
    assert!(v == ["a", "d", "c", "b"]);
}
```
## to_int_unchecked

to_int_unchecked方法将浮点数转换为整数类型，转换过程中会进行截断

safe方式使用as将浮点数转换为整数类型，转换过程中也会进行截断，编译器会在类型无法容纳时给出警告

unsafe 1(unsafe 2与unsafe 1区别仅f64->f32)
```
#![allow(unused)]
fn main() {
    let value = 4.6_f64;
    let rounded = unsafe { value.to_int_unchecked::<u16>() };
    assert_eq!(rounded, 4);

    let value = -128.9_f64;
    let rounded = unsafe { value.to_int_unchecked::<i8>() };
    assert_eq!(rounded, i8::MIN);
}
```
safe 1
```
#![allow(unused)]
fn main() {
    let value = 4.6_f32;
    let rounded = value as u16;
    assert_eq!(rounded, 4);

    let value = -128.9_f32;
    let rounded = value as i8;
    assert_eq!(rounded, i8::MIN);
}
```
## unwrap_unchecked

unwrap_unchecked作用是直接将包装的枚举类型的值转换为内部的值，如果 Option 的值是 None 则会导致 panic

- unsafe1和unsafe2 分别针对Option ：Some(T) 和None 
- unsafe3和unsafe4 分别针对Result ：Ok(T)和Err(E) 
  - unsafe1234 本质上为同一类 修改方式为将unwrap_unchecked改为unwrap


unsafe 1
```
#![allow(unused)]
fn main() {
let x = Some("air");
assert_eq!(unsafe { x.unwrap_unchecked() }, "air");
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
let x: Option<&str> = None;
assert_eq!(unsafe { x.unwrap_unchecked() }, "air"); // Undefined behavior!
}
```
unsafe 3
```
#![allow(unused)]
fn main() {
let x: Result<u32, &str> = Ok(2);
assert_eq!(unsafe { x.unwrap_unchecked() }, 2);
}
```
unsafe 4
```
#![allow(unused)]
fn main() {
let x: Result<u32, &str> = Err("emergency failure");
unsafe { x.unwrap_unchecked(); } // Undefined behavior!
}
```


## unwrap_err_unchecked

unwrap_err_unchecked 用于从 Result 类型的值中获取错误值，如果 Result 中的值是 Ok，此方法将会导致未定义的行为

safe方式为使用 unwrap_err()替换unwrap_err_unchecked 


unsafe 1
```
//调用 unwrap_err_unchecked()，但是 x 的值是 Ok(2)，所以调用是未定义的行为
#![allow(unused)]
fn main() {
let x: Result<u32, &str> = Ok(2);
unsafe { x.unwrap_err_unchecked() }; // Undefined behavior!
}
```
unsafe 2
```
//调用unwrap_err_unchecked()，但是 x 的值是 Err("emergency failure")，所以调用会返回包含错误信息字符串的 Result
#![allow(unused)]
fn main() {
let x: Result<u32, &str> = Err("emergency failure");
assert_eq!(unsafe { x.unwrap_err_unchecked() }, "emergency failure");
}
```
## write
std::ptr::write 用于在指定地址写入一个值
unsafe 1 和 unsafe 2 **目的和操作对象不同**
unsafe 1 操作的是指向**变量** x 的可变指针 y
unsafe 2 操作的是指向**数组** data 的可变指针 ptr

unsafe 1
```
// 使用了指针写入和读取操作，而且没有对指针进行正确的生命周期管理和借用规则，存在悬空指针和多次释放等安全问题
#![allow(unused)]
fn main() {
    let mut x = 0;
    let y = &mut x as *mut i32;
    let z = 12;

    unsafe {
        std::ptr::write(y, z);
        assert_eq!(std::ptr::read(y), 12);
    }

}
```
safe 1
```
// 对变量直接修改
#![allow(unused)]
fn main() {
    let mut x = 12;
    let y = &mut x as *mut i32;

}
```
补充 unsafe 2
```
fn main() {
    let mut data = [0u8; 10];
    // 指向数组 data 的可变指针 ptr
    let mut ptr: *mut u8 = data.as_mut_ptr();

    unsafe {
    // 使用不安全的 add 方法将指针增加 5 个元素的偏移量，使其指向数组的第 6 个元素
        ptr = ptr.add(5); 
        //使用 std::ptr::write 方法向指针指向的内存位置写入值 42
        std::ptr::write(ptr, 42); 
    }

    assert_eq!(data, [0, 0, 0, 0, 0, 42, 0, 0, 0, 0]);
}

```
对应 safe 2
```
fn main() {
    let mut data = [0u8; 10];
    let mut index = 5;

    data[index] = 42;

    assert_eq!(data, [0, 0, 0, 0, 0, 42, 0, 0, 0, 0]);
}

```

## raw_pointer_deref

 （被舍弃的分类方式）不可变裸指针 \*const T｜｜可变裸指针 \*mut T||函数指针 fn(T) -> U

- 1 2 3 13 对**数组**使用裸指针进行迭代访问；4 12 指针指向的地址是一个**常量**（修改方式一致）
- 5 6  **数组** 使用裸指针修改**可变**数据
- 7 8 **UnsafeCell** 使用了 UnsafeCell 类型来创建一个内部可变的变量，并对其进行了修改（UnsafeCell 可以使得数据在编译期看起来是不可变的，但是实际上可以在运行时进行修改）
- 9 **NonNull** 使用了 NonNull 类型来创建一个非空的裸指针，并对其进行了解引用和值的修改操作
- 10 11 **Rc** 使用了 Rc 类型来创建一个共享所有权的智能指针，并对其进行了解引用操作
 
 
*1 2 3 13 对数组使用裸指针进行迭代访问
safe方式为use std::rc::Rc 智能指针类型迭代数组 使用了 Rc::new 创建智能指针，并且通过 Deref trait 实现对智能指针内容的访问
Rc 是共享所有权的，因此可以在循环中多次使用，而不需要使用裸指针进行指针操作*
 
unsafe 1
```
fn main() {
    let data = [1u8, 2, 3, 4, 5];
    let mut ptr: *const u8 = data.as_ptr();
    let step = 2;
    let end_rounded_up = ptr.wrapping_offset(6);
    while ptr != end_rounded_up {
        unsafe {
            print!("{}, ", *ptr);
        }
        ptr = ptr.wrapping_offset(step);
    }
}
```
unsafe 2
```
fn main() {
    let data = [1u8, 2, 3, 4, 5];
    let mut ptr: *const u8 = data.as_ptr();
    let step = 2;
    let end_rounded_up = ptr.wrapping_add(6);
    while ptr != end_rounded_up {
        unsafe {
            print!("{}, ", *ptr);
        }
        ptr = ptr.wrapping_add(step);
    }
}
```
unsafe 3
```
fn main() {
    let data = [1u8, 2, 3, 4, 5];
    let mut ptr: *const u8 = data.as_ptr();
    let start_rounded_down = ptr.wrapping_sub(2);
    ptr = ptr.wrapping_add(4);
    let step = 2;
    while ptr != start_rounded_down {
        unsafe {
            print!("{}, ", *ptr);
        }
        ptr = ptr.wrapping_sub(step);
    }
}
```
unsafe 13
```
fn main() {
    let data = [1u8, 2, 3, 4, 5];
    let mut ptr: *const u8 = data.as_ptr();
    let step = 2;
    let end_rounded_up = ptr.wrapping_offset(6);
    while ptr != end_rounded_up {
        unsafe {
            print!("{}, ", *ptr);
        }
        ptr = ptr.wrapping_offset(step);
    }
}
```
unsafe 4
```
// 使用一个裸指针创建了一个指向常量 10u8 的指针，然后使用 &* 操作符进行解引用，得到了指向常量的引用，输出该引用指向的值
fn main() {
    let ptr: *const u8 = &10u8 as *const u8;
    unsafe {
        let val_back = &*ptr;
        println!("We got back the value: {}!", val_back);
    }
}
```
unsafe 12
```
// 使用 Rc 包装一个指向常量 10u8 的指针，然后使用 deref() 方法得到了该指针的引用，输出该引用指向的值。
fn main() {
    let ptr: *const u8 = &20u8 as *const u8;
    unsafe {
        let val_back = &*ptr;
        println!(val_back);
    }
}
```
*5 6 数组使用裸指针修改数据
safe方式直接对数组进行操作*

unsafe 5
```
fn main() {
    let mut data = [1u8, 2, 3, 4, 5];
    let mut ptr: *mut u8 = data.as_mut_ptr();
    let step = 2;
    let end_rounded_up = ptr.wrapping_offset(6);
    while ptr != end_rounded_up {
        unsafe {
            *ptr = 0;
        }
        ptr = ptr.wrapping_offset(step);
    }
    assert_eq!(&data, &[0, 2, 0, 4, 0]);
} 
```
unsafe 6
```
fn main() {
    let mut s = [1, 2, 3];
    let ptr: *mut u32 = s.as_mut_ptr();
    let first_value = unsafe { &mut *ptr };
    *first_value = 4;
    assert_eq!(s, [4, 2, 3]);
    println!("{:?}", s); 
}
```

*7 8 UnsafeCell 使用了 UnsafeCell 类型来创建一个内部可变的变量，并对其进行了修改
safe方式为将 UnsafeCell 中的 get() 方法替换为 get_mut() 方法*

unsafe 7
```
// 使用 UnsafeCell 和 get() 方法来获取一个可变的指针，然后使用 * 运算符来访问和修改它所指向的值。同时在unsafe块内使用 &mut 来获取一个可变的指针引用，输出时用 get_mut() 方法来获取 UnsafeCell 中存储的值
#![allow(unused)]
fn main() {
    use std::cell::UnsafeCell;
    let mut x: UnsafeCell<i32> = UnsafeCell::new(5);
    unsafe 
        let p1_exclusive: &mut i32 = &mut *x.get(); 
        *p1_exclusive += 27; 
    } 
    println!("{:?}", x.get_mut());
}
```
unsafe 8
```
#![allow(unused)]
fn main() {
    use std::cell::UnsafeCell;
    let mut x: UnsafeCell<i32> = 5.into();
    unsafe {
        let p1_exclusive: &mut i32 = &mut *x.get(); 
        *p1_exclusive += 27; 
    } 
    println!("{:?}", x.get_mut());
}
```

*9 NonNull 使用了 NonNull 类型来创建一个非空的裸指针，并对其进行了解引用和值的修改操作
safe方式为不需要使用NonNull和unsafe代码来访问和修改指针，直接对变量进行复制和运算*
unsafe 9
```
fn main() {
    use std::ptr::NonNull;
    let mut x = 0u32;
    let ptr = NonNull::new(&mut x).expect("ptr is null!");
    let x_value = unsafe { *ptr.as_ptr() };
    assert_eq!(x_value, 0);
    unsafe { *ptr.as_ptr() += 2; }
    let x_value = unsafe { *ptr.as_ptr() };
    assert_eq!(x_value, 2);
}
```

*10 11 Rc 使用了 Rc 类型来创建一个共享所有权的智能指针，并对其进行了解引用操作
safe方式为直接通过Rc实例的deref()方法来获取其内部的值，不再使用Rc::into_raw()函数将Rc实例x转换为裸指针，进而解引用操作*

unsafe 10
```
fn main() {
    use std::rc::Rc;
    let x = Rc::new("hello".to_owned());
    let x_ptr = Rc::into_raw(x);
    assert_eq!(unsafe { &*x_ptr }, "hello");
}
```
unsafe 11
```
fn main() {
    use std::rc::Rc;
    let x = Rc::new("hello".to_owned());
    let y = Rc::clone(&x);
    let x_ptr = Rc::as_ptr(&x);
    assert_eq!(x_ptr, Rc::as_ptr(&y));
    assert_eq!(unsafe { &*x_ptr }, "hello");
}
```
—————————————————————————————————————————————————————————————————————


<font color=‘red’>unchecked_add;unchecked_mul;offset;offset_from;pointer_add;pointer_sub;pointer_as_mut </font>

API余7
## unchecked_add

unsafe 1～unsafe 6 都使用了 NonZero 类型： NonZeroU8、NonZeroU16、NonZeroU32、NonZeroU64、NonZeroU128、NonZeroUsize

safe方式为将 unchecked_add 替换为 checked_add ，然后将返回值替换为Option 类型（如果加法操作不导致整数溢出会返回一个包含结果的 Some、否则会返回 None ）

unsafe 1
```
#![allow(unused)]
#![feature(nonzero_ops)]
use std::num::NonZeroU16;

fn main() -> (){

    let one = NonZeroU16::new(1).unwrap();
    let two = NonZeroU16::new(2).unwrap();
    /* 
    unsafe 2
    let one = NonZeroUsize::new(1).unwrap();
    let two = NonZeroUsize::new(2).unwrap();
    */
    /* 
    unsafe 3
    let one = NonZeroU32::new(1).unwrap();
    let two = NonZeroU32::new(2).unwrap();
    */
    /* 
    unsafe 4
    let one = NonZeroU128::new(1).unwrap();
    let two = NonZeroU128::new(2).unwrap();
    */
    /* 
    unsafe 5
    let one = NonZeroU64::new(1).unwrap();
    let two = NonZeroU64::new(2).unwrap();
    */
    /* 
    unsafe 6
    let one = NonZeroU8::new(1).unwrap();
    let two = NonZeroU8::new(2).unwrap();
    */
    
    assert_eq!(two, unsafe { one.unchecked_add(1) });


}

```
safe 1～6
```
#![allow(unused)]
#![feature(nonzero_ops)]
use std::num::NonZeroU16;

fn main() -> (){

    let one = NonZeroU16::new(1).unwrap();
    let two = NonZeroU16::new(2).unwrap();

    assert_eq!(Some(two), one.checked_add(1));


}
```


## unchecked_mul

unsafe 1～unsafe 12 都使用了 NonZero 类型： NonZeroI8、NonZeroI16、NonZeroI32、NonZeroI64、NonZeroI128、NonZeroIsize、NonZeroU8、NonZeroU16、NonZeroU32、NonZeroU64、NonZeroU128、NonZeroUsize

safe方式为使用 checked_mul 代替 unchecked_mul，返回一个 Option<NonZero···> 类型，操作数非零值返回 Some 包含结果的值、否则返回 None

unsafe 1
```
#![allow(unused)]
#![feature(nonzero_ops)]

use std::num::NonZeroI128;

fn main() -> () {
    let two = NonZeroI128::new(2).unwrap();
    let four = NonZeroI128::new(4).unwrap();

    assert_eq!(four, unsafe { two.unchecked_mul(two) });
}

```
safe 1
```
#![allow(unused)]
#![feature(nonzero_ops)]

use std::num::NonZeroI128;

fn main() -> () {
    let two = NonZeroI128::new(2).unwrap();
    let four = NonZeroI128::new(4).unwrap();
    assert_eq!(Some(four), two.checked_mul(two));
}

```

## offset
用于获取指针在偏移量处的新地址

按照修改方式14，23可分为两类

unsafe 1与unsafe 4

- unsafe 1: 指向**字符串**的**不可变指针**，然后使用offset直接访问内存中的字符串字符
  - safe 1: 将字符串转换Rc，然后使用deref和chars访问字符串的字符
- unsafe 4: 指向**数组**的**可变指针**，然后使用offset直接访问内存中的整数元素
  - safe 4: 将整数数组转换为Rc，然后使用deref和数组索引访问整数元素
unsafe 2与unsafe 3
- unsafe 2: 指向**数组**的**可变指针**，使用offset方法来计算它们之间的偏移量
  - safe 2: 使用了wrapping_offset确保它们之间的偏移量不会超出数组的边界
- unsafe 3: 指向**数组**的**不可变指针**，使用offset方法来计算它们之间的偏移量
  - safe 3：使用wrapping_offset确保它们之间的偏移量不会超出数组的边界。


unsafe 1
```
#![allow(unused)]
fn main() {
    let s: &str = "123";
    let ptr: *const u8 = s.as_ptr();

    unsafe {
        println!("{}", *ptr.offset(1) as char);
        println!("{}", *ptr.offset(2) as char);
    }
}
```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
fn main() {
    let s: &str = "123";

    let ptr2 = Rc::new(s);

    println!("{}",ptr2.deref().chars().nth(1).unwrap());
    println!("{}",ptr2.deref().chars().nth(2).unwrap());
}
```
unsafe 4
```
#![allow(unused)]
fn main() {
    let mut s = [1, 2, 3];
    let ptr: *mut u32 = s.as_mut_ptr();

    unsafe {
        println!("{}", *ptr.offset(1));
        println!("{}", *ptr.offset(2));
    }
}
```
safe 4
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
fn main() {
    let mut s = [1, 2, 3];

    let ptr2 = Rc::new(s);

    println!("{}",ptr2.deref()[1]);
    println!("{}",ptr2.deref()[2]);
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    let mut a = [0; 5];
    let ptr1: *mut i32 = &mut a[1];
    let ptr2: *mut i32 = &mut a[3];
    unsafe {
        assert_eq!(ptr1.offset(2), ptr2);
        assert_eq!(ptr2.offset(-2), ptr1);
    }
}
```
safe 2
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
use core::mem::size_of;
fn main() {
    let mut a = [0; 5];
    let ptr1: *mut i32 = &mut a[1];
    let ptr2: *mut i32 = &mut a[3];

    assert_eq!(ptr1.wrapping_offset(2), ptr2);
    assert_eq!(ptr2.wrapping_offset(-2), ptr1);


}
```
unsafe 3
```
#![allow(unused)]
fn main() {
    let a = [0; 5];
    let ptr1: *const i32 = &a[1];
    let ptr2: *const i32 = &a[3];
    unsafe {

        assert_eq!(ptr1.offset(2), ptr2);
        assert_eq!(ptr2.offset(-2), ptr1);
    }
}
```
safe 3
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
use core::mem::size_of;
fn main() {
    let a = [0; 5];

    let ptr1: *const i32 = &a[1];
    let ptr2: *const i32 = &a[3];

    assert_eq!(ptr1.wrapping_offset(2), ptr2);
    assert_eq!(ptr2.wrapping_offset(-2), ptr1);


}
```
## offset_from 
用于计算两个指针之间偏移量（unsafe因为它假设这两个指针来自同一块内存，并且第一个指针在第二个指针之前）

unsafe 1 2 3 4 
safe 方式使用 wrapping_sub 方法计算指针的偏移量，并且使用相除的方式来获取偏移量


unsafe 1
```
#![allow(unused)]
fn main() {
    let a = [0; 5];
    let ptr1: *const i32 = &a[1];
    let ptr2: *const i32 = &a[3];
    unsafe {
        assert_eq!(ptr2.offset_from(ptr1), 2);
        assert_eq!(ptr1.offset_from(ptr2), -2);
    }
}
```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
use core::mem::size_of;
fn main() {
    let a = [0; 5];
    // 将指针强制转换为 isize 类型，使用 wrapping_sub 
    // isize 类型是有符号的，可以避免溢出错误
    let ptr1: *const i32 = &a[1];
    let ptr2: *const i32 = &a[3];
    let diff1:isize = (ptr2 as isize).wrapping_sub(ptr1 as isize);
    let diff2:isize = (ptr1 as isize).wrapping_sub(ptr2 as isize);
    let size_of_i32 = size_of::<i32>() as isize;
    // 除以 i32 的大小来得到指针之间的距离
    assert_eq!(diff1/size_of_i32, 2);
    assert_eq!(diff2/size_of_i32, -2);


}
```
unsafe 3
```
#![allow(unused)]
fn main() {
    let mut a = [0; 5];
    let ptr1: *mut i32 = &mut a[1];
    let ptr2: *mut i32 = &mut a[3];
    unsafe {
        assert_eq!(ptr2.offset_from(ptr1), 2);
        assert_eq!(ptr1.offset_from(ptr2), -2);
    }
}
```
safe 3
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
use core::mem::size_of;
fn main() {
    let mut a = [0; 5];
    let ptr1: *mut i32 = &mut a[1];
    let ptr2: *mut i32 = &mut a[3];
    let diff1:isize = (ptr2 as isize).wrapping_sub(ptr1 as isize);
    let diff2:isize = (ptr1 as isize).wrapping_sub(ptr2 as isize);
    let size_of_i32 = size_of::<i32>() as isize;
    assert_eq!(diff1/size_of_i32, 2);
    assert_eq!(diff2/size_of_i32, -2);


}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    let ptr1 = Box::into_raw(Box::new(0u8)) as *const u8;
    let ptr2 = Box::into_raw(Box::new(1u8)) as *const u8;
    let diff = (ptr2 as isize).wrapping_sub(ptr1 as isize);
// Make ptr2_other an "alias" of ptr2, but derived from ptr1.
    let ptr2_other = (ptr1 as *const u8).wrapping_offset(diff);
    assert_eq!(ptr2 as usize, ptr2_other as usize);
// Since ptr2_other and ptr2 are derived from pointers to different objects,
// computing their offset is undefined behavior, even though
// they point to the same address!
    unsafe {
        let zero = ptr2_other.offset_from(ptr2); // Undefined Behavior
        println!("{:?}",ptr2_other.offset_from(ptr2));
    }
}
```
safe 2
```
#![allow(unused)]
fn main() {
    let ptr1 = Box::into_raw(Box::new(0u8)) as *const u8;
    let ptr2 = Box::into_raw(Box::new(1u8)) as *const u8;
    let diff = (ptr2 as isize).wrapping_sub(ptr1 as isize);
// Make ptr2_other an "alias" of ptr2, but derived from ptr1.
    let ptr2_other = (ptr1 as *const u8).wrapping_offset(diff);
    assert_eq!(ptr2 as usize, ptr2_other as usize);
// Since ptr2_other and ptr2 are derived from pointers to different objects,
// computing their offset is undefined behavior, even though
// they point to the same address!

    let zero = (ptr2_other as isize).wrapping_sub(ptr2 as isize);
    println!("{:?}",zero);
}
```
unsafe 4
```
#![allow(unused)]
fn main() {
    let ptr1 = Box::into_raw(Box::new(0u8));
    let ptr2 = Box::into_raw(Box::new(1u8));
    let diff = (ptr2 as isize).wrapping_sub(ptr1 as isize);
// Make ptr2_other an "alias" of ptr2, but derived from ptr1.
    let ptr2_other = (ptr1 as *mut u8).wrapping_offset(diff);
    assert_eq!(ptr2 as usize, ptr2_other as usize);
// Since ptr2_other and ptr2 are derived from pointers to different objects,
// computing their offset is undefined behavior, even though
// they point to the same address!
    unsafe {
        let zero = ptr2_other.offset_from(ptr2); // Undefined Behavior
        println!("{:?}",zero);
    }
}
```
safe 4
```
#![allow(unused)]
fn main() {
    let ptr1 = Box::into_raw(Box::new(0u8));
    let ptr2 = Box::into_raw(Box::new(1u8));
    let diff = (ptr2 as isize).wrapping_sub(ptr1 as isize);
// Make ptr2_other an "alias" of ptr2, but derived from ptr1.
    let ptr2_other = (ptr1 as *const u8).wrapping_offset(diff);
    assert_eq!(ptr2 as usize, ptr2_other as usize);
// Since ptr2_other and ptr2 are derived from pointers to different objects,
// computing their offset is undefined behavior, even though
// they point to the same address!

    let zero = (ptr2_other as isize).wrapping_sub(ptr2 as isize);
    println!("{:?}",zero);
}
```
## pointer_add
用于计算指针加上某个偏移量后的新指针

- unsafe 1 使用指针问**字符串**的字符
  - safe 使用 Rc然后deref() 并使用 chars().nth(i) 来访问第i个字符。
- unsafe 2 使用指针访问和修改**可变的数组**,使用pointer_add()，依次访问和修改所有元素
- unsafe 3 使用指针访问**不可变的数组**，使用pointer_add()和 get_unchecked() 来访问所有元素
  - 2 3的safe方式一致 为将不安全指针操作改为常规的数组访问方式

unsafe 1
```
#![allow(unused)]
fn main() {
    let s: &str = "123";
    let ptr: *const u8 = s.as_ptr();

    unsafe {
        println!("{}", *ptr.add(1) as char);
        println!("{}", *ptr.add(2) as char);
    }
}
```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
fn main() {
    let s: &str = "123";
    let mut i = 1;
    let ptr2 = Rc::new(s);

    println!("{}",ptr2.deref().chars().nth(i).unwrap());
    i+=1;
    println!("{}",ptr2.deref().chars().nth(i).unwrap());
    i+=1;
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    let x = &mut [1, 2, 4];
    let x_ptr = x.as_mut_ptr();

    unsafe {
        for i in 0..x.len() {
            *x_ptr.add(i) += 2;
        }
    }
    assert_eq!(x, &[3, 4, 6]);
}
```
safe 2
```
#![allow(unused)]

fn main() {
    let x = &mut [1, 2, 4];
    for i in 0..x.len() {
        x[i] += 2;
    }
    assert_eq!(x, &[3, 4, 6]);
}
```
unsafe 3
```
#![allow(unused)]
fn main() {
    let x = &[1, 2, 4];
    let x_ptr = x.as_ptr();
    // x.as_ptr() 方法返回了一个指向数组首个元素的指针

    unsafe {
        for i in 0..x.len() {
            assert_eq!(x.get_unchecked(i), &*x_ptr.add(i));
        }
    }
}
```
safe 3
```
#![allow(unused)]

fn main() {
    let x = &[1, 2, 4];

    for i in 0..x.len() {
    // x 的第 i 个元素与 解引用 x 指针后所得到的数组的第 i 个元素
        assert_eq!(x[i], (*x)[i]);
    }
}
```
## pointer_sub
ptr.sub(i)来获得一个指向前i个元素的新指针

- 与pointer_add unsafe 1 修改方式一致
  - safe方式为使用Rc引用计数类型和deref方法来访问字符串（将字符串s封装到一个引用计数类型的Rc对象中，使用deref()获得字符串的引用，接着使用chars()将字符串转换成字符迭代器，最后使用nth()来访问字符）

unsafe 1
```
#![allow(unused)]
fn main() {
    let s: &str = "123";

    unsafe {
        let end: *const u8 = s.as_ptr().add(3);
        println!("{}", *end.sub(1) as char);
        println!("{}", *end.sub(2) as char);
    }
}
```
safe 1
```
#![allow(unused)]
use std::rc::Rc;
use std::ops::Deref;
fn main() {
    let s: &str = "123";
    let ptr = Rc::new(s);
    let mut i = 3;
    i-=1;
    println!("{}", ptr.deref().chars().nth(i).unwrap());
    i-=1;
    println!("{}", ptr.deref().chars().nth(i).unwrap());

}
```

## pointer_as_mut
用于将一个指向不可变类型的指针转换为指向可变类型的指针

不同类型的指针
- unsafe 1针对**数组**
  - safe方式不再使用指针而是直接通过索引访问和修改数组元素
- unsafe 2针对**变量**
  - safe方式不再使用指针而是直接使用可变变量x修改它的值

unsafe 1
```
#![allow(unused)]
fn main() {
    let mut s = [1, 2, 3];
    let ptr: *mut u32 = s.as_mut_ptr();
    let first_value = unsafe { ptr.as_mut().unwrap() };
    *first_value = 4;
    assert_eq!(s, [4, 2, 3]);
    println!("{:?}", s); // It'll print: "[4, 2, 3]".
}
```
safe 1
```
#![allow(unused)]
fn main() {
    let mut s = [1, 2, 3];
    s[0]=4;
    assert_eq!(s, [4, 2, 3]);
    println!("{:?}", s); // It'll print: "[4, 2, 3]".
}
```
unsafe 2
```
#![allow(unused)]
fn main() {
    use std::ptr::NonNull;

    let mut x = 0u32;
    let mut ptr = NonNull::new(&mut x).expect("null pointer");

    let x_ref = unsafe { ptr.as_mut() };
    assert_eq!(*x_ref, 0);
    *x_ref += 2;
    assert_eq!(*x_ref, 2);
}
```
safe 2
```
#![allow(unused)]

fn main() {
    use std::ptr::NonNull;

    let mut x = 0u32;

    assert_eq!(x, 0);

    x += 2;
    assert_eq!(x, 2);
}
```

