# Rust Ownership and Reference

## Ownership

Ownership 规则：同一时刻value只能被一个var所拥有，当var超过了它的作用域后，value将会被drop掉。

1. Each value in Rust has a variable that’s called its owner.
2. There can only be one owner at a time.
3. When the owner goes out of scope, the value will be dropped.

这里面的第三点很像c++中的析构函数, 第二点避免了资源被多次release的问题。

和Ownership相关的trait

* Copy
* Drop

函数传参默认是move或者copy.


## Reference

Reference 规则

1. At any given time, you can have either but not both tof ht following: one mutable ref or any number imuttable ref
2. reference must always validate

Mutable ref和Imuttable ref 和Write lock/read lock很相似，这样rust可以在编译器发现各种data race的问题, 达到所谓的fearless concurrency

### Borrow

#### 编译期 borrow checker

#### 运行期 borrow checker



## LifeTime


ref: 

1.[Basic of rust ownership](https://www.snoyman.com/blog/2018/10/rust-crash-course-02-basics-of-ownership) 
