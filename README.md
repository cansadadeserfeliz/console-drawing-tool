# Coding challenge

## Drawing tool

You're given the task of writing a simple drawing tool. In a nutshell, the program reads the
`input.txt`, executes a set of commands from the file, step by step, and produces
`output.txt`.

At this time, the functionality of the program is quite limited but this might change in the future.
At the moment, the program should support the following set of commands:

C w h
    Create Canvas: Should create a new canvas of width w and height h.
L x1 y1 x2 y2
    Create Line: Should create a new line from (x1,y1) to (x2,y2). Currently
    only horizontal or vertical lines are supported. Horizontal and vertical
    lines will be drawn using the 'x' character.
R x1 y1 x2 y2
    Create Rectangle: Should create a new rectangle, whose upper left
    corner is (x1,y1) and lower right corner is (x2,y2). Horizontal and vertical
    lines will be drawn using the 'x' character.
B x y c
    Bucket Fill: Should fill the entire area connected to (x,y) with "colour" c.
    The behaviour of this is the same as that of the "bucket fill" tool in paint
    programs.

Please take into account that you can only draw if a canvas has been created.
