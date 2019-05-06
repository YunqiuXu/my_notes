# Install ViZDoom 1.1.8 compatibly with PyTorch 1.1.0 (no root)

+ General installation (clone repo, then run `pip install . ` directly) does not work, why?
    + The PyTorch installed via conda is compiled by gcc 4.9.2, while the default local compiler for ViZDoom is gcc 4.8.5. 
    + This may cause segmentation fault if you import PyTorch and ViZDoom together.
    + Reference: https://github.com/pytorch/pytorch/issues/7981\
+ So how to tackle it? 
    + There are two methods, one is to downgrade PyTorch to 0.3, here I will use another method.
    + Install new gcc, then compile ViZDoom from source, while PyTorch is unchanged.
    
    
+ Step 1: install new gcc
    + Here I follow https://blog.csdn.net/qq_20965753/article/details/64133013
    + Note that the version should be 4.9.2
+ Step 2: after installation, set path and variables in .zshrc (Here I install new gcc in folder "gcc_installed")
    + Note that "LD_PRELOAD" should be set beforehand, otherwise there will be error "GLIBCXX_3.4.20 not found"
    + Reference: https://blog.csdn.net/liningeasy/article/details/21476217

```
# In .zshrc, used when compiling with gcc 4.9.2
export PATH=/home/yunqxu/gcc_installed/bin:/home/yunqxu/gcc_installed/lib64:$PATH
export LD_LIBRARY_PATH=/home/yunqxu/gcc_installed/lib/
export LD_PRELOAD="/home/yunqxu/gcc_installed/lib64/libstdc++.so.6.0.20"
export CXX="/home/yunqxu/gcc_installed/bin/g++"
export CC="/home/yunqxu/gcc_installed/bin/gcc"
```

+ Step 3: clone the repo of ViZDoom, then modify `cmake_all.sh`

```
# In cmake_all.sh
cmake -DCMAKE_BUILD_TYPE=Release \
 -DBUILD_PYTHON=OFF \
 -DBUILD_PYTHON3=ON \
 -DPYTHON_EXECUTABLE=/home/yunqxu/anaconda3/bin/python \
 -DNUMPY_ROOT_DIR=/home/yunqxu/anaconda3/lib/python3.6/site-packages/numpy \
 -DNUMPY_LIBRARIES=/home/yunqxu/anaconda3/lib/python3.6/site-packages/numpy/lib \
 -DNUMPY_INCLUDES=/home/yunqxu/anaconda3/lib/python3.6/site-packages/numpy/core/include \
 -DBUILD_JAVA=OFF \
 -DBUILD_LUA=OFF
```

+ Step 4: compile
    + Note that if compilation failed, you should run `cmake_clean.sh` to clean old data
    
    
```
./cmake_all.sh
make -j32
pip install .
```

+ Now everything seems OK, enjoy!