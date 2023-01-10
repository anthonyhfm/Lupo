<div align="center">
  <a href="https://github.com/anthonyhfm/lupo">
    <img src="https://raw.githubusercontent.com/anthonyhfm/Lupo/master/lupo.svg">
  </a>
</div>

## Introduction
**Lupo** is an easy way to make good looking **Cross-Platform** User Interfaces for using Python.

## Support

- 🆗 &nbsp; MacOS _is Supported but not fully fleshed out_ **(more work in progress)**
- ❌️ &nbsp; Windows ***is currently not Supported***
- ❌️ &nbsp; Linux ***is currently not Supported***

## Installation

````
pip install lupo
````

## Simple Window using Lupo

```python
from lupo import *

window = Window()
window.set_size(300, 300)
window.set_title("Hello World!")
window.set_resizable(False) # Proper window resizing is not implemented in the current Version of Lupo (disable it for good)

window.body = View(children=[ # This is the Body of the Window with Views and Children
    
    Row(style=Style(gap=px(10)), children=[ # Creates a Row of Buttons with a 10 pixel Gap in between
        Button("Hello", Style(width=px(100), height=px(100))),
        Button("World", Style(width=px(100), height=px(100))),
    ]),
    
])

window.open()
```

If you want to help me building this Library, feel free to ***fork*** the repo and _contribute_
