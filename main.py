from tkinter import *
import time
import random
from colorama import Fore
from colorama import Style
import os
PATH = os.getcwd()+'\imgs'

class CPU:
    def __init__(self):
        self.CPUutilization = 0
        self.sleepTime = 1
        self.flag = False
        self.entry = None
        self.win = None
        self.text=''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show(txt):
        # Create an instance of tkinter frame
        if cpu.win:
            cpu.win.destroy()
        cpu.win = Toplevel()

        # Set the geometry
        cpu.win.geometry("700x350")

        # Add a Scrollbar(horizontal)
        v = Scrollbar(cpu.win, orient='vertical')
        v.pack(side=RIGHT, fill='y')

        # Add a text widget
        text = Text(cpu.win, font=("Georgia, 24"), yscrollcommand=v.set)

        # Add some text in the text widget
        text.insert(END, txt)

        # Attach the scrollbar with the text widget
        v.config(command=text.yview)
        text.pack()
        window.update()

def speed():
    if cpu.sleepTime >= 0.1:
        cpu.sleepTime -= 0.1
        delay.configure(text=round(cpu.sleepTime, 1))
        window.update()
    else:
        cpu.sleepTime = 0
        delay.configure(text=round(cpu.sleepTime, 1))
        window.update()


def Pause(self):
    if cpu.flag:
        self.configure(image=img2)
        cpu.flag = False
    else:
        self.configure(image=img1)
        cpu.flag = True


def temp_entry(e):
    if cpu.entry.get() == "Stop Time":
        cpu.entry.delete(0, "end")

def history(HistoryQ):
    for i in HistoryQ:
        if i[0] == 'E':
            counter = 2
            while True:
                if i[counter] == '_':
                    break
                counter += 1
            for L in HistoryQ:
                if L[0] == 'L' and L[counter] == '_' and L[1:counter] == i[1:counter]:
                    print(f"PID = {i[1:counter]} and start={i[counter + 1:]} end={L[counter + 1:]}")
                    break


class Process:
    def __init__(self, name, data: list):
        self.name = name  # PID
        self.data = data  # Array (List)
        self.sumBurst = 0  # sum CPU Burst
        self.t = 0  # used in Q3
        self.numOfRun = 0  # used in Q1 and Q2
        self.state = 'waiting'  # waiting / running / terminated / I/O
        self.preempted = 0  # used in Q3
        self.finishTime = None  # has the Time when finish
        self.start = None  # the time when left
        self.timeToLeft = None  # used in Q1 **MUST back to NONE if its done*
        self.calculate = True  # used in Q3




def write_to_file():
    f = open("input.txt", "a")
    f.truncate(0)
    for i in range(NumberOfProcesses):  # number of process
        f.write(f"{i}\t")  # print PID
        f.write(f"{random.randint(0, MaxArrivalTime)}\t")  # Arrival time
        NumOfCPUBrust = random.randint(1, MaxNumOfCPUBurst)
        for CPU in range(NumOfCPUBrust):
            f.write(f"{random.randint(MinCPU, MaxCPU)}\t")  # CPU
            if CPU != NumOfCPUBrust - 1:
                f.write(f"{random.randint(MinCPU, MaxCPU)}\t")  # IO
        f.write('\n')
    f.close()


def read_from_file():
    f = open('input.txt', 'r')
    for i in f.readlines():
        l = []
        for data in i.split('\t'):
            if data != '\n':
                l.append(int(data))
        AllProcesses.append(Process(name=l[0], data=l))
    for i in AllProcesses:
        for dataIndex in range(2, len(i.data)):
            if dataIndex % 2 == 0:  # CPU Burst
                i.sumBurst += i.data[dataIndex]


def swap_the_list(newList):  # used in check_arrive_swap
    if newList:
        size = len(newList)

        # Swapping
        temp = newList[0]

        for i in range(len(newList)):
            if i < size - 1:
                newList[i] = newList[i + 1]
        newList[size - 1] = temp


