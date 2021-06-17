import sys
import matplotlib.pyplot as plt
from random import randint
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk #NavigationToolbar2TkAgg
# 图像对象
f=None
WIDTH  = 60
HEIGHT = 40
# 全局变量
input = None
window = None
# 初始化已访问列表
def initVisitedList():
	visited = []
	for y in range(HEIGHT):
		line = []
		for x in range(WIDTH):
			line.append(False)
		visited.append(line)
	return visited

def drawLine(x1, y1, x2, y2):
	plt.plot([x1, x2], [y1, y2], color="black")

def removeLine(x1, y1, x2, y2):
	plt.plot([x1, x2], [y1, y2], color="white")
# 得到所有边
def get_edges(x, y):
	result = []
	result.append((x, y, x, y+1))
	result.append((x+1, y, x+1, y+1))
	result.append((x, y, x+1, y))
	result.append((x, y+1, x+1, y+1))

	return result
# 遍历邻边
def drawCell(x, y):
	edges = get_edges(x, y)
	for item in edges:
		drawLine(item[0], item[1], item[2], item[3])
# 获取两点之间相同的边
def getCommonEdge(cell1_x, cell1_y, cell2_x, cell2_y):
	edges1 = get_edges(cell1_x, cell1_y)
	edges2 = set(get_edges(cell2_x, cell2_y))
	for edge in edges1:
		if edge in edges2:
			return edge
	return None
# 初始化边表
def initEdgeList():
	edges = set()
	for x in range(WIDTH):
		for y in range(HEIGHT):
			cellEdges = get_edges(x, y)
			for edge in cellEdges:
				edges.add(edge)
	return edges
# 判断位置是否合法
def isValidPosition(x, y):
	if x < 0 or x >= WIDTH:
		return False
	elif y < 0 or y >= HEIGHT:
		return False
	else:
		return True
# 打乱两数组内数据顺序
def shuffle(dX, dY):
	for t in range(4):
		i = randint(0, 3)
		j = randint(0, 3)
		dX[i], dX[j] = dX[j], dX[i]
		dY[i], dY[j] = dY[j], dY[i]
# dfs
def DFS(X, Y, edgeList, visited):
	dX = [0,  0, -1, 1]
	dY = [-1, 1, 0,  0]
	shuffle(dX, dY)
	for i in range(len(dX)):
		nextX = X + dX[i]
		nextY = Y + dY[i]
		if isValidPosition(nextX, nextY):
			if not visited[nextY][nextX]:
				visited[nextY][nextX] = True
				commonEdge = getCommonEdge(X, Y, nextX, nextY)
				if commonEdge in edgeList:
					edgeList.remove(commonEdge)
				DFS(nextX, nextY, edgeList, visited)


def draw():
	# 清除之前的画线
	plt.clf()
	f = plt.figure(1)
	f1 = plt.subplot(111)
	plt.axis('equal')
	plt.title('Maze')
	edgeList = initEdgeList()
	visited = initVisitedList()
	DFS(0, 0, edgeList, visited)
	edgeList.remove((0, 0, 0, 1))
	edgeList.remove((WIDTH, HEIGHT - 1, WIDTH, HEIGHT))
	for edge in edgeList:
		drawLine(edge[0], edge[1], edge[2], edge[3])
	# plt.show()
	return f

def show():
	global input
	global window
	global HEIGHT
	global WIDTH

	try:
		WIDTH = int(input.get().split(',')[0])
		HEIGHT = int(input.get().split(',')[1])
	except Exception as e:
		tk.messagebox.showerror(title='error', message='你输入的格式有误，请检查格式')
		return
	if WIDTH <= 0 or HEIGHT <= 0:
		tk.messagebox.showerror(title='error', message='你输入的参数大小有误，请检查是否大于0')
		return

	mainFrame= tk.Frame(window)
	f = draw()
	canvas=FigureCanvasTkAgg(f,mainFrame)
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2Tk(canvas,
								   mainFrame)  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
	canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	toolbar.update()
	mainFrame.place(x=170,y=100)
def main():
	global f
	global input
	window = tk.Tk()
	window.title('迷宫生成大作业')
	window.iconbitmap('./bitbug_favicon.ico')
	window.geometry('1000x900')
	l = tk.Label(window, text='迷宫生成大作业', bg='green', fg='red', width=30, height=2).pack()
	tk.Label(window, text='请输入m,n,以逗号作为分隔符:', font=('Arial', 14)).place(x=0, y=35)
	# 获取输入
	input=tk.Entry(window, show=None)
	input.place(x=250,y=35)
	print(input.get())
	tk.Button(window, text='开始绘制',command=show).pack()


	window.mainloop()

if __name__=="__main__":
    main()
