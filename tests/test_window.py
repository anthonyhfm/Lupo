from lupo import *

window = Window()
window.set_size(256, 256)

window.body = View(children=[
    Column(style=Style(gap = px(10)), children=[
        Button("Test 1"),
        Button("Test 2"),
        Button("Test 3"),
        Button("Test 4"),
    ])
])

window.open()