def check_arrive_swap(SWAP):
    if TIME <= MaxArrivalTime:
        for i in AllProcesses:  # Arrival time = self.data[1]
            if i.data[1] == TIME:
                print(f"{Fore.CYAN}**Note** Process ({i.name}) has arrived **Note** {Style.RESET_ALL}")
                cpu.text+='\n'+f"**Note** Process ({str(i.name)} has arrived **Note** "

                i.start = TIME
                Queue1.append(i)
                movementsAtQ1.append(f'E{i.name}_{TIME}')
    if arrive:
        for i in arrive:
            if dictionary[i] == Queue3:
                i.calculate = True
            dictionary[i].append(i)
        arrive.clear()
    if SWAP == 'Q1':
        swap_the_list(Queue1)
    elif SWAP == 'Q2':
        swap_the_list(Queue2)


def check_IO_Qs():

    delete = []
    if IO:  # Note : here we will +1 to all processes in I/O untill the I/O Burst reach 0 to Move it to arrive list
        index = -1
        for loopProcess in IO:
            index += 1
            for i in range(2, len(loopProcess.data)):
                if loopProcess.data[i] != 0:
                    if i % 2 == 1:  # I/O Burst
                        loopProcess.data[i] -= 1
                        if loopProcess.data[i] == 0:
                            if i < len(loopProcess.data) - 1:
                                loopProcess.state = 'waiting'
                                delete.append(index)
                                arrive.append(loopProcess)
                            else:
                                Exception("ERROR, we got a I/O state Process No CPU Burst after it")
                    else:
                        raise Exception("ERROR, we got a I/O state Process with CPU value")
                    break

    # delete Area
    tcopy = delete.copy()
    fixed = len(delete)
    for i in tcopy:
        IO.pop(i + len(delete) - fixed)
        delete.pop(0)
    # delete Area

    flag = None
    if Queue1 or Queue2:

        if Queue1:
            sec = 1
            Queue = Queue1
        else:
            Queue = Queue2
            sec = 2
        loopProcess = Queue[0]
        if loopProcess.state == 'waiting' or loopProcess.state == 'running':
            for i in range(2, len(loopProcess.data)):
                if loopProcess.data[i] != 0:
                    if i % 2 == 0:  # CPU Burst
                        if loopProcess.state == 'waiting':
                            loopProcess.timeToLeft = min(q1, loopProcess.data[i])
                            loopProcess.state = 'running'

                        loopProcess.data[i] -= 1
                        loopProcess.timeToLeft -= 1
                        cpu.CPUutilization += 1
                        if loopProcess.timeToLeft == 0:
                            loopProcess.numOfRun += 1
                            if loopProcess.data[i] == 0:

                                if i < len(loopProcess.data) - 1:
                                    loopProcess.state = 'I/O'
                                    IO.append(loopProcess)
                                    if sec == 1:
                                        dictionary[loopProcess] = Queue2
                                    elif sec == 2:
                                        dictionary[loopProcess] = Queue3
                                    if loopProcess.numOfRun == 10:
                                        loopProcess.numOfRun = 0
                                        if sec == 1:
                                            dictionary[loopProcess] = Queue2
                                        elif sec == 2:
                                            dictionary[loopProcess] = Queue3
                                    if sec == 1:
                                        movementsAtQ1.append(f'L{loopProcess.name}_{TIME}')
                                    else:
                                        movementsAtQ2.append(f'L{loopProcess.name}_{TIME}')
                                    Queue.pop(0)

                                else:
                                    loopProcess.state = 'terminated'
                                    Finish.append(loopProcess)
                                    if sec == 1:
                                        movementsAtQ1.append(f'L{loopProcess.name}_{TIME}')
                                    else:
                                        movementsAtQ2.append(f'L{loopProcess.name}_{TIME}')
                                    Queue.pop(0)
                            else:
                                loopProcess.state = 'waiting'
                                if loopProcess.numOfRun == 10:
                                    loopProcess.numOfRun = 0
                                    if sec == 1:
                                        Queue2.append(loopProcess)
                                        movementsAtQ2.append(f'E{loopProcess.name}_{TIME}')
                                    elif sec == 2:

                                        Queue3.append(loopProcess)
                                        movementsAtQ3.append(f'E{loopProcess.name}_{TIME}')
                                    if sec == 1:
                                        movementsAtQ1.append(f'L{loopProcess.name}_{TIME}')
                                    else:
                                        movementsAtQ2.append(f'L{loopProcess.name}_{TIME}')
                                    Queue.pop(0)
                                else:
                                    if sec == 1:
                                        flag = 'Q1'
                                    elif sec == 2:
                                        flag = 'Q2'

                    else:
                        raise Exception("ERROR, we got a waiting state Process with I/O value")
                    break



    # self.state = 'waiting'  # waiting / running / terminated / I/O
    elif Queue3:
        min3 = None
        waitingIndex = None
        runningIndex = None
        Burst = None
        Remove = None
        for i in range(len(Queue3)):
            if Queue3[i].state == 'running':
                if runningIndex:
                    raise Exception("ERROR, we have 2 running states in Q3")
                runningIndex = i
                if min3 == None:
                    min3 = Queue3[i].t
                elif min3 != None:
                    if Queue3[i].t < min3:
                        min3 = Queue3[i].t
            elif Queue3[i].state == 'waiting':
                for index in range(2, len(Queue3[i].data)):
                    if Queue3[i].data[index] > 0:
                        if Queue3[i].calculate:
                            Burst = Alpha * Queue3[i].data[index] + (1 - Alpha) * Queue3[i].t
                            Queue3[i].calculate = False
                            Queue3[i].t = Burst
                        else:
                            Burst = Queue3[i].t
                        if min3 == None or Burst < min3:
                            waitingIndex = i
                            min3 = Burst
                        break
            else:
                raise Exception(f"ERROR, we got {Queue3[i].state} in Q3")
        if runningIndex != None:  # convert Processing
            if Queue3[runningIndex].t > min3:
                Queue3[runningIndex].preempted += 1
                Queue3[waitingIndex].t = Burst
                Queue3[waitingIndex].state = 'running'
                Queue3[runningIndex].state = 'waiting'
                if Queue3[runningIndex].preempted == 3:
                    Remove = runningIndex
                    Queue4.append(Queue3[runningIndex])
                    movementsAtQ4.append(f'E{Queue3[runningIndex].name}_{TIME}')
                runningIndex = waitingIndex
        elif runningIndex == None:
            runningIndex = waitingIndex
            Queue3[runningIndex].t = Burst
            Queue3[runningIndex].state = 'running'

        for dataIndex in range(2, len(Queue3[runningIndex].data)):
            if Queue3[runningIndex].data[dataIndex] > 0:
                Queue3[runningIndex].data[dataIndex] -= 1
                cpu.CPUutilization += 1
                if Queue3[runningIndex].data[dataIndex] == 0:
                    if dataIndex < len(Queue3[runningIndex].data) - 1:
                        Queue3[runningIndex].state = 'I/O'
                        dictionary[Queue3[runningIndex]] = Queue3
                        Remove = runningIndex
                        IO.append(Queue3[runningIndex])
                    else:
                        Queue3[runningIndex].state = 'terminated'
                        Remove = runningIndex
                        Finish.append(Queue3[runningIndex])
                break

        if Remove != None:
            movementsAtQ3.append(f'L{Queue3[Remove].name}_{TIME}')
            Queue3.pop(Remove)

    elif Queue4:
        for data in range(2, len(Queue4[0].data)):
            if Queue4[0].data[data] > 0:
                Queue4[0].data[data] -= 1
                cpu.CPUutilization += 1
                if Queue4[0].data[data] == 0:
                    if data < len(Queue4[0].data) - 1:  # I/O
                        Queue4[0].state = 'I/O'
                        dictionary[Queue4[0]] = Queue4
                        IO.append(Queue4[0])
                        movementsAtQ4.append(f'L{Queue4[0].name}_{TIME}')
                        Queue4.pop(0)
                    else:  # Finished
                        Queue4[0].state = 'terminated'
                        Finish.append(Queue4[0])
                        movementsAtQ4.append(f'L{Queue4[0].name}_{TIME}')
                        Queue4.pop(0)
                break
    return flag


