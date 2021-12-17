#encoding=utf8

#-импортируем библиотеки----------------------------------------------------------------------------
from Tkinter import *
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import OpenOPC
import sys
import json
#----------------------------------------------------------------------------------------------------

#-кодировка------------------------------------------------------------------------------------------
reload(sys)
sys.setdefaultencoding('utf8')
#----------------------------------------------------------------------------------------------------

#-Загружаем стиль фигуры-----------------------------------------------------------------------------
#plt.style.use('seaborn-whitegrid')
#----------------------------------------------------------------------------------------------------

#-Создаем главную окно ------------------------------------------------------------------------------
#Читать значение по умолчание -----------------------------------------------------------------------
"""
try:
	with open('term1.json', 'r') as f:
		tmpl_error = json.load(f)
	if tmpl_error != '':
		term1_nb = tmpl_error[0].split(",")
		term1_ns = tmpl_error[1].split(",")
		term1_ze = tmpl_error[2].split(",")
		term1_ps = tmpl_error[3].split(",")
		term1_pb = tmpl_error[4].split(",")
	else:
		term1_nb = [-3, -3, -1.5]
		term1_ns = [-3, -1.5, 0]
		term1_ze  = [-1.5, 0, 1.5]
		term1_ps = [0, 1.5, 3]
		term1_pb = [1.5, 3, 3]
	f.close()
except Exception:
	term1_nb = [-3, -3, -1.5]
	term1_ns = [-3, -1.5, 0]
	term1_ze  = [-1.5, 0, 1.5]
	term1_ps = [0, 1.5, 3]
	term1_pb = [1.5, 3, 3]

try:
	with open('term2.json', 'r') as f:
		tmpl_delta = json.load(f)
	if tmpl_delta != '':
		term2_nb = tmpl_error[0].split(",")
		term2_ns = tmpl_error[1].split(",")
		term2_ze = tmpl_error[2].split(",")
		term2_ps = tmpl_error[3].split(",")
		term2_pb = tmpl_error[4].split(",")
	else:
		term2_nb = [-3, -3, -1.5]
		term2_ns = [-3, -1.5, 0]
		term2_ze  = [-1.5, 0, 1.5]
		term2_ps = [0, 1.5, 3]
		term2_pb = [1.5, 3, 3]
	f.close()
except Exception:
	term2_nb = [-3, -3, -1.5]
	term2_ns = [-3, -1.5, 0]
	term2_ze  = [-1.5, 0, 1.5]
	term2_ps = [0, 1.5, 3]
	term2_pb = [1.5, 3, 3]

try:
	with open('term3.json', 'r') as f:
		tmpl_output = json.load(f)
	if tmpl_output != '':
		term3_nb = tmpl_output[0].split(",")
		term3_ns = tmpl_output[1].split(",")
		term3_ze = tmpl_output[2].split(",")
		term3_ps = tmpl_output[3].split(",")
		term3_pb = tmpl_output[4].split(",")
	else:
		term3_nb = [-1, -1, -0.5]
		term3_ns = [-1, -0.5, 0]
		term3_ze  = [-0.5, 0, 0.5]
		term3_ps = [0, 0.5, 1]
		term3_pb = [0.5, 1, 1]
	f.close()
except Exception:
	term3_nb = [-1, -1, -0.5]
	term3_ns = [-1, -0.5, 0]
	term3_ze  = [-0.5, 0, 0.5]
	term3_ps = [0, 0.5, 1]
	term3_pb = [0.5, 1, 1]

#----------------------------------------------------------------------------------------------------
"""


root = Tk()
#Cоздаем глобальный переменные-----------------------------------------------------------------------
tmpr_error = []


term2_nb = [-3, -3, -1.5]
term2_ns = [-3, -1.5, 0]
term2_ze  = [-1.5, 0, 1.5]
term2_ps = [0, 1.5, 3]
term2_pb = [1.5, 3, 3]

term3_nb = [-1, -1, -0.5]
term3_ns = [-1, -0.5, 0]
term3_ze  = [-0.5, 0, 0.5]
term3_ps = [0, 0.5, 1]
term3_pb = [0.5, 1, 1]

width = 600
height = 600
# ширина экрана
wscreen = root.winfo_screenwidth()
# высота экрана
hscreen = root.winfo_screenheight()

cntr_screenW = (wscreen - width) // 2
cntr_screenH = (hscreen - height) // 2
#----------------------------------------------------------------------------------------------------

