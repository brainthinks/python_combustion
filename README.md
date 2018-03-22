# Python Script for Combustion Library

In short, `combustion` allows you to convert the retail Halo PC map files into Halo CE map files.  If you paid for the retail Halo PC game, and want to the play the single player campaign using the updated Halo CE engine (and its extensions and mods, which are awesome), you either need to pirate the map files or convert them yourself from the map files that you legally own.  While pirating the map files is possible, I don't endorse that, not so much for legal reasons, but because you don't necessarily have any control over how those single player maps were created, and don't know what additional code, malicious or otherwise, they contain.  I don't pretend to know what `combustion` and `tritium` do, but I have the option of learning Rust and auditing the code myself.  If you download the converted map files from halomods, you don't have that option.

This script will utilize the `combustion` library, written in Rust, that allows a Halo PC map to be converted to a map that Halo CE can use.

I wrote this because the Combustion utility was written for Windows, and is not cli-friendly.  I want to be able to automate the conversion of all of my Halo maps, which is what this script was made to do.


## Use

Since I am not an experienced Python developer, this script loads the files into memory before doing any processing on them.  This means that until someone submits a pull request to make this script more efficient, or until I become more proficient in Python, you are required to have a few gigs of free memory to convert any map files.  I recommend at least 2 gigs of free memory.  I pulled this number out of almost thin air, so if you know that more memory is needed, please submit a pull request for this readme.


### `examples/convert_all_retail_maps.sh`

The all-inclusive script.  This will install and download all of the dependencies needed to use `pycombustion`, then convert all of your maps.  Here is an example of running it:

`./examples/convert_all_retail_maps.sh "/home/user/PlayOnLinux's virtual drives/halo_ce_new/drive_c"`


### `examples/convert_all_retail_maps.py`

A basic script that will utilize the `pycombustion` package.  It is intended for you to modify as needed, if needed.


### `src/pycombustion/combustion.py`

This file contains the bindings that make it easier to interact with the Combustion library.  If you know what you're doing, you can call `convert_map` or even `_convert_map` yourself.


### `src/pycombustion/combustion.h`

You'll only need this file if you're doing something custom.  This is the C header file that defines the interface for the functions that the Combustion library exposes.  This should probably be a part of the Combustion project, but for now, it will live here.


## Lessons Learned

As a javascript developer, almost every aspect of this was new to me.  Rust, Python, C, libraries...  I had to understand what a library was, I had to understand how to make two different programming languages talk to each other, I had to learn that C was the bridge between them, I had to learn that a library was the infrastructure that made that bridge possible, I had to learn that a dynamic library was the required implementation of a library for an interpreted language like Python, I had to learn that Rust was created with the ability to do this in mind... I also had to become familiary with buffers and total length, which is not something I typically have to worry about in javascript-land.  Most things are dynamic, and streams can be avoided for medium-sized projects.

I was able to figure out almost every issue I ran into on my own.  Here were the issues of note:

### Vectors

When trying to compile Tritium, I got a few compilation errors.  They told me that "append" wasn't an available method on a particular variable.  After much guesswork and experimentation, I was able to determine that "append" is a `Vector` method, so I tried changing the `array` declarations to `Vector` declarations, and I got lucky - it worked.  The only reason that I was able to make the connection was a) by reading the rust docs and seeing what had an "append" method and b) my Java class from college back in 2005, where I was told that Vectors are basically arrays that don't require their sizes up front.

### FFI

When trying to create the python wrapper for this rust library, there was a host of issues I ran into.  Before I get into them, it is worth noting that the concept of using a C-compatible compiled library has a name - Foreign Function Interface, or the more common initialism of FFI.  Also, thanks to the generouse folks on the Rust Discord channel, I learned about the concept of "calling convention".  I can't define that term, but I know it's important, and it has to do with the way Python "calls" the Rust library function.

First, I had to create the library as a dynamic library rather than static to be able to use it in an interpreted (rather than compiled) language such as Python.  Beyond that statement, I can't really speak more to it.  Static libraries are for compiled languages, and dynamic libraries are used at runtime, which means they will work with interpreted languages, such as Python, Ruby, javascript, etc.  I think this is correct, but I can't confirm that.

Once I knew that, I was able to compile the "Combustion" project as a "dylib" in Rust terms, and subsequently I was able to import it into my Python script.  Thankfully, Python's documentation is excellent (which is one of the reasons I chose it), and I didn't have to look too hard to find `ctypes`, which is one method of importing and using a compiled dynamic library.