cpu = CPU()
window = Tk()
window.geometry("798x497")
window.configure(bg="#FFFFFF")
canvas = Canvas(window, bg="#FFFFFF", height=497, width=798, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=PATH+r"\background.png")
img0 = PhotoImage(file=PATH+r"\img0.png")
img2 = PhotoImage(file=PATH+r"\img2.png")
img1 = PhotoImage(file=PATH+r"\img1.png")

background = canvas.create_image(398.99999999999994, 248.50000000000003, image=background_img)
speedButton = Button(bg='#EED0EE', image=img0, borderwidth=0, highlightthickness=0, command=lambda: speed(),
                     relief="flat")
PauseButton = Button(bg='#EED0EE', image=img2, borderwidth=0, highlightthickness=0, command=lambda: Pause(PauseButton),
                     relief="flat")

speedButton.place(x=269.0, y=353.0, width=95, height=75)
PauseButton.place(x=399.0, y=353.0, width=80, height=80)

delay = Label(master=window, bg='#EED0EE', text='1', font=("Ariel", 20))
delay.place(x=190, y=215)

Timer = Label(master=window, fg='#D75151', bg='#EED0EE', text='0', font=("Ariel", 40, "bold"))
Timer.place(x=350, y=120)

entry1 = cpu.entry = Entry(bd=2, bg="#EED0EE", justify='center', highlightthickness=0, font=('Times 14 italic bold'))
entry1.place(x=93.0, y=150.0, width=88.0, height=38)
entry1.insert(0, "Stop Time")
entry1.bind("<FocusIn>", temp_entry)

