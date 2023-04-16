import re
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
import sys
import subprocess
import inspect
import ctypes
import sv_ttk #sun valley theme


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


global ani
bClickStop = False
# class class_read:
#     def __init__(self, p_connect, textctrl):
#         textctrl.tag_config("tag_1", foreground="red", font=('blod'))
#         result = []
#         while p_connect.poll() is None:
#             line = p_connect.stdout.readline().strip()
#             if line:
#                 result.append(line)
#                 strTemp = bytes.decode(line)
#                 print(strTemp)
#                 fTemp = float(strTemp[strTemp.find('"temperature": ') + len('"temperature": '):strTemp.find(', "humidity"')])
#                 if(fTemp < 76.85):
#                     textctrl.insert('end', strTemp+'\n')
#                 else:
#                     textctrl.insert('end', strTemp+'\n', "tag_1")
#                 textctrl.update()
#                 textctrl.see('end')
#                 if(True == bClickStop):
#                     break
#             sys.stdout.flush()
#             sys.stderr.flush()
#         print("Stop!")
        
#         p_connect.kill()

# class Thread_process:
#     def __init__(self):
#         self.bClickStop = False

#     def create_connect_thread(self, strCmdPopen):
#         self.connect_thread = threading.Thread(target=self._connect_and_get_message(strCmdPopen), name="T1")

#     def _connect_and_get_message(self, cmd):

#         p = subprocess.Popen(cmd, close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         result = []
#         while p.poll() is None:
#             line = p.stdout.readline().strip()
#             if line:
#                 # line = _decode_data(line)
#                 result.append(line)
#                 # print('\033[1;35m{0}\033[0m'.format(line))
#                 print(line)
#                 if(True == self.bClickStop):
#                     break
#             sys.stdout.flush()
#             sys.stderr.flush()
#         if p.returncode == 0:
#             print('\033[1;32m************** SUCCESS **************\033[0m')
#         else:
#             print('\033[1;31m************** FAILED **************\033[0m')

#         self.p_connect.kill()
#         os.killpg(os.getpgid(self.p_connect), 9)




#         # os.system(cmd)
#         self.bConnect = False

