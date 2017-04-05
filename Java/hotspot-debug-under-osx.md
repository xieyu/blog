## 在osx下编译调试hotspot

### 准备工作

1. 安装freetype

```bash
$brew install freetype
```

2. 获取openjdk repo代码

```bash
$git clone https://github.com/dmlloyd/openjdk.git
```

3. configure然后make slowdebug 版本, 开启``--with-native-debug-symbols=internal``选项以保留debug-symols

```bash
$bash ./configure  --with-target-bits=64 --with-freetype-include=/usr/X11/include/freetype2 --with-freetype-lib=/usr/X11/lib --disable-warnings-as-errors --with-debug-level=slowdebug  --with-native-debug-symbols=internal

$make
```

### GDB 调试
准备好HelloWorld.java, 然后用javac编译

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("hello,world");
    }
}
```

准备gdb 调试脚本, 这里面的file指向第一步编译好的java
```
$sudo gdb -x hello.gdb
```
里面的hello.gdb内容如下：

```
//hello.gdb
file /codes/openjdk/build/macosx-x86_64-normal-server-slowdebug/jdk/bin/java
handle SIGSEGV nostop noprint pass

# break points
break java.c:JavaMain
break InitializeJVM
break LoadJavaVM
break ContinueInNewThread

#in javaMain, after InitializeJVM
break java.c:477
commands
print "vm is"
print **vm
print "env is"
print **env
end

run HelloWorld
```

gdb脚本中的 break java.c:477 commands ... end 在到达断点的时候，会去执行commands中的命令，这样感觉非常方便~~. 在这边可以看到运行完InitializeJVM之后，vm和env这两个都初始化好了。

vm初始化之后是这样的, 绑定了几个函数指针, env中绑定的函数指针太多了，在此就不列举了。
```
{reserved0 = 0x0, reserved1 = 0x0, reserved2 = 0x0,
    DestroyJavaVM = 0x104939bb0,
    AttachCurrentThread = 0x104939e20,
    DetachCurrentThread = 0x10493a2d0,
    GetEnv = 0x10493a470,
    AttachCurrentThreadAsDaemon = 0x10493a770
```
gdb 调试在mac下会有些问题，libjvm这个so中的符号看不到，无法打断点，网上研究了不少时间，最后发现是osx sierra和gdb兼容性问题，最后搞了半天，感觉太麻烦了。只好放弃，改用lldb.

### lldb 调试

[lldb](https://developer.apple.com/library/content/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-basics.html)调试和gdb很类似. lldb类似的脚本如下, 感觉比gdb清晰些，但是也啰嗦了些~~。

由于lldb只有在进程跑起来的时候，才能加``process handle xxx``, 所以在main上加一个breakpoint，在那个时候把hanlde SIGSEGV这个加上，忽略SIGSEGV信号。 lldb中通过breakpoing command add 这个加断点的时候要执行的命令，以DONE作为结束。


```gdb
file /codes/openjdk/build/macosx-x86_64-normal-server-slowdebug/jdk/bin/java
settings set frame-format "frame #${frame.index}: ${line.file.basename}:${line.number}: ${function.name}\n"

#breakpoints
breakpoint set --name main
breakpoint command add
process handle SIGSEGV --notify false --pass true --stop false
continue
DONE

run HelloWorld
process handle SIGSEGV --notify false --pass true --stop false
```

通过下面命令执行lldb debug的脚本

```sh
$lldb -s helloworld.lldb
```
