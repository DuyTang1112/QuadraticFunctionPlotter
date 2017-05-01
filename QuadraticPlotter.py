from tkinter import *
from tkinter.messagebox import *
import math
class CoefficientsDialog:
    def __init__(self, master,title="Coefficients"):
        self.a =0
        self.b=1
        self.c=0
        self.top=Toplevel(master)
        self.top.title(title)
        self.top.resizable(width=False, height=False)
        self.top.protocol('WM_DELETE_WINDOW',self.close) #set behavior for X button
        self.top.grab_set()
        frame1=Frame(self.top)
        frame1.pack(side =TOP,expand=True, fill = X)
        self.entry1=Entry(frame1)
        self.entry1.pack( side = LEFT)
        label1=Label(frame1,text="X^2\t+",width=15, anchor ="w")
        label1.pack(side = LEFT)
        frame1=Frame(self.top)
        frame1.pack(side =TOP,expand=True, fill = X)
        self.entry2=Entry(frame1)
        self.entry2.pack( side = LEFT)
        label1=Label(frame1,text="X  \t+",width=15, anchor ="w")
        label1.pack(side = LEFT)
        frame1=Frame(self.top)
        frame1.pack(side =TOP,expand=True, fill = X)
        self.entry3=Entry(frame1)
        self.entry3.pack( side = LEFT)
        self.button=Button(self.top,text = "Submit",command = self.submit)
        self.button.pack()
    def submit(self):
        self.a=self.entry1.get()
        self.b=self.entry2.get()
        self.c=self.entry3.get()
        if self.a=="" or self.b=="" or self.c=="":
            result=showerror("No input found","Please input something")
            print(result)
        else :
            isdig=True
            try:
                self.a=int(self.a)
                self.b=int(self.b)
                self.c=int(self.c)
            except ValueError:
                isdig=False
            if not isdig:
                showerror("Non numeric input found","Please input integers only")
            elif self.a==0:
                showerror("Coefficient requirement","Coefficient of X^2 cannot be 0")
            else:
                print(self.a,self.b,self.c)
                self.top.destroy()
        
    def close(self):
        self.a, self.c=0,0
        self.b=1
        self.top.destroy()
                

            