#-Функции для Subform--------------------------------------------------------------------------------

#Закрываем  вспомогательные окна и открываем главное окно--------------------------------------------
def closeSubForm(subForm):
    subForm.destroy()
    root.update()
    root.deiconify()
#----------------------------------------------------------------------------------------------------

#Скрываем от вида главное окно пока открыто вспомогательное окно ------------------------------------
def hideMainForm():
    root.withdraw()
#----------------------------------------------------------------------------------------------------

#-Окно настройки температры -------------------------------------------------------------------------
def first_inp_widget():
	hideMainForm()
	first_inp_form = Toplevel()
	first_inp_form.geometry('{}x{}+{}+{}'.format(width, height, cntr_screenW, cntr_screenH))
	first_inp_form.title('Настройка терма рассогласавания')
	term1_nb = [-3, -3, -1.5]
	term1_ns = [-3, -1.5, 0]
	term1_ze  = [-1.5, 0, 1.5]
	term1_ps = [0, 1.5, 3]
	term1_pb = [1.5, 3, 3]

#Функции --------------------------------------------------------------------------------------------

	def update_first_setting():
		del tmpr_error[:]
		tmp = [i for i in range(5)]
		tmp[0] = entry_0.get()
		tmp[1] = entry_1.get()
		tmp[2] = entry_2.get()
		tmp[3] = entry_3.get()
		tmp[4] = entry_4.get()
		for i in range(len(tmp)):
			templ = cleanList1(tmp[i])
			tmpr_error.append(templ)
		drawFigure1(tmpr_error)


	def cleanList1(tmp):
		lst=list(tmp)
		lst.pop(0)
		lst.pop(-1)
		lst="".join(lst)
		lst = lst.split(",")
		lst = [float(i) for i in lst]
		return lst

	def drawFigure1(lst=None):
		print(type(lst))
		print lst
		if lst != None:
			error_nb = lst[0]
			error_ns = lst[1]
			error_ze = lst[2]
			error_ps = lst[3]
			error_pb = lst[4]

		print("I am Drawing")
		print( term1_nb)
		error_x = np.linspace(-3, 3, 5)
		error_nb = fuzz.trimf(error_x, term1_nb)
		error_ns = fuzz.trimf(error_x, term1_ns)
		error_ze = fuzz.trimf(error_x, term1_ze)
		error_ps = fuzz.trimf(error_x, term1_ps)
		error_pb = fuzz.trimf(error_x, term1_pb)

		first_picture.plot(error_x, error_nb, label='NB')
		first_picture.plot(error_x, error_ns, label='NS')
		first_picture.plot(error_x, error_ze, label='NE')
		first_picture.plot(error_x, error_ps, label='PS')
		first_picture.plot(error_x, error_pb, label='PB')
		first_picture.grid()
		first_picture.legend(frameon=False)
		first_picture.set_xlim(-3,3)
		first_picture.set_ylim(0,1)
		first_picture.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.)





#----------------------------------------------------------------------------------------------------
#-Фигура --------------------------------------------------------------------------------------------
	first_inp_form.resizable(False,False)
	first_figure = Figure(figsize=(3, 3), dpi=100)
	first_canvas = FigureCanvasTkAgg(first_figure, master=first_inp_form)
	first_canvas.draw()
	toolbar = NavigationToolbar2Tk(first_canvas, first_inp_form)
	toolbar.update()
	toolbar.pack(side=TOP, fill=X, padx=4)
	first_picture = first_figure.add_subplot(111)
	drawFigure1()
	print("call me ")
	first_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=5)
	first_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx=5)