After reading a few examples and what I considered to be the relevant parts of the documentation, I was well on my way to creating a Python script that could convert Halo PC maps to Halo CE maps.  I modified the (thankfully well written) combustion library source code to demonstrate that I was passing things correctly when I came upon a strange error.  Every other argument that is passed to the library's `convert_map_cd` method is of type `usize`, which from what I read is supposed to indicate the number of bytes that exist in the buffer (each buffer, from what I understand, represents a file).  I created some "fake" buffers based on the `ctypes` documentation, and despite not haviing any runtime panics, I found that when I printed the argument values to stdout using `println!`, some of them were not correct.  I never found a consistent way to replicate the "garbage" argument values, but I was able to narrow it down to the first 6 arguments.  Any argument after the sixth was garbage.  I still do not know why.

### CFFI

After getting some help on the Rust Discord channel, I was able to find a helpful article by using the search term "calling convention".  I did a quick experiment using the `cffi` module that was promoted in that article, and found immediately that the argument garbage problem was no longer an issue.  I still do not know what caused this problem with `ctypes`, so if you know, please submit a pull request.

With `cffi` implemented, I was able to submit the proper arguments to the library function, as well as have the benefit of basic argument type validation, using `ffi.cdef`.

However, the hardest part was still to come.  After a bit of trial and error and research, I was able to get file buffer reads to work.  Here is an extracted example:

```python
map_data_file = open(source_map_path, 'rb')
map_data_len = os.fstat(map_data_file.fileno()).st_size
map_data_raw = ffi.from_buffer(map_data_file.read(map_data_len))
```

I open the binary file buffer, which allows me to determine the length of the file and get the FFI C-compatible buffer.  Not a problem.  Getting a write buffer to work was a differnet story, however.  Getting a write buffer working was a story that was 8 straight hours in the making.  Special shoutout to Python Discord helper `lucy/looselystyled#7626`, whose help allowed me to write the converted map files to disk.  Thank you again :)

Here is the binary file buffer pointer example that is needed to get the library to mutate a buffer pointer:

```python
buffer_file = open(target_map_path, 'rb+')
buffer_len = 1000000000
buffer_raw = ffi.new("char[]", buffer_len)
buffer_pointer = ffi.addressof(buffer_raw)
```

And with that, the rest of the script writing was business as usual...


### Python Conventions

I'm positive that it's just my lack of experience, but I found Python best practices hard to find.  For instance, I didn't find the "source of truth" for how to properly document Python code.  It seems that `pydoc` is the tool of choice for generating documentation, but what documentation does `pydoc` look for?  I didn't spend a whole lot of time on it, but it didn't come up as quickly in google as I'm used to.  I decided instead that I would use a popular Python library to give me some guidance into how to write "good" Python package code.  I decided to use `nvbn/thefuck`, as it is the fourth most popular Python project on github, and probably less scary than `tensorflow`.  Here are some of my own personal notes:

* using `import` statements at the top of the file does not result in "side-effects"
* you can import relative files by appending to `sys.path` - see the examples folder


## Credits

* `Halogen002` - without your excellent work, I would not have been able to use Halo in Linux on my terms, let alone create this wrapper script!
* Rust Discord channel members - without your help, I may have given up...
    * `<'a, 't, 's: 't> oberien<'a, 't>`
    * `#[macro_use(Restioson)]`
    * `Slikrick`
* Python Discord channel member `lucy/looselystyled#7626` - withouth your help, I absolutely would have given up!  I am in your debt.


## References
* [https://opencarnage.net/index.php?/topic/4680-combustion-203/](https://opencarnage.net/index.php?/topic/4680-combustion-203/)
* [https://www.todayifoundout.com/index.php/2012/05/the-difference-between-an-acronym-and-an-initialism/](https://www.todayifoundout.com/index.php/2012/05/the-difference-between-an-acronym-and-an-initialism/)
* [https://www.reddit.com/r/rust/comments/5rrybx/discord_server_for_rust/](https://www.reddit.com/r/rust/comments/5rrybx/discord_server_for_rust/)
* [https://bheisler.github.io/post/calling-rust-in-python/](https://bheisler.github.io/post/calling-rust-in-python/)
* [http://cffi.readthedocs.io/en/latest/ref.html#ffi-buffer-ffi-from-buffer](http://cffi.readthedocs.io/en/latest/ref.html#ffi-buffer-ffi-from-buffer)
* [https://tentacles666.wordpress.com/2013/12/04/python-ctypes-efficiently-writing-binary-data/](https://tentacles666.wordpress.com/2013/12/04/python-ctypes-efficiently-writing-binary-data/)


## @todo

* detect rust prior to trying to install it
* should the header file exist in the combustion project?  Is there a best practice for generating a c header file from `pub unsafe extern "C"`?
* is there a way to create a buffer/pointer where I do not have to pre-allocate the size?
* implement seamine - [https://opencarnage.net/index.php?/topic/6034-sea-mine/](https://opencarnage.net/index.php?/topic/6034-sea-mine/)
* where is the documentation for writing documentation that can be understood by pydoc?
* what is the best practice for creating a package?  should I use `if __name__ == "__main__"`?
* write this in javascript using `node-ffi`