class QuadEQPlot:
    def plot_axis(self):
        self.y_val=[(self.a*i*i+self.b*i+self.c)for i in self.x_val] #y values corresponding to x values
        self.ymax=float("-inf")
        for i in self.y_val:
            if abs(i)>self.ymax:
                self.ymax=abs(i)
        self.plotYvalue=[(-self.ymax+(2*self.ymax/10)*i) for i in range(11)] # y values shown in the y-axis
        #draw x axis
        self.canvas.create_line(self.cwidth*.05,self.cheight*.5,self.cwidth*.95,self.cheight*.5,width = 1.5, fill = "green")
        #draw y axis
        self.canvas.create_line(self.cwidth*.5,self.cheight*.05,self.cwidth*.5,self.cheight*.95,width = 1.5, fill = "green")
        xdistance=(self.cwidth*.95-self.cwidth*.05)/10 # distance between each index in x axis
        delimXCoor=[(self.cwidth*.05+xdistance*i) for i in range(len(self.x_val))]
        #draw the plotted lines on x axis
        for i in delimXCoor:
            self.canvas.create_line(i,self.cheight*.5,i,self.cheight*.49,width =1.5, fill ="green")
        # draw the numbers on the x axis
        for i in range(len(self.x_val)):
            if self.x_val[i]==0:
                self.canvas.create_text(delimXCoor[i]+xdistance*.1,self.cheight*.53,text=str(self.x_val[i]))
            else:
                self.canvas.create_text(delimXCoor[i],self.cheight*.53,text=str(self.x_val[i]))
        ydistance=(self.cheight*.95-self.cheight*.05)/10 #distance between each index in y axis
        delimYCoor=[(self.cheight*.05+ydistance*i) for i in range(len(self.y_val))]
        #draw the plotted lines on y axis
        for i in delimYCoor:
            self.canvas.create_line(self.cwidth*.5,i,self.cwidth*.505,i,width =1.5, fill ="green")
        self.plotYvalue=self.plotYvalue[::-1]
        #print(self.plotYvalue)
        # draw the numbers on the y axis
        for i in range(len(self.plotYvalue)):
            if self.plotYvalue[i]==0:
                continue
            self.canvas.create_text(self.cwidth*.49,delimYCoor[i],text="{0:.1f}".format(round(self.plotYvalue[i],4)), anchor = "e")

    def __init__(self,master,title="Function Plot"):
        self.a =0
        self.b= 1
        self.c =0
        self.x_val=[i for i in range(-5,6)]
        self.y_val=[]
        self.init_widgets(master,title)
        
    def init_widgets(self,master,title):
        self.top = Toplevel(master)
        self.top.title(title)
        self.top.resizable(width=False, height=False)
        self.top.protocol('WM_DELETE_WINDOW',self.exit) #set behavior for X button
        menubar=Menu(self.top)
        filemenu=Menu(menubar)
        filemenu.add_command(label = "New equation",command = self.new_equation)
        filemenu.add_command(label = "Save plot as .PS", command = self.save_canvas)
        filemenu.add_separator()
        filemenu.add_command(label = "Clear canvas",command = self.clear_canvas)
        filemenu.add_command(label = "Exit", command = self.exit)
        helpmenu=Menu(menubar)
        helpmenu.add_command(label = "About", command = self.show_help_about)
        menubar.add_cascade(label = "File", menu = filemenu)
        menubar.add_cascade(label = "Help", menu = helpmenu)
        self.top.config(menu=menubar)
        frame=Frame(self.top)
        frame.pack(side =TOP,expand=True, fill = X)
        self.label=Label(frame,text = "No equation")
        self.label.pack(side=LEFT ,anchor=W)
        self.choice=IntVar()
        self.lineRb=Radiobutton(frame, text = "Line", variable=self.choice, value = 0,command = self.plot_equation)
        self.lineRb.pack(side=RIGHT, anchor = E)
        self.pointRb=Radiobutton(frame, text = "Points", variable=self.choice, value = 1,command = self.plot_equation)
        self.pointRb.pack(anchor = E)
        self.cwidth=800 #canvas width
        self.cheight=600 #canvas height
        self.canvas=Canvas(self.top,width=self.cwidth,height=self.cheight,bg = "white")
        self.canvas.pack()
        self.plot_axis()

    def plot_equation(self):
        if self.a==0 or (self.b==0 and self.c==0):
            return
        self.label["text"]="y = {}x^2 + {}x + {}".format(self.a,self.b,self.c)
        self.canvas.delete("all")
        self.plot_axis()
        self.yvalueCoor=[(self.cheight*.5-(i/self.ymax)*(self.cheight*.45)) for i in self.y_val] # actual coordinate of y on canvas
        self.xvalueCoor=[self.cwidth*.5+(i/5)*(self.cwidth*.45) for i in self.x_val] # actual coordinate of x on canvas
        if self.choice.get()==1:
            self.plot_points()
        elif self.choice.get()==0:
            self.plot_line()
    def plot_points(self):
        print(self.x_val)
        print(self.y_val)
        for i in range (len(self.x_val)):
            self.canvas.create_oval(self.xvalueCoor[i]-2,self.yvalueCoor[i]-2,self.xvalueCoor[i]+2,self.yvalueCoor[i]+2,outline= "red",fill = "yellow")
    
    def plot_line(self):
        """ generate a smoother graph by providing more plotted points"""
        xval=[]
        for i in range(-5,6):
            xval.append(i)
            if i!=5:
                k=250 #indicate how many points per 1 unit interval the canvas will plot 
                for j in range (1,k):
                    xval.append(i+round(j/k,10))
        yval=[(self.a*i*i+self.b*i+self.c)for i in xval]
        plotyval=[(self.cheight*.5-(i/self.ymax)*(self.cheight*.45)) for i in yval] # actual coordinate of y on canvas
        plotxval=[self.cwidth*.5+(i/5)*(self.cwidth*.45) for i in xval] # actual coordinate of x on canvas
        for i in range(len(xval)-1):
            self.canvas.create_line(plotxval[i],plotyval[i],plotxval[i+1],plotyval[i+1], fill = "red")
    def clear_canvas(self):
        self.label["text"]="No equation"
        self.canvas.delete("all")
        self.a =0
        self.b= 1
        self.c =0
        self.plot_axis()
        self.b= 0
        
    def show_help_about(self):
        showinfo("About QuadEQPlot","Name: Duy Tang \nID: 0979527")
    def new_equation(self):
        dial=CoefficientsDialog(self.top)
        self.top.wait_window(dial.top)
        self.a=dial.a
        self.b=dial.b
        self.c=dial.c
        self.label["text"]="y = {}x^2 + {}x + {}".format(self.a,self.b,self.c)
        self.canvas.delete("all")
        self.plot_axis()
    def exit(self):
        result=askyesno("Quit QuadEQPlot?", "Do you want to quit?")
        if result:
            quit()
    def save_canvas(self):
        self.canvas.postscript(file="0979527.ps",colormode = "color")

       
mainwin=Tk()
mainwin.withdraw()
qed=QuadEQPlot(mainwin)
mainwin.mainloop()