Button(bg='#EED0EE', bd=3, borderwidth=0,text='Press to show the changes',font=("Ariel", 16, "bold"), highlightthickness=0, command=lambda: show(cpu.text),
                     relief="flat").place(x=87,y=274)
NumberOfProcesses = 10
MaxArrivalTime = 10
MaxNumOfCPUBurst = 5

MinIO = 0
MaxIO = 5

MinCPU = 10
MaxCPU = 50
q1 = 1
q2 = 1
Alpha = 0.5


TIME = 0

AllProcesses = []
arrive = []
Finish = []

Queue1 = []
Queue2 = []
Queue3 = []
Queue4 = []
movementsAtQ1 = []
movementsAtQ2 = []
movementsAtQ3 = []
movementsAtQ4 = []
IO = []
dictionary = {}


text=''
write_to_file()
read_from_file()

copyProcesses = AllProcesses.copy()

print(f'we have {len(copyProcesses)} Processes')
cpu.text+='\n'+f'we have {len(copyProcesses)} Processes'
for i in copyProcesses:
    print(i.data)
    cpu.text+='\n'
    test=''
    for d in i.data:
        test+=f' {d} '
    cpu.text += test
print('---------------------------------------------------------------')
cpu.text+='\n'+'---------------------------------------------------------------'
flag = True
while flag:
    try:
        window.update()
    except:
        break
    while cpu.flag and flag:
        if cpu.entry.get() != 'Stop Time':
            if TIME == int(cpu.entry.get()):
                cpu.flag = False
                PauseButton.configure(image=img2)
        cpu.text=''
        print(f"{Fore.MAGENTA}the time ={TIME}{Style.RESET_ALL}")
        cpu.text+='\n'+f"the time ={TIME}"
        changeFinish = len(Finish)
        SWAP = check_IO_Qs()
        check_arrive_swap(SWAP)
        if Queue1:
            print(bcolors.WARNING + '----->>>Q1<<<-----' + bcolors.ENDC)
            cpu.text += '\n' +'----->>>Q1<<<-----'

            for i in Queue1:
                print(i.data, end=' ')
                cpu.text += '\n'
                test = ''
                for d in i.data:
                    test += f' {d} '
                test +='numOfRun = '+ str(i.numOfRun)
                cpu.text += test
                print(i.numOfRun)
        if Queue2:
            print(bcolors.WARNING + '----->>>Q2<<<-----' + bcolors.ENDC)
            cpu.text += '\n' + '----->>>Q2<<<-----'
            for i in Queue2:
                cpu.text += '\n'
                test = ''
                for d in i.data:
                    test += f' {d} '
                test +='numOfRun = '+ str(i.numOfRun)
                cpu.text += test

                print(i.data, end=' ')
                print(i.numOfRun)
        if Queue3:
            cpu.text += '\n' + '----->>>Q3<<<-----'
            print(bcolors.WARNING + '----->>>Q3<<<-----' + bcolors.ENDC)
            for i in Queue3:
                cpu.text += '\n'
                test = ''
                for d in i.data:
                    test += f' {d} '
                test += ' t= ' + str(i.numOfRun) + ' Premeted = ' + str(i.preempted)
                cpu.text += test

                print(i.data, end=' t=')
                print(i.t, end=' Premeted = ')
                print(i.preempted)
        if Queue4:
            cpu.text += '\n' + '----->>>Q4<<<-----'
            print(bcolors.WARNING + '----->>>Q4<<<-----' + bcolors.ENDC)
            for i in Queue4:
                cpu.text += '\n'
                test = ''
                for d in i.data:
                    test += f' {d} '
                cpu.text += test
                print(i.data)
        if IO:
            cpu.text += '\n' + '----->>>IO<<<-----'
            print(f"{Fore.GREEN}----->>>IO<<<-----{Style.RESET_ALL}")
            for i in IO:
                cpu.text += '\n'
                test = ''
                for d in i.data:
                    test += f' {d} '
                cpu.text += test


                print(f"{Fore.GREEN}{i.data}{Style.RESET_ALL}")
        if len(Finish) != changeFinish:
            cpu.text += '\n' + f"Process ({Finish[len(Finish) - 1].name}) has Finished"
            print(
                f"{Fore.CYAN} Process ({Finish[len(Finish) - 1].name}) has Finished {Style.RESET_ALL}")
            Finish[len(Finish) - 1].finishTime = TIME
        print()
        cpu.text += '\n' +'---------------------------------------------------------------'
        print('---------------------------------------------------------------')
        try:
            if cpu.sleepTime >= 0.1:
                Timer.configure(text=TIME)
                time.sleep(cpu.sleepTime)
            window.update()
        except:
            continue
        TIME += 1

        flag = False

        for i in copyProcesses:
            if i not in Finish:
                flag = True

    sumWaiting = 0

for i in copyProcesses:
    name = i.data[0]
    arriveTime = i.data[1]
    finishTime = i.finishTime
    try:
        waitingTime = finishTime - arriveTime - i.sumBurst
        sumWaiting += waitingTime
    except:break

    start = i.start
    print(f"in PID = {name} start at {start} finished at {finishTime} its waiting time = {waitingTime}")
print(f"avarage waiting time = {sumWaiting / len(copyProcesses)}")
if TIME:
    print(f"CPUutilization == {cpu.CPUutilization / TIME}")
    Timer.configure(text=TIME - 1)


if movementsAtQ1:
    print('in Queue#1')
    history(movementsAtQ1)
if movementsAtQ2:
    print('in Queue#2')
    history(movementsAtQ2)
if movementsAtQ3:
    print('in Queue#3')
    history(movementsAtQ3)
if movementsAtQ4:
    print('in Queue#4')
    history(movementsAtQ4)
while True:
    try:
        window.update()
    except:
        break