#-Главная фрейм---------------------------------------------------------------------------------------
	first_frame = LabelFrame(first_inp_form, height =200, text='Настройка термов')
	#-Вверхный фрейм ---------------------------------------------------------------------------------
	top_frame_1 = Frame(first_frame, height =100)

	label_0    = Label(top_frame_1, width = 10, text='NB(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_1    = Label(top_frame_1, width = 10, text='NS(x1,x2,x3)').grid(row=1, column=3, padx=5)
	label_2    = Label(top_frame_1, width = 10, text='ZE(x1,x2,x3)').grid(row=1, column=5, padx=5)

	entry_0    = Entry(top_frame_1, width = 10, font=14)
	entry_1    = Entry(top_frame_1, width = 10, font=14)
	entry_2    = Entry(top_frame_1, width = 10, font=14)

	entry_0.insert(0, term1_nb)
	entry_1.insert(0, term1_ns)
	entry_2.insert(0, term1_ze)


	entry_0.grid(row=1, column=2)
	entry_1.grid(row=1, column=4)
	entry_2.grid(row=1, column=6)

	top_frame_1.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	#-Нижный фрейм------------------------------------------------------------------------------------
	bottom_frame_1 = Frame(first_frame, height =100)

	label_3   = Label(bottom_frame_1,  width = 10, text='PS(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_4   = Label(bottom_frame_1,  width = 10, text='PB(x1,x2,x3)').grid(row=1, column=3, padx=5)

	entry_3   = Entry(bottom_frame_1,  width = 10, font=14)
	entry_4   = Entry(bottom_frame_1,  width = 10, font=14)

	entry_3.insert(0, term1_ps)
	entry_4.insert(0, term1_pb)

	entry_3.grid(row=1, column=2)
	entry_4.grid(row=1, column=4)

	bottom_frame_1.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	#Кнопки управления -------------------------------------------------------------------------------
	term_btn_1 = Button(first_frame, width = 10, text ='ОК')
	term_btn_1.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_2 = Button(first_frame, width = 10, text ='Отмена', command = lambda:closeSubForm(first_inp_form))
	term_btn_2.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_3 = Button(first_frame, width = 10, text = 'Обновить', command=update_first_setting)
	term_btn_3.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	first_frame.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=10)

	first_inp_form.protocol('WM_DELETE_WINDOW', lambda: closeSubForm(first_inp_form))
#-----------------------------------------------------------------------------------------------------


#-Окно настройки температры --------------------------------------------------------------------------
def second_inp_widget():
	pass

	hideMainForm()
	second_inp_form = Toplevel()
	second_inp_form.geometry('{}x{}+{}+{}'.format(width, height, cntr_screenW, cntr_screenH))
	second_inp_form.title('Настройка ∆е скорость изминение рассогласавания')
	second_inp_form.resizable(False,False)
#Функции --------------------------------------------------------------------------------------------

	def update_second_setting():
		del tmpr_delta[:]
		tmpr_delta.append(entry_0.get())
		tmpr_delta.append(entry_1.get())
		tmpr_delta.append(entry_2.get())

	def drawFigure2():
		delta_x = np.linspace(-3, 3, 5)
		delta_nb = fuzz.trimf(delta_x, term2_nb)
		delta_ns = fuzz.trimf(delta_x, term2_ns)
		delta_ze = fuzz.trimf(delta_x, term2_ze)
		delta_ps = fuzz.trimf(delta_x, term2_ps)
		delta_pb = fuzz.trimf(delta_x, term2_pb)

		second_picture.plot(delta_x, delta_nb, label='NB')
		second_picture.plot(delta_x, delta_ns, label='NS')
		second_picture.plot(delta_x, delta_ze, label='ZE')
		second_picture.plot(delta_x, delta_ps, label='PS')
		second_picture.plot(delta_x, delta_pb, label='PB')
		second_picture.grid()
		second_picture.legend(frameon=False)
		second_picture.set_xlim(-3,3)
		second_picture.set_ylim(0,1)
		second_picture.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.)

#----------------------------------------------------------------------------------------------------
#-Фигура --------------------------------------------------------------------------------------------
	second_figure = Figure(figsize=(3, 3), dpi=100)
	second_canvas = FigureCanvasTkAgg(second_figure, master=second_inp_form)
	second_canvas.draw()
	toolbar = NavigationToolbar2Tk(second_canvas,second_inp_form)
	toolbar.update()
	toolbar.pack(side=TOP, fill=X, padx=8)
	second_picture  = second_figure.add_subplot(111)
	drawFigure2()
	second_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=10)
	second_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx=10)
