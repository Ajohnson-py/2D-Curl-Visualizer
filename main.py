from ursina import *
from sympy import symbols, diff
from matplotlib import pyplot as plt
import numpy as np

formatted_field = ''


def draw_field():
    # graphs vector field
    x, y = np.meshgrid(np.linspace(-10, 10, 15),
                       np.linspace(-10, 10, 15))
    u = eval(formatted_field[0])
    v = eval(formatted_field[1])
    plt.quiver(x, y, u, v, color='c')
    # formats graph
    plt.style.use('dark_background')
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    ax = plt.gca()
    plt.grid(True)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))
    plt.savefig('new_xy_axis.png', bbox_inches='tight', dpi=700)


def format_field(vector_field):
    # the following code formats the user input so it can be graphed
    vector_field = vector_field.replace('^', '**').replace('x', '*(x)').replace('y', '*(y)').replace('sqrt', 'np.sqrt')

    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']  # used for comparison in 'while' loop
    index = 0
    while index < len(vector_field):
        if vector_field[index] == '*' and vector_field[index - 1] != '*' and vector_field[index - 1] != ')' and \
                vector_field[index - 1] not in numbers:
            vector_field = vector_field[:index] + vector_field[index + 1:]

        index += 1

    x_component, y_component = vector_field.split('i')
    y_component = y_component.replace('j', '')

    # the following if statement eliminates the '+' sign if there is one in the front
    if y_component[0] == '+':
        y_component = y_component[1:]

    return x_component, y_component


def on_submit():
    # when the submit button is pressed, this code formats the user input and displays the graph of the field
    global formatted_field
    global xy_axis
    formatted_field = format_field(input_field.text)
    draw_field()
    xy_axis.texture = "new_xy_axis.png"


def add_paddle_wheel():
    def rotate_paddles():
        x, y = symbols('x y')
        x_component = formatted_field[0]
        y_component = formatted_field[1]
        position = e.position
        x_position = position[0]
        y_position = position[1]

        # finds the partial derivative of the y component wrt x and the x component wrt y
        # then it evaluates them at where the paddle wheel is to find the curl
        ydx = diff(y_component, x)
        xdy = diff(x_component, y)
        ydx = ydx.subs([(x, x_position * 3.7037037037), (y, y_position * 3.7037037037)]) # the 3.7 will need to be updated depending on monitor resolution
        xdy = xdy.subs([(x, x_position * 3.7037037037), (y, y_position * 3.7037037037)]) # the 3.7 will need to be updated depending on monitor resolution
        print(ydx, xdy)
        # print(x_position * 3.7037037037, y_position * 3.7037037037)

        curl = ydx - xdy
        print(curl)
        e.rotation_z = e.rotation_z - (0.05 * curl)
        b.rotation_z = b.rotation_z - (0.05 * curl)

    def delete_paddle_wheel():
        # ran out of time to implement
        pass

    global formatted_field
    # e is the vertical part of the paddle wheel and b is the horizontal part
    e = Entity(model='quad', color=color.red, position=mouse.world_point, scale_x=0.1, scale_y=0.5,
               on_click=delete_paddle_wheel)
    b = Entity(model='quad', color=color.red, position=mouse.world_point, scale_x=0.1, scale_y=0.5,
               on_click=delete_paddle_wheel)
    b.rotation_z = 90

    e.update = rotate_paddles
    b.update = rotate_paddles


# Initiates app
app = Ursina()
Sky(texture=color.white)

window.borderless = False
window.fullscreen = True
window.exit_button.visible = False

'''
The following code is used to get the starting graph. Once you have it downloaded, this code
doesn't need to be run

plt.style.use('dark_background')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
ax = plt.gca()
plt.grid(True)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))
plt.savefig('starting_xy_axis.png', bbox_inches='tight', dpi=1000)
'''

submit_button = Button(text='submit', position=(0.4, -0.4), scale=0.1, on_click=on_submit)
enter_field_text = Entity(text='Enter a vector field:', position=(-0.4, -0.1), texture=color.black, scale=6)
input_field = InputField(position=(0, -0.4))
xy_axis = Entity(model='quad', scale=6, texture='starting_xy_axis.png', collider='box', on_click=add_paddle_wheel,
                 z=-0.5)

app.run()

