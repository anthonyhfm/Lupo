from lupo import *

window = Window()
window.set_size(300, 300)
window.set_title("Example Window")
window.set_resizable(False)

def test_print(text: str):
    print(f"{text}")


window.body = View(children=[
    Column(style=Style(gap=px(10)), children=[

        Row(style=Style(gap=px(10)), children=[
            Button("Test 1", Style(width=px(100), height=px(100)), onclick=lambda: test_print("You clicked Test 1")),
            Button("Test 2", Style(width=px(100), height=px(100)), onclick=lambda: test_print("You clicked Test 2")),
        ]),

        Row(style=Style(gap=px(10)), children=[
            Button("Test 3", Style(width=px(100), height=px(100)), onclick=lambda: test_print("You clicked Test 3")),
            Button("Test 4", Style(width=px(100), height=px(100)), onclick=lambda: test_print("You clicked Test 4")),
        ]),

    ])
])

window.open()