#-----------------------------------------------------------------------------------------------------
#-Главная фрейм---------------------------------------------------------------------------------------
	second_frame = LabelFrame(second_inp_form, height =200, text='Настройка термов')
	#-Вверхный фрейм ---------------------------------------------------------------------------------
	top_frame_2 = Frame(second_frame, height =100)

	label_0  = Label(top_frame_2, width = 10, text='NP(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_1  = Label(top_frame_2, width = 10, text='NS(x1,x2,x3)').grid(row=1, column=3, padx=5)
	label_2  = Label(top_frame_2, width = 10, text='Z(x1,x2,x3)' ).grid(row=1, column=5, padx=5)

	entry_0  = Entry(top_frame_2, width = 10, font=14)
	entry_1  = Entry(top_frame_2, width = 10, font=14)
	entry_2  = Entry(top_frame_2, width = 10, font=14)

	entry_0.insert(0, term2_nb)
	entry_1.insert(0, term2_ns)
	entry_2.insert(0, term2_ze)

	entry_0.grid(row=1, column=2)
	entry_1.grid(row=1, column=4)
	entry_2.grid(row=1, column=6)

	top_frame_2.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)

	#-Нижный фрейм------------------------------------------------------------------------------------
	bottom_frame_2 = Frame(second_frame, height =100)

	label_3   = Label(bottom_frame_2,  width = 10, text='PS(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_4   = Label(bottom_frame_2,  width = 10, text='PB(x1,x2,x3)').grid(row=1, column=3, padx=5)

	entry_3   = Entry(bottom_frame_2,  width = 10, font=14)
	entry_4   = Entry(bottom_frame_2,  width = 10, font=14)

	entry_3.insert(0, term2_ps)
	entry_4.insert(0, term2_pb)

	entry_3.grid(row=1, column=2)
	entry_4.grid(row=1, column=4)

	bottom_frame_2.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------
	#Кнопки управления -------------------------------------------------------------------------------
	term_btn_1 = Button(second_frame, width = 10, text ='ОК')
	term_btn_1.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_2 = Button(second_frame, width = 10, text ='Отмена', command = lambda:closeSubForm(second_inp_form))
	term_btn_2.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_3 = Button(second_frame, width = 10, text = 'Обновить')
	term_btn_3.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------
	second_frame.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=10)

	second_inp_form.protocol('WM_DELETE_WINDOW', lambda: closeSubForm(second_inp_form))
#-----------------------------------------------------------------------------------------------------
#-Окно настройки температры -------------------------------------------------------------------------

def output_widget():
	pass

	hideMainForm()
	first_out_form = Toplevel()
	first_out_form.geometry('{}x{}+{}+{}'.format(width, height, cntr_screenW, cntr_screenH))
	first_out_form.title('Настройка Температуры')
#Функции --------------------------------------------------------------------------------------------

	def update_out_setting():
		del ctrl_output[:]
		ctrl_output.append(entry_0.get())
		ctrl_output.append(entry_1.get())
		ctrl_output.append(entry_2.get())
		ctrl_output.append(entry_3.get())
		ctrl_output.append(entry_4.get())

	def drawFigure3():
		output_x = np.linspace(-1, 1, 5)
		output_nb = fuzz.trimf(output_x, term3_nb)
		output_ns = fuzz.trimf(output_x, term3_ns)
		output_ze = fuzz.trimf(output_x, term3_ze)
		output_ps = fuzz.trimf(output_x, term3_ps)
		output_pb = fuzz.trimf(output_x, term3_pb)
		third_picture.plot(output_x, output_nb, label='NB')
		third_picture.plot(output_x, output_ns, label='NS')
		third_picture.plot(output_x, output_ze, label='ZE')
		third_picture.plot(output_x, output_ps, label='PS')
		third_picture.plot(output_x, output_pb, label='PB')
		third_picture.grid()
		third_picture.legend(frameon=False)
		third_picture.set_xlim(-1,1)
		third_picture.set_ylim(0,1)
		third_picture.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.)

#----------------------------------------------------------------------------------------------------
#-Фигура --------------------------------------------------------------------------------------------
	first_out_form.resizable(False,False)
	third_figure = Figure(figsize=(3, 3), dpi=100)
	third_canvas = FigureCanvasTkAgg(third_figure, master=first_out_form)
	third_canvas.draw()
	toolbar = NavigationToolbar2Tk(third_canvas, first_out_form)
	toolbar.update()
	toolbar.pack(side=TOP, fill=X, padx=8)
	third_picture = third_figure.add_subplot(111)
	drawFigure3()
	third_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=10)
	third_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx=10)

