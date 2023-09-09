import customtkinter as tk
import mysql.connector as mysql
conn = mysql.connect(host="localhost", user="root", password="\your Database passcode\")
cur = conn.cursor()


def checkDB(): #Checking for requirements of database
    try:
        cur.execute("use alexa;")
        try:
            cur.execute("select * from tasks;")
            res = cur.fetchall()
        except:
            cur.execute(
                "create table tasks(Id int auto_increment primary key, task varchaes(1000),date varchar(10),stat varchar(20));"
            )
    except:
        cur.execute("create database alexa;")
        checkDB()

def delTask():
    cur.execute("delete from tasks where stat='completed'")
    conn.commit()
    ErrorLb.configure(text="Deleted completed tasks")

def addTask():
    ErrorLb.configure(text="")
    task=TaskText.get("1.0","end-1c")
    task=task.strip()
    date=DateEntry.get().split("/")
    if(len(date)!=3 or int(date[0])>31 or int(date[1])>12 or len(date[2])!=4 or len(task)==0):
        ErrorLb.configure(text="Enter valid information")
    else:
        date=formatDate(date)
        cur.execute(f"insert into tasks(task,date,stat) values('{task}','{date[0]}/{date[1]}/{date[2]}','notcompleted');")
        ErrorLb.configure(text="Successfully added")
        TaskText.delete("1.0","end-1c")
        DateEntry.delete(1,"end")

def completed():
    tasksDict={}
    print(tasksNotcom)
    for i in tasksNotcom:
        tasksDict[i]=globals()[i].get()
    for i in range (len(list(tasksDict.keys()))):
        if(list(tasksDict.values())[i]!=0):
            cur.execute(f"update tasks set stat='completed' where id={int(list(tasksDict.keys())[i][3:])}")
            conn.commit()
    getTask()
    ProgressBar.set(len(tasksCom)/(len(tasksCom)+len(tasksNotcom)))
    ProgressPcent.configure(text=len(tasksCom)/(len(tasksCom)+len(tasksNotcom))*100)

def renderTask(res):
    for i in res:
        print(i)
        print(f"tsk{i[0]}")
        if(i[3]!="completed"):
            globals()[f"tsk{i[0]}"]=tk.CTkCheckBox(ContentFrame,text=i[1],onvalue=i[0],offvalue=0)
            globals()[f"tsk{i[0]}"].pack(side="top")
            tasksNotcom.append(f"tsk{i[0]}")
        else:
            globals()[f"tsk{i[0]}"]=tk.CTkLabel(ContentFrame,text=i[1])
            globals()[f"tsk{i[0]}"].pack(side="top",padx=10)
            tasksCom.append(f"tsk{i[0]}")
        globals()[f"stat{i[0]}"]=tk.CTkLabel(StatFrame,text=i[3])
        globals()[f"stat{i[0]}"].pack(side="top")
        print(tasksCom)
        print(tasksNotcom)

def formatDate(date):
    if(len(date[0])==1):
        date[0]=date[0].strip()
        date[0]="0"+date[0]
    if(len(date[1])==1):
        date[1]=date[1].strip()
        date[1]="0"+date[1]
    return date

def getTask():
    global tasksNotcom,tasksCom
    tasksNotcom=[]
    tasksCom=[]
    CompleteButton.configure(state="normal",command=completed)
    for i in ContentFrame.winfo_children():
        i.destroy()
    for i in StatFrame.winfo_children():
        i.destroy()
    ErrorLb.configure(text="")
    date=DateEntry.get().split("/")
    if(len(date)!=1):
        if(len(date)!=3 or int(date[0])>31 or int(date[1])>12 or len(date[2])!=4):
            ErrorLb.configure(text="Enter a valid date with format DD/MM/YYYY")
        else:
            date=formatDate(date)
            cur.execute(f"select * from tasks where date='{date[0]}/{date[1]}/{date[2]}'")
            res=cur.fetchall()
            renderTask(res)
    else:
        cur.execute(f"select * from tasks;")
        ErrorLb.configure(text="Displaying all tasks as there is no date entered"   )
        res=cur.fetchall()
        renderTask(res)

checkDB()
tk.set_appearance_mode("system")
tk.set_window_scaling(1.0)
app=tk.CTk()
app.geometry("600x600")
MainFrame=tk.CTkFrame(app,border_width=0)
MainFrame.pack(fill="y")
LbMain=tk.CTkLabel(MainFrame,text="Tasks")
LbMain.pack(side="top")

TaskFrame=tk.CTkScrollableFrame(MainFrame,border_width=0)
TaskFrame.pack(fill="x",side="top")
TextFrame=tk.CTkFrame(TaskFrame,border_width=0,)
TextFrame.pack(side="top")

ContentFrame=tk.CTkFrame(TextFrame,border_width=0)
ContentFrame.pack(side="left",anchor="w")
StatFrame=tk.CTkFrame(TextFrame,border_width=0)
StatFrame.pack(side="left",anchor="w")

ProgFrame=tk.CTkFrame(TaskFrame,border_width=0)
ProgFrame.pack(side="top",anchor="s",fill="x",pady=10)
CompleteButton=tk.CTkButton(ProgFrame,text="Complete/Check progress",fg_color="#2b405f",corner_radius=18,border_width=0,state="disabled",command=completed)
CompleteButton.pack(side="top")
ProgressLb=tk.CTkLabel(ProgFrame,text="Progress")
ProgressLb.pack(side="left",padx=5)
ProgressBar=tk.CTkProgressBar(ProgFrame,corner_radius=10,fg_color="#2b3756")
ProgressBar.pack(side="left")
ProgressPcent=tk.CTkLabel(ProgFrame,text="")
ProgressPcent.pack(side="left",padx=5)

InteractionFrame=tk.CTkFrame(MainFrame,border_width=0)
InteractionFrame.pack(side="top")
LabelFrame=tk.CTkFrame(InteractionFrame,border_width=0)
LabelFrame.pack(side='left',fill="y",anchor="w")
TaskLb=tk.CTkLabel(LabelFrame,text="Task: ")
TaskLb.pack(side="top",anchor="n",pady=20)
DateLb=tk.CTkLabel(LabelFrame,text="Date: ")
DateLb.pack(side="top",anchor="n",pady=20)

EntryFrame=tk.CTkFrame(InteractionFrame,border_width=0)
EntryFrame.pack(side="left",fill="y",anchor="w")
TaskText=tk.CTkTextbox(EntryFrame,corner_radius=10,bg_color="#293840",height=80,width=700)
TaskText.pack(side="top",anchor="w",fill="x")
DateEntry=tk.CTkEntry(EntryFrame,corner_radius=10,bg_color="#293840",width=700,placeholder_text="DD/MM/YYYY")
DateEntry.pack(side="top",anchor="w",fill="x",pady=10)

AddButton=tk.CTkButton(MainFrame,text="Add Task",fg_color="#2b405f",corner_radius=18,border_width=0,command=addTask)
AddButton.pack(side="left",padx=5,pady=10)
GetButton=tk.CTkButton(MainFrame,text="Get Tasks",fg_color="#2b405f",corner_radius=18,border_width=0,command=getTask)
GetButton.pack(side="left",padx=5,pady=10)
DelButton=tk.CTkButton(MainFrame,text="Delete Completed",fg_color="#2b405f",corner_radius=18,border_width=0,command=delTask)
DelButton.pack(side="left",padx=5,pady=10)

ErrorLb=tk.CTkLabel(app,text="")
ErrorLb.pack(side="top")
app.mainloop()
