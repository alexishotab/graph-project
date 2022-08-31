from tkinter import Tk, Canvas
from tkinter import *
import time
from PIL import Image, ImageTk


class BallsManager:

    def __init__(self, canvas):
        self.canvas = canvas
        self.balls = []
        self.selected_ball = None

    def ball_create(self, x, y):
        """
        Creates a ball (an instance of the Ball class) centered at the point with coordinates (х, y)
        """
        for ball in self.balls:
            if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < 2 \
                * ball.radius + 5:
                break
        else:
            ball = Ball(canvas, x, y)
            self.balls.append(ball)

        if not lines_manager.matrix:
            lines_manager.matrix = [[0]]
        else:
            for i in range(len(lines_manager.matrix)):
                lines_manager.matrix[i].append(0)
            lines_manager.matrix.append([0]
                    * len(lines_manager.matrix[-1]))
            
    def select_ball(self, x, y):
        """
        Selects the ball that contains the point with coordinates (х, y)
        """
        for ball in self.balls:
            if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < ball.radius:
                self.selected_ball = ball
                self.canvas.itemconfig(ball.id, fill='green', outline='red')
                break

    def delete_ball(self):
        """
        Deleting the ball and his lines
        """
        if self.selected_ball is not None:
            for ball in self.balls:
                if ball.id == self.selected_ball.id:
                    lines_manager.matrix.pop(ball.index)
                    for i in lines_manager.matrix:
                        i.pop(ball.index)

                    for i in range(len(lines_manager.lines) - 1, -1, -1):
                        if ball.index in lines_manager.ways[i]:
                            lines_manager.ways.pop(i)
                            canvas.delete(lines_manager.lines[i].id)
                            lines_manager.lines.pop(i)

                    for i in range(len(lines_manager.ways)):
                        if lines_manager.ways[i][0] > ball.index:
                            lines_manager.ways[i][0] -= 1
                        if lines_manager.ways[i][1] > ball.index:
                            lines_manager.ways[i][1] -= 1

                    ind = self.balls.index(ball)
                    self.canvas.delete(self.balls[ind].text)
                    self.canvas.delete(self.balls[ind].id)
                    self.balls.pop(ind)
                    self.selected_ball = None

                    for i in range(ind, len(self.balls)):
                        self.balls[i].index -= 1
                        self.canvas.itemconfig(self.balls[i].text, text=str(self.balls[i].index))
                    break


class Ball:

    def __init__(
        self,
        canvas,
        x,
        y,
        radius=50,
        fill_color='white',
        outline_color='orange',
        ):
        self.canvas = canvas

        self.x = x
        self.y = y
        self.radius = radius

        self.fill_color = fill_color
        self.outline_color = outline_color

        self.index = len(balls_manager.balls)
        self.id = self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.fill_color,
            outline=self.outline_color,
            width=self.radius // 10,
            )

        self.text = canvas.create_text(x, y,
                text=str(len(balls_manager.balls)), font='Verdana 20',
                fill='grey')

        
class LinesManager:

    def __init__(self, canvas):
        self.canvas = canvas
        self.lines = []
        self.ways = []
        self.matrix = []

    def line_create(
        self,
        x0,
        y0,
        x1,
        y1,
        index1,
        index2,
        ):
        """
        Creates a line between points with coordinates (х0, у0), (х1, у1)
        """
        way = [index1, index2]
        way.sort()
        if way not in self.ways and way[::-1] not in self.ways:
            self.lines.append(Line(self.canvas, x0, y0, x1, y1))
            self.ways.append(way)
            self.matrix[index1][index2] = 1
            self.matrix[index2][index1] = 1


class Line:

    def __init__(
        self,
        canvas,
        x0,
        y0,
        x1,
        y1,
        fill_color='grey',
        width=5,
        ):
        self.canvas = canvas

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        self.fill_color = fill_color
        self.width = width

        self.id = self.canvas.create_line(
            self.x0,
            self.y0,
            self.x1,
            self.y1,
            fill=self.fill_color,
            width=self.width,
            )