#-Главная фрейм---------------------------------------------------------------------------------------
	first_frame = LabelFrame(first_out_form, height =200, text='Настройка термов')
	#-Вверхный фрейм ---------------------------------------------------------------------------------
	top_frame_1 = Frame(first_frame, height =100)

	label_0    = Label(top_frame_1, width = 10, text='NP(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_1    = Label(top_frame_1, width = 10, text='NS(x1,x2,x3)').grid(row=1, column=3, padx=5)
	label_2    = Label(top_frame_1, width = 10, text='Z(x1,x2,x3) ').grid(row=1, column=5, padx=5)

	entry_0    = Entry(top_frame_1, width = 10, font=14)
	entry_1    = Entry(top_frame_1, width = 10, font=14)
	entry_2    = Entry(top_frame_1, width = 10, font=14)

	entry_0.insert(0, term3_nb)
	entry_1.insert(0, term3_ns)
	entry_2.insert(0, term3_ze)

	entry_0.grid(row=1, column=2)
	entry_1.grid(row=1, column=4)
	entry_2.grid(row=1, column=6)

	top_frame_1.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	#-Нижный фрейм------------------------------------------------------------------------------------
	bottom_frame_1 = Frame(first_frame, height =100)

	label_3   = Label(bottom_frame_1,  width = 10, text='PS(x1,x2,x3)').grid(row=1, column=1, padx=5)
	label_4   = Label(bottom_frame_1,  width = 10, text='PB(x1,x2,x3)').grid(row=1, column=3, padx=5)

	entry_3   = Entry(bottom_frame_1,  width = 10, font=14)
	entry_4   = Entry(bottom_frame_1,  width = 10, font=14)

	entry_3.insert(0, term3_ps)
	entry_4.insert(0, term3_pb)

	entry_3.grid(row=1, column=2)
	entry_4.grid(row=1, column=4)

	bottom_frame_1.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	#Кнопки управления -------------------------------------------------------------------------------
	term_btn_1 = Button(first_frame, width = 10, text ='ОК')
	term_btn_1.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_2 = Button(first_frame, width = 10, text ='Отмена',command = lambda:closeSubForm(first_out_form))
	term_btn_2.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	term_btn_3 = Button(first_frame, width = 10, text = 'Обновить')
	term_btn_3.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
	#-------------------------------------------------------------------------------------------------

	first_frame.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=10)

	first_out_form.protocol('WM_DELETE_WINDOW', lambda: closeSubForm(first_out_form))
#-----------------------------------------------------------------------------------------------------
# расчет программы для симуляции----------------------------------------------------------------------

# Sparse universe makes calculations faster, without sacrifice accuracy.
# Only the critical points are included here; making it higher resolution is
# unnecessary.


universe1 = np.linspace(-3, 3, 5)
universe2 = np.linspace(-3, 3, 5)
universe3 = np.linspace(-1, 1, 5)

# Create the three fuzzy variables - two inputs, one output
error = ctrl.Antecedent(universe1, 'error')
delta = ctrl.Antecedent(universe2, 'delta')
output = ctrl.Consequent(universe3, 'output')

# Here we use the convenience `automf` to populate the fuzzy variables with
# terms. The optional kwarg `names=` lets us specify the names of our Terms.

error['nb'] = fuzz.trimf(universe1, [-3,-3,-1.5])
error['ns'] = fuzz.trimf(universe1, [-3,-1.5,-0])
error['ze'] = fuzz.trimf(universe1, [-1.5,0,1.5])
error['ps'] = fuzz.trimf(universe1, [0,1.5,3])
error['pb'] = fuzz.trimf(universe1, [1.5,3,3])

delta['nb'] = fuzz.trimf(universe2, [-3,-3,-1.5])
delta['ns'] = fuzz.trimf(universe2, [-3,-1.5,-0])
delta['ze'] = fuzz.trimf(universe2, [-1.5,0,1.5])
delta['ps'] = fuzz.trimf(universe2, [0,1.5,3])
delta['pb'] = fuzz.trimf(universe2, [1.5,3,3])

output['nb'] = fuzz.trimf(universe3, [-1,-1,-0.5])
output['ns'] = fuzz.trimf(universe3, [-1,-0.5,0])
output['ze'] = fuzz.trimf(universe3, [-0.5,0,0.5])
output['ps'] = fuzz.trimf(universe3, [0,0.5,1])
output['pb'] = fuzz.trimf(universe3, [0.5,1,1])


rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
          (error['ns'] & delta['nb']) |
          (error['nb'] & delta['ns'])),
consequent=output['nb'], label='rule nb')

rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
          (error['nb'] & delta['ps']) |
          (error['ns'] & delta['ns']) |
          (error['ns'] & delta['ze']) |
          (error['ze'] & delta['ns']) |
          (error['ze'] & delta['nb']) |
          (error['ps'] & delta['nb'])),
