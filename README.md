DebugProv
==========

DebugProv is an Algorithmic Debugger designed to locate defects in Python programs.  
Debugprov implements a technique called provenance enhancement to reduce the number of questions in the navigation phase of the algorithmic debugging session.  

Quick Installation
------------------

To install DebugProv, you should first set up a Python 3.7 environment.

The requirements for running DebugProv are: noWorkflow 2.0-alpha, graphviz, and prompt-toolkit.
 
To install noWorkflow 2.0-alpha, follow these basic instructions:
```bash
$ git clone git@github.com:gems-uff/noworkflow.git
$ cd noworkflow
$ git checkout 2.0-alpha
$ cd capture
$ python setup.py install
```
This installs noWorkflow 2.0-alpha.

To install the other dependencies, please do:
```bash
$ pip install graphviz
$ pip install prompt-toolkit
```

Basic Usage
-----------

To start an algorithmic debugging session of a defective Python program, you should run
```bash
$ debugprov program.py
```

To pass arguments to the program:
```bash
$ debugprov program.py first_arg second_arg 
```


License Terms
-------------

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