class App(ttk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.mosquitto_sub_path = r"D:/Program Files/mosquitto/mosquitto_sub.exe"
        self.mosquitto_pub_path = r"D:/Program Files/mosquitto/mosquitto_pub.exe"



        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create value lists
        self.option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
        self.readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

        self.combo_list = []
        self.tag_list = []
        self.id_list = []
        self.ca_list = []
        self.key_list = []
        self.cert_list = []


        conf_file = 'config.txt'
        self.read_config(conf_file)

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.var_4 = tk.StringVar(value=self.option_menu_list[1])
        self.var_5 = tk.DoubleVar(value=75.0)

        self.str_var_entry_t = tk.StringVar()
        self.str_var_entry_i = tk.StringVar()
        self.str_var_entry_ca = tk.StringVar()
        self.str_var_entry_key = tk.StringVar()
        self.str_var_entry_cert = tk.StringVar()
        self.str_var_entry_th = tk.StringVar()

        self.str_var_entry_t_pub = tk.StringVar()
        self.str_var_entry_i_pub = tk.StringVar()
        self.str_var_entry_ca_pub = tk.StringVar()
        self.str_var_entry_key_pub = tk.StringVar()
        self.str_var_entry_cert_pub = tk.StringVar()

        self.bClickStop = False
        self.bConnect = False
        self.read_thread = None

        self.dict_realtime_line = {}
        self.list_threshold_line = [[],[]]
        self.line_length = 20

        # Create widgets :)
        self.setup_widgets()
        
    
    def close_window(self):
        if(self.read_thread is not None):
            self.stop_thread(self.read_thread)
        self.read_thread = None
        self.parent.quit()
        self.parent.destroy()


    

    def read_config(self, conf_file):
        with open(conf_file, 'r') as cf:
            lines = cf.readlines()
        
        nIndex = 0
        for line in lines:
            if('#' in line):
                line = line[:line.find('#')]
            if('' != line):
                listTemp = line.split(',')
                if(0 == nIndex): #host
                    self.mosquitto_sub_path = listTemp[0].strip()
                elif(1 == nIndex): #host
                    self.mosquitto_pub_path = listTemp[0].strip()
                elif(2 == nIndex): #host
                    for item in listTemp:
                        item = item.strip()
                        if(item not in self.combo_list):
                            self.combo_list.append(item)
                elif(3 == nIndex): #tag
                    for item in listTemp:
                        item = item.strip()
                        if(item not in self.tag_list):
                            self.tag_list.append(item)
                elif(4 == nIndex): #id
                    for item in listTemp:
                        item = item.strip()
                        if(item not in self.id_list):
                            self.id_list.append(item)
                elif(5 == nIndex): #ca
                    for item in listTemp:
                        item = os.path.abspath(item.strip())
                        if(item not in self.ca_list):
                            self.ca_list.append(item)
                elif(6 == nIndex): #key
                    for item in listTemp:
                        item = os.path.abspath(item.strip())
                        if(item not in self.key_list):
                            self.key_list.append(item)
                elif(7 == nIndex): #cert
                    for item in listTemp:
                        item = os.path.abspath(item.strip())
                        if(item not in self.cert_list):
                            self.cert_list.append(item)
                nIndex = nIndex + 1



    def setup_widgets(self):
        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        
        self.input_frame_total = ttk.LabelFrame(self.widgets_frame, text="Settings", padding=(5, 5))
        self.input_frame_total.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.input_frame = ttk.LabelFrame(self.input_frame_total, text="Sub", padding=(20, 10))
        self.input_frame.grid(
            row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew"
        )

        # label
        self.label_t = ttk.Label(self.input_frame, text='TAG')
        self.label_t.grid(row=0, column=0, padx=5, pady=(0, 10))

        # label
        self.label_i = ttk.Label(self.input_frame, text='ID')
        self.label_i.grid(row=1, column=0, padx=5, pady=(0, 10))

        # label
        self.label_h = ttk.Label(self.input_frame, text='HOST')
        self.label_h.grid(row=2, column=0, padx=5, pady=(0, 10))

        # label
        self.label_ca = ttk.Label(self.input_frame, text='CA')
        self.label_ca.grid(row=3, column=0, padx=5, pady=(0, 10))

        # label
        self.label_key = ttk.Label(self.input_frame, text='KEY')
        self.label_key.grid(row=4, column=0, padx=5, pady=(0, 10))

        # label
        self.label_cert = ttk.Label(self.input_frame, text='CERT')
        self.label_cert.grid(row=5, column=0, padx=5, pady=(0, 10))

        # label
        self.label_th = ttk.Label(self.input_frame, text='Threshold')
        self.label_th.grid(row=6, column=0, padx=5, pady=(0, 10))

        # Entry
        self.entry_t = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_t)
        self.entry_t.insert(0, self.tag_list[0])
        self.entry_t.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        # Entry
        self.entry_i = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_i)
        self.entry_i.insert(0, self.id_list[0])
        self.entry_i.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        

        # Combobox
        self.combobox = ttk.Combobox(self.input_frame, values=self.combo_list)
        self.combobox.current(0)
        self.combobox.grid(row=2, column=1, padx=5, pady=10, sticky="ew", columnspan=2)

        
        # Entry
        self.entry_ca = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_ca)
        self.entry_ca.insert(0, self.ca_list[0])
        # self.entry_ca.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew", columnspan=2)
        self.entry_ca.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_ca = ttk.Button(self.input_frame, text="...",  width = 1, command=self.get_path_ca)
        self.button_ca.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="w")

        
        # Entry
        self.entry_key = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_key)
        self.entry_key.insert(0, self.key_list[0])
        self.entry_key.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_key = ttk.Button(self.input_frame, text="...",  width = 1, command=self.get_path_key)
        self.button_key.grid(row=4, column=2, padx=5, pady=(0, 10), sticky="w")

        # Entry
        self.entry_cert = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_cert)
        self.entry_cert.insert(0, self.cert_list[0])
        self.entry_cert.grid(row=5, column=1, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_cert = ttk.Button(self.input_frame, text="...",  width = 1, command=self.get_path_cert)
        self.button_cert.grid(row=5, column=2, padx=5, pady=(0, 10), sticky="w")

        

        # Entry
        self.entry_th = ttk.Entry(self.input_frame, textvariable=self.str_var_entry_th)
        self.entry_th.insert(0, 76.5)
        self.entry_th.grid(row=6, column=1, padx=5, pady=(0, 10), sticky="ew", columnspan=2)





        self.input_frame_pub = ttk.LabelFrame(self.input_frame_total, text="Pub", padding=(20, 10))
        self.input_frame_pub.grid(
            row=0, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew"
        )

        # Entry
        self.entry_t_pub = ttk.Entry(self.input_frame_pub, textvariable=self.str_var_entry_t_pub)
        self.entry_t_pub.insert(0, self.tag_list[0])
        self.entry_t_pub.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        # Entry
        self.entry_i_pub = ttk.Entry(self.input_frame_pub, textvariable=self.str_var_entry_i_pub)
        self.entry_i_pub.insert(0, self.id_list[1])
        self.entry_i_pub.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew", columnspan=2)

        # Combobox
        self.combobox_pub = ttk.Combobox(self.input_frame_pub, values=self.combo_list)
        self.combobox_pub.current(0)
        self.combobox_pub.grid(row=2, column=0, padx=5, pady=10, sticky="ew", columnspan=2)

        # Entry
        self.entry_ca_pub = ttk.Entry(self.input_frame_pub, textvariable=self.str_var_entry_ca_pub)
        self.entry_ca_pub.insert(0, self.ca_list[0])
        # self.entry_ca.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew", columnspan=2)
        self.entry_ca_pub.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_ca_pub = ttk.Button(self.input_frame_pub, text="...",  width = 1, command=self.get_path_ca_pub)
        # self.button_ca.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="w")
        self.button_ca_pub.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="w")

        # Entry
        self.entry_key_pub = ttk.Entry(self.input_frame_pub, textvariable=self.str_var_entry_key_pub)
        self.entry_key_pub.insert(0, self.key_list[0])
        self.entry_key_pub.grid(row=4, column=0, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_key_pub = ttk.Button(self.input_frame_pub, text="...",  width = 1, command=self.get_path_key_pub)
        self.button_key_pub.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="w")

        # Entry
        self.entry_cert_pub = ttk.Entry(self.input_frame_pub, textvariable=self.str_var_entry_cert_pub)
        self.entry_cert_pub.insert(0, self.cert_list[0])
        self.entry_cert_pub.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")
        # Button
        self.button_cert_pub = ttk.Button(self.input_frame_pub, text="...",  width = 1, command=self.get_path_cert_pub)
        self.button_cert_pub.grid(row=5, column=1, padx=5, pady=(0, 10), sticky="w")




        # Separator
        self.separator_c2 = ttk.Separator(self.widgets_frame)
        self.separator_c2.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.control_frame = ttk.LabelFrame(self.widgets_frame, text="Control", padding=(20, 10))
        self.control_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        # Button
        self.button_connect = ttk.Button(self.control_frame, text="Subscribe", style="Accent.TButton", command=self.btn_func_subscription_connect)
        self.button_connect.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        # Button
        self.button_stop = ttk.Button(self.control_frame, text="Stop", command=self.btn_func_subscription_stop)
        self.button_stop.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Button
        self.button_clear = ttk.Button(self.control_frame, text="Clear", command=self.btn_func_clear_text)
        self.button_clear.grid(row=0, column=2, padx=5, pady=10, sticky="ew")



        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        self.textdisp = tk.Text(self.pane_1, height=10, state='disabled')
        # self.textdisp(row=0, column=0, padx=5, pady=(0, 10), sticky="ew", columnspan=2, rowspan=3)
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")
        
        self.scrollbar.config(command=self.textdisp.yview)
        self.textdisp.config(yscrollcommand=self.scrollbar.set)
        self.textdisp.pack(expand=True, fill="both")


        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # # Tab #1
        # self.tab_1 = ttk.Frame(self.notebook)
        # for index in [0, 1]:
        #     self.tab_1.columnconfigure(index=index, weight=1)
        #     self.tab_1.rowconfigure(index=index, weight=1)
        # self.notebook.add(self.tab_1, text="Tab 1")

        self.fig = plt.Figure(figsize=(6.4, 3.8))
        self.x = []
        self.currentx = 0

        # self.line_length = 100
        # self.x = np.arange(0, self.line_length)        # x-array
        for i in range(self.line_length):
            self.x.append(i)
        self.ax = self.fig.add_subplot(111)
        self.ax.axes.xaxis.set_visible(False)


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.notebook)
        self.canvas.get_tk_widget().grid(column=0,row=1)

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

        # self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)


    def get_path_ca(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_ca.set(str_file_path)
        return str_file_path
    
    def get_path_key(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_key.set(str_file_path)
        return str_file_path
    
    def get_path_cert(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_cert.set(str_file_path)
        return str_file_path
    
    def get_path_ca_pub(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_ca_pub.set(str_file_path)
        return str_file_path
    
    def get_path_key_pub(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_key_pub.set(str_file_path)
        return str_file_path
    
    def get_path_cert_pub(self):
        str_file_path = askopenfilename(title='Open')
        print(str_file_path)
        self.str_var_entry_cert_pub.set(str_file_path)
        return str_file_path

    def btn_func_subscription_stop(self):
        global bClickStop
        bClickStop = True
        self.bClickStop = True
        self.bConnect = False
        if(self.read_thread is not None):
            self.stop_thread(self.read_thread)
        self.button_connect.config(state="normal")
        self.read_thread = None
        
    def btn_func_clear_text(self):
        self.textdisp.config(state='normal')
        self.textdisp.delete(1.0,'end')
        self.textdisp.update()
        self.textdisp.config(state='disabled')

        self.ax.clear()
        self.x = []
        self.currentx = 0
        for i in range(self.line_length):
            self.x.append(i)
        self.dict_realtime_line = {}
        self.canvas.draw()

    def btn_func_subscription_connect(self):
        global bClickStop, ani
        if(False == self.bConnect):
            print("h:" + self.combobox.get())
            print("t:" + self.str_var_entry_t.get())
            print("i:" + self.str_var_entry_i.get())
            print("ca:" + os.path.abspath(self.str_var_entry_ca.get()))
            print("key:" + os.path.abspath(self.str_var_entry_key.get()))
            print("cert:" + os.path.abspath(self.str_var_entry_cert.get()))
            strCurrentWorkPath = os.getcwd()
            print(strCurrentWorkPath)
            strLogFile = os.path.abspath(os.path.join(strCurrentWorkPath, 'subscriber.log'))
            strCmd = '"' + os.path.abspath(self.mosquitto_sub_path) + '"' + ' -h ' + self.combobox.get() + ' -t ' + self.str_var_entry_t.get() + ' -i ' + self.str_var_entry_i.get() + ' --cafile ' + os.path.abspath(self.str_var_entry_ca.get()) + ' --key ' + os.path.abspath(self.str_var_entry_key.get()) + ' --cert ' + os.path.abspath(self.str_var_entry_cert.get()) + ' > ' + strLogFile
            strCmdPopen = '"' + os.path.abspath(self.mosquitto_sub_path) + '"' + ' -h ' + self.combobox.get() + ' -t ' + self.str_var_entry_t.get() + ' -i ' + self.str_var_entry_i.get() + ' --cafile ' + os.path.abspath(self.str_var_entry_ca.get()) + ' --key ' + os.path.abspath(self.str_var_entry_key.get()) + ' --cert ' + os.path.abspath(self.str_var_entry_cert.get())
            print(strCmd)
            

            


            

            self.read_thread = threading.Thread(target=self._connect_and_get_message_inner_func, name="T1", args=(strCmdPopen, ))
            self.read_thread.setDaemon(True)
            self.read_thread.start()
            
            self.bConnect = True
            bClickStop = False
            self.bClickStop = False
            # ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)
    
    def animate(self,i):
        self.line.set_ydata(1*np.sin(self.x+1*i))  # update the data
        return self.line,

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def _connect_and_get_message(self, cmd):
        p_connect = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.bConnect = True
        
        return p_connect
    
    def _pub_warnings(self, cmd):
        p_connect = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = []
        while p_connect.poll() is None:
            line = p_connect.stdout.readline().strip()
            if line:
                result.append(line)
                strTemp = bytes.decode(line)
                print(strTemp)
                if(True == self.bClickStop):
                    break
            sys.stdout.flush()
            sys.stderr.flush()

    def _update_figure(self, msg):
        fTemp = None
        fHumidity = None
        strID = "unknown_id"
        if('"temperature":' in msg):
            fTemp = msg[msg.find('"temperature":') + len('"temperature":'):]
            fTemp = fTemp[: fTemp.find(',')]
            fTemp = float(fTemp)
        if('"humidity"' in msg):
            fHumidity = msg[msg.find('"humidity":') + len('"humidity":'):]
            fHumidity = fHumidity[: fHumidity.find(',')]
            fHumidity = float(fHumidity)
        if('"ID": ' in msg):
            strID = msg[msg.find('"ID": ') + len('"ID": '): msg.find(', "temperature":')]
        
        ################################################################
        # self.dict_realtime_line: [[[temp_x], [temp_y]],[[humidity_x],[fHumidity_y]]]
        ################################################################
        if((None != fTemp) or (None != fHumidity)):
            self.currentx = self.currentx + 1
            if(re.match('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', self.str_var_entry_th.get())):
                self.list_threshold_line[0].append(self.currentx)
                self.list_threshold_line[1].append(float(self.str_var_entry_th.get()))
        if(strID not in self.dict_realtime_line.keys()):
            self.dict_realtime_line[strID] = [[[],[]],[[],[]]] # [[[temp_x], [temp_y]],[[humidity_x],[fHumidity_y]]]
            
        for key in self.dict_realtime_line.keys():
            if(key == strID):
                self.dict_realtime_line[key][0][0].append(self.currentx)
                self.dict_realtime_line[key][0][1].append(fTemp)
                if(self.line_length < len(self.dict_realtime_line[key][0][0])):
                    self.dict_realtime_line[key][0][0].pop(0)
                    self.dict_realtime_line[key][0][1].pop(0)
            else:
                self.dict_realtime_line[key][0][0].append(self.currentx)
                self.dict_realtime_line[key][0][1].append(self.dict_realtime_line[key][0][1][-1])
                if(self.line_length < len(self.dict_realtime_line[key][0][0])):
                    self.dict_realtime_line[key][0][0].pop(0)
                    self.dict_realtime_line[key][0][1].pop(0)
        
        self.ax.clear()
        minx = 1
        maxx = 0
        # self.line_threshold, = self.ax.plot(self.x, [float(self.str_var_entry_th.get())]*self.line_length, 'r--')
        for key in self.dict_realtime_line.keys():
            if(0 != len(self.dict_realtime_line[key][0][0])):
                if(self.dict_realtime_line[key][0][0][0] < minx):
                    minx = self.dict_realtime_line[key][0][0][0]
                if(self.dict_realtime_line[key][0][0][-1] > maxx):
                    maxx = self.dict_realtime_line[key][0][0][-1]
                self.ax.plot(self.dict_realtime_line[key][0][0], self.dict_realtime_line[key][0][1], label=key)
        
        line_threshold_x = np.arange(minx,maxx+1)
        if(self.line_length < len(self.list_threshold_line[0])):
            self.list_threshold_line[0].pop(0)
            self.list_threshold_line[1].pop(0)
        self.line_threshold, = self.ax.plot(self.list_threshold_line[0], self.list_threshold_line[1], 'r--', label='Threshold')

        self.ax.legend()
        self.ax.axes.xaxis.set_visible(False)
        plt.pause(0.1)
        self.canvas.draw()

    





    def _connect_and_get_message_inner_func(self, cmd):

        p_connect = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.button_connect.config(state="disabled")
        # self.p_connect = p_connect
        self.bConnect = True
        
        self.textdisp.tag_config("tag_1", foreground="red", font=('blod'))
        self.textdisp.tag_config("tag_2", background="yellow", foreground="red", font=('blod'))
        result = []
        dictStatus = {}
        nStatus = 0
        while p_connect.poll() is None:
            line = p_connect.stdout.readline().strip()
            if line:
                # result.append(line)
                strTemp = bytes.decode(line)
                print(strTemp)
                self.textdisp.config(state='normal')
                # if('Warning: ' not in strTemp and 'Error' not in strTemp):
                if(('"temperature": ' in strTemp) and (', "humidity"' in strTemp)):
                    strID = ""
                    if('"ID": ' in strTemp):
                        strID = strTemp[strTemp.find('"ID": ') + len('"ID": '):strTemp.find(', "temperature"')]
                    else:
                        strID = "unknown_id"
                    fTemp = float(strTemp[strTemp.find('"temperature": ') + len('"temperature": '):strTemp.find(', "humidity"')])
                    fHumi = float(strTemp[strTemp.find('"humidity": ') + len('"humidity": '):strTemp.find('}')])
                    if(re.match('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', self.str_var_entry_th.get())):
                        fThreshold = float(self.str_var_entry_th.get())
                        strWarning = ""
                        if(fTemp < fThreshold):
                            self.textdisp.insert('end', strTemp+'\n')
                            if("" != strID):
                                dictStatus[strID] = 0
                            else:
                                nStatus = 0
                        else:
                            self.textdisp.insert('end', strTemp+'\n', "tag_1")
                            if("" != strID):
                                if(strID in dictStatus.keys()):
                                    if(1 != dictStatus[strID]):
                                        dictStatus[strID] = 1
                                        for key in dictStatus.keys():
                                            if(0 == dictStatus[key]):
                                                strWarning = strWarning + key + ': normal, '
                                            else:
                                                strWarning = strWarning + key + ': DANGER, '
                                        if(', ' == strWarning[-2:]):
                                            strWarning = strWarning[:-2]
                                        strWarning = 'Warning: ' + strWarning
                                else:
                                    dictStatus[strID] = 1
                                    for key in dictStatus.keys():
                                        if(0 == dictStatus[key]):
                                            strWarning = strWarning + key + ': normal, '
                                        else:
                                            strWarning = strWarning + key + ': DANGER, '
                                    if(', ' == strWarning[-2:]):
                                        strWarning = strWarning[:-2]
                                    strWarning = 'Warning: ' + strWarning
                            else:
                                if(1 != nStatus):
                                    strWarning = "Warning: DANGER!"
                            if("" != strWarning):
                                strcmd = '"' + os.path.abspath(self.mosquitto_pub_path) + '"' + ' -h ' + self.combobox_pub.get() + ' -t ' + self.str_var_entry_t_pub.get() + ' -i ' + self.str_var_entry_i_pub.get() + ' --cafile ' + os.path.abspath(self.str_var_entry_ca_pub.get()) + ' --key ' + os.path.abspath(self.str_var_entry_key_pub.get()) + ' --cert ' + os.path.abspath(self.str_var_entry_cert_pub.get()) + ' -m "' + strWarning + '"'
                                self._pub_warnings(strcmd)
                        self._update_figure(strTemp)
                    else:
                        self.textdisp.insert('end', strTemp+'\n')
                elif(('Warning: ' in strTemp) or ('Error' in strTemp)):
                    self.textdisp.insert('end', strTemp+'\n', "tag_2")
                else:
                    self.textdisp.insert('end', strTemp+'\n')
                
                self.textdisp.config(state='disabled')
                self.textdisp.update()
                self.textdisp.see('end')

                

                if(True == self.bClickStop):
                    break
            sys.stdout.flush()
            sys.stderr.flush()
        print('Stop!')

        return p_connect


    def btn_func_test(self):
        # Create a Frame for the Checkbuttons
        print("Combo = " + self.combobox.get())
        print("Entry = " + self.entry_t.get())
        print(self.str_var_entry_t.get())
        print(self.str_var_entry_i.get())
        

if __name__ == "__main__":
    root = tk.Tk()
    
    root.title("")
    # sv_ttk.set_theme("dark")
    sv_ttk.set_theme("light")
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.close_window)
    app.pack(fill="both", expand=True)
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    # ani = animation.FuncAnimation(app.fig, app.animate, np.arange(1, 200), interval=25, blit=False)
    root.mainloop()