consequent=output['ns'], label='rule ns')

rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
          (error['ns'] & delta['ps']) |
          (error['ze'] & delta['ze']) |
          (error['ps'] & delta['ns']) |
          (error['pb'] & delta['nb'])),
consequent=output['ze'], label='rule ze')

rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
          (error['ze'] & delta['pb']) |
          (error['ze'] & delta['ps']) |
          (error['ps'] & delta['ps']) |
          (error['ps'] & delta['ze']) |
          (error['pb'] & delta['ze']) |
          (error['pb'] & delta['ns'])),
consequent=output['ps'], label='rule ps')

rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
          (error['pb'] & delta['pb']) |
          (error['pb'] & delta['ps'])),
consequent=output['pb'], label='rule pb')

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])
sim = ctrl.ControlSystemSimulation(system, flush_after_run=21 * 21 + 1)
upsampled = np.linspace(-3, 3, 21)
x, y = np.meshgrid(upsampled, upsampled)
z = np.zeros_like(x)
for i in range(21):
    for j in range(21):
        sim.input['error'] = x[i, j]
        sim.input['delta'] = y[i, j]
        sim.compute()
        z[i, j] = sim.output['output']
#-----------------------------------------------------------------------------------------------------

#-Создаем главную окно -------------------------------------------------------------------------------
root.geometry('{}x{}+{}+{}'.format(width, height, cntr_screenW, cntr_screenH))
root.resizable(False,False)
root.title('Настройки нечеткого регулятора')
#-----------------------------------------------------------------------------------------------------
#-Создаем фигуру для главного окна -------------------------------------------------------------------
from mpl_toolkits.mplot3d import Axes3D
fig = Figure(figsize=(3, 3), dpi=100)
main_canvas = FigureCanvasTkAgg(fig, master=root)
main_canvas.draw()
toolbar = NavigationToolbar2Tk(main_canvas,root)
toolbar.update()
toolbar.pack(side=TOP, fill=X, padx=8)
mainPict  = fig.add_subplot(111, projection='3d')
surf = mainPict.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)

main_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=10)
main_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1, padx=10)
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
ctrl_frame = LabelFrame(root, height= 200, text="Настройка регулятора")
#-----------------------------------------------------------------------------------------------------
left_frame = Frame(ctrl_frame, height= 100)

ctrl_inp_btn_1 = Button(left_frame, height=2, width=20,
						text='E Ошибка', font='14', command=first_inp_widget)
ctrl_inp_btn_1.pack(padx=5, pady=5, expand=1)
ctrl_inp_btn_2 = Button(left_frame, height=2, width=20,
 						text='∆E Дельта', font='14', command=second_inp_widget)
ctrl_inp_btn_2.pack(padx=5, pady=5, expand=1)
left_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=8, pady=10)
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
center_frame   = Frame(ctrl_frame, height= 100)
met_label1 = Label(center_frame, text='Метод\nМамдани', bd = 1,
				   relief = RAISED, height='8', width='15', font='14' )
met_label1.pack(padx=5, pady=5, expand=1)
center_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=8, pady=10)
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
right_frame = Frame(ctrl_frame, height= 100)

ctrl_out_btn_3 = Button(right_frame, height=2, width=20, font='14',
 						text='Вывод', command=output_widget)
ctrl_out_btn_3.pack(padx=5, pady=5, expand=1)
right_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=8, pady=10)

#Кнопки управления -------------------------------------------------------------------------------
ctrl_bot_frame = Frame(root, height=100)
ctrl_btn_1 = Button(ctrl_bot_frame, width = 10, text ='ОК')
ctrl_btn_1.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
ctrl_btn_2 = Button(ctrl_bot_frame, width = 10, text ='Отмена', command = root.destroy)
ctrl_btn_2.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
ctrl_btn_3 = Button(ctrl_bot_frame, width = 10, text ='Обновить')
ctrl_btn_3.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
ctrl_bot_frame.pack(side=BOTTOM, fill=BOTH, expand=1, padx=5, pady=10)
#-------------------------------------------------------------------------------------------------

ctrl_frame.pack(side=TOP, fill=BOTH, expand=1, padx=8, pady=10)
#-----------------------------------------------------------------------------------------------------

#Нечеткая логика ------------------------------------------------------------------------------------



root.mainloop()