class DFSmanager:

    def __init__(self, canvas):
        self.massive = lines_manager.matrix
        self.spis = []
        self.ball = None
        self.line = None
        self.previous = None
        self.canvas = canvas
        self.flag = False
        self.timing = 400

    def printing(self):
        """
        printing a massive in console
        """
        self.massive = []
        for i in lines_manager.matrix:
            self.massive.append(i)
        print ('[')
        for i in self.massive:
            print (i, ',')
        print (']')

    def dfs(
        self,
        visited,
        graph,
        node,
        ):
        """
        main DFS-algorithm with color change and printing points in console
        """
        if node not in visited:
            ballNumb = int(node)
            self.previous = self.ball
            self.ball = balls_manager.balls[ballNumb].id
            self.canvas.after(int(self.timing),
                              self.canvas.itemconfig(self.ball,
                              fill='yellow'))
            tk.update()
            print (node)
            self.spis.append(node)
            visited.add(node)
            self.canvas.itemconfig(self.line, fill='grey')
            tk.update()
            for neighbour in graph[node]:
                if self.flag == True:
                    self.canvas.itemconfig(self.previous, fill='White')
                    self.flag = False
                    tk.update()
                self.canvas.itemconfig(self.line, fill='grey')
                tk.update()
                ballNumb = int(neighbour)
                way = [int(node), ballNumb]
                way.sort()
                index = lines_manager.ways.index(way)
                self.line = lines_manager.lines[index].id
                self.canvas.after(int(self.timing * 2.5),
                                  self.canvas.itemconfig(self.line,
                                  fill='red'))
                self.ball = balls_manager.balls[ballNumb].id
                tk.update()
                self.dfs(visited, graph, neighbour)
            self.flag = True
            self.canvas.itemconfig(self.ball, fill='white')
            self.canvas.itemconfig(self.line, fill='grey')
            tk.update()
        else:
            ballNumb = int(node)
            self.ball = balls_manager.balls[ballNumb].id
            self.canvas.itemconfig(self.ball, fill='red')
            tk.update()
            self.canvas.after(int(self.timing),
                              self.canvas.itemconfig(self.ball,
                              fill='white'))
            tk.update()

    def dfsdestroyer(self):
        """
        change the colors of the graph into the starting position
        """
        for b in balls_manager.balls:
            self.ball = b.id
            self.canvas.itemconfig(self.ball, fill='white')
            tk.update()
        for l in lines_manager.lines:
            self.line = l.id
            self.canvas.itemconfig(self.line, fill='grey')
            tk.update()

    def deliting(self):
        """
        clear the screen and deleting graph
        """
        self.canvas.delete('all')
        balls_manager.balls = []
        lines_manager.lines = []
        lines_manager.ways = []
        lines_manager.matrix = []
        depth_manager.spis = []

    def usingDFS(self):
        """
        The function coordinates the work of the class
        """
        self.printing()
        inputmassive = self.massive[:]
        matrix2 = []
        cnt2 = 0
        for i in range(len(inputmassive)):
            ab = [cnt2]
            for j in range(len(inputmassive[i])):
                if inputmassive[i][j] == 1:
                    ab.append(str(j))
            matrix2.append(ab)
            cnt2 += 1
        visited = set()
        graph = {}
        self.spis = []
        a = str(startInput.get())
        for x in range(len(matrix2)):
            graph[str(matrix2[x][0])] = (matrix2[x])[1:]
        self.dfs(visited, graph, a)
        self.dfsdestroyer()
        Output.delete(0, END)
        Output.insert(0, self.spis)
        print (self.spis)

    def OnScale(self):
        """
        assigns a value from the scale to the operating speed parameter
        """
        self.timing = s1.get()


class Theme:

    def __init__(self, canvas, fill_color='White'):
        self.canvas = canvas
        self.fillc = fill_color

    def White_theme(self):
        """
        full changing theme to white
        """
        self.fill_c = 'White'
        self.canvas.configure(bg=self.fill_c)
        inscription['bg'] = 'White'
        inscription['foreground'] = 'Black'
        s1['bg'] = 'white'
        s1['foreground'] = 'Black'
        s1['highlightbackground'] = 'white'

    def Black_theme(self):
        """
        full changing theme to black
        """
        self.fill_c = 'Black'
        self.canvas.configure(bg=self.fill_c)
        inscription['bg'] = 'Black'
        inscription['foreground'] = 'white'
        s1['bg'] = 'black'
        s1['foreground'] = 'white'
        s1['highlightbackground'] = 'black'

    def close(self):
        """
        closing window
        """
        tk.destroy()

    def okey(self):
        """
        button 'okey' destroyer
        """
        btnOk.destroy()
        lab.destroy()
#comment out in case [Error 2]
    def Borzuha(self):
        """
        surprise fun function, starting with button 'help'
        """
        imag = Image.open('borzuha.jpg')
        photo = ImageTk.PhotoImage(imag)
        image = self.canvas.create_image(650, 500, anchor='center',
                image=photo)
        tk.update()
        time.sleep(4)
        canvas.delete(image)
        tk.update()
#end of comment

def click(x, y):
    """
    Handles a click: selects the ball, or draws a line between the new one and the one already selected, or builds a new ball
    """
    for ball in balls_manager.balls:
        if ((ball.x - x) ** 2 + (ball.y - y) ** 2) ** 0.5 < ball.radius:
            if balls_manager.selected_ball is None:
                balls_manager.select_ball(x, y)
            else:
                lines_manager.line_create(
                    balls_manager.selected_ball.x,
                    balls_manager.selected_ball.y,
                    ball.x,
                    ball.y,
                    balls_manager.selected_ball.index,
                    ball.index,
                    )
                canvas.itemconfig(balls_manager.selected_ball.id,
                                  fill=balls_manager.selected_ball.fill_color,
                                  outline=balls_manager.selected_ball.outline_color)
                balls_manager.selected_ball = None
            break
    else:
        if (x >= 1150 or x <= 80) and y <= 700:
            pass
        else:
            balls_manager.ball_create(x, y)
            
massive = []
tk = Tk()
tk.title('GraphoMania')
tk.resizable(0, 0)
canvas = Canvas(tk, width=1300, height=1000)
canvas.configure(bg='White')
canvas.pack()
#comment out in case [Error 2]
imag=Image.open('splashscreen.png')
photo=ImageTk.PhotoImage(imag)
ba=canvas.create_image(650, 500, anchor='center', image=photo)
tk.update()
time.sleep(3)
canvas.delete(ba)
imag=Image.open('splashscreen2.png')
photo=ImageTk.PhotoImage(imag)
ba=canvas.create_image(650,500,anchor='center',image=photo)
tk.update()
time.sleep(3)
canvas.delete(ba)
#end of comment

#classes
balls_manager = BallsManager(canvas)
lines_manager = LinesManager(canvas)
depth_manager = DFSmanager(canvas)
theme_manager = Theme(canvas)

#creating buttons
tk.bind('<Double-Button-1>', lambda event: click(event.x, event.y))
tk.bind("<Button-3>", lambda event: balls_manager.delete_ball())

btn = Button(text='Print Matrix', bg='pale green', font=('Roboto', 13),
             command=depth_manager.printing)
btn.place(x=1210, y=240, width=100, height=40)
startInput = Entry(font=('Roboto', 13), bd=5, justify=CENTER)
startInput.place(x=1210, y=120, width=100, height=40)
inscription = \
    Label(text='Т. Отсчета:'
          , font=('Roboto', 15), bg='White', foreground='Black')
inscription.place(x=1100, y=120, width=110, height=40)
Output = Entry(font=('Roboto', 13), bd=5, justify=CENTER)
Output.place(x=1010, y=0, width=200, height=40)
btnDFS = Button(text='DFS graph:', bg='pale green', font=('Roboto',
                13), command=depth_manager.usingDFS)
btnDFS.place(x=1210, y=40, width=100, height=80)
btndestroy = \
    Button(text='Очистка графа'
           , bg='red', font=('Roboto', 9), justify=CENTER,
           command=depth_manager.deliting)
btndestroy.place(x=1210, y=160, width=100, height=80)
btnclose = \
    Button(text='Закрыть окно'
           , bg='red', font=('Roboto', 9), justify=CENTER,
           command=theme_manager.close)
btnclose.place(x=1210, y=0, width=100, height=40)
lab = \
    Label(text='Темы в верхнем левом углу. 2-ой щелчек - new point. ПКМ - delete'
          , font=('Roboto', 20), bg='White')
lab.place(x=10, y=10, width=850, height=80)
btnOk = Button(text='Понял!',
               bg='pale green', font=('Roboto', 20),
               command=theme_manager.okey)
btnOk.place(x=860, y=10, width=100, height=80)
v1 = DoubleVar()
s1 = Scale(
    variable=v1,
    from_=200,
    to=2000,
    orient=VERTICAL,
    bg='White',
    trough='orange',
    highlightbackground='white',
    label='delay',
    )
s1.place(x=1215, y=280, width=100, height=300)
btnScale = \
    Button(text='Ввод значения'
           , bg='pale green', font=('Roboto', 9),
           command=depth_manager.OnScale)
btnScale.place(x=1200, y=585, width=100, height=40)
#comment out in case [Error 2]
Sovet = \
    Button(text='Подсказка'
           , bg='red', font=('Roboto', 10),
           command=theme_manager.Borzuha)
Sovet.place(x=1200, y=625, width=100, height=40)
#end of comment
#creating Menu of program
mainmenu = Menu(tk)
tk.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0, font=('Roboto', 20))
filemenu.add_command(label='Темная тема'
                     , command=lambda : theme_manager.Black_theme())
filemenu.add_separator()
filemenu.add_command(label='Светлая тема'
                     , command=lambda : theme_manager.White_theme())
filemenu.add_separator()
mainmenu.add_cascade(label='Тема страницы'
                     , menu=filemenu)

tk.mainloop()
