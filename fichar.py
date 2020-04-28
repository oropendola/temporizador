#!/cygdrive/c/Users/javi/AppData/Local/Programs/Python/Python36-32/python
#
# @ Javier Felipe Toribio 2019-11-19
#
# Temporizador
#

from tkinter  import *
from tkinter  import messagebox
from datetime import datetime
from datetime import timedelta

import threading

class Record:
    """ Register init time and end time"""
    def __init__(self):
        self.init = None
        self.end  = None
        self.diff = None

    def start(self):
        self.init = datetime.now()
        return self.init

    def finish(self):
        self.end = datetime.now()
        self.diff = (self.end - self.init).seconds
        return self.end

class Registrar:

    def __init__(self,display):
        self.display = display
        self.work    = Record()
        self.dinner  = Record()
        self.actions = { "startDinner"  : self.dinner.start,
                         "finishDinner" : self.dinner.finish,
                         "start"        : self.work.start,
                         "finish"       : self.work.finish }

        if datetime.today().weekday() == 4: #Friday
            hours = 6.25
            # Meal time
            hours += 1.0
        else:
            hours = 8.5


        #self.workSeconds = hours * 3600.0
        self.workSeconds = 10.0 #60.0

    def total(self):
        totalDiff = self.work.diff - self.dinner.diff
        #print(f"totalDiff = {totalDiff}")
        return [str(timedelta(seconds=totalDiff)),
                str(timedelta(seconds=self.dinner.diff))]

    def execute(self,action):
        def perform():
            first_time = self.work.init is None
            fmt = "%H:%M:%S"
            time = self.actions[action]()
            timeStr = time.strftime(fmt)
            self.display.controls[action]["label"].configure(text=timeStr)

            # Cuando se pulsa el boton de iniciar jornada
            # lanzamos un timer con el tiempo jornada + tiempo comida
            # Cuando se cumpla el timer salta una ventana warning
            # para indicar que es hora de irse a casa
            if first_time is True:
                endTime = time + timedelta(seconds=self.workSeconds)
                endTimeStr = endTime.strftime(fmt)
                timer = threading.Timer(self.workSeconds,
                                        self.display.warn(endTimeStr))
                timer.start()

            # Cuando todos los tramos temporales (work y meal) han
            # sido calculados, rellenamos los textos de 
            # diferencia de tiempos (work, meal) respectivamente
            if self.work.diff   is not None and \
               self.dinner.diff is not None:
                total,totalDinner = self.total()
                self.display.total.configure(text=total)
                self.display.totalDinner.configure(text=totalDinner)
        return perform


class Display:



    def __init__(self):

        FONT          = ("Lucila Console",18)
        LABEL_BG      = "#f9f9eb"
        LABEL_FG      = "#800000"
        BASE_WIDTH    = "20"
        LARGE_WIDTH   = "20"
        BUTTON_BG     = "#cce6ff"
        FIELD_2_BG    = "#ccffe6"
        FIELD_2_FG    = "#00331a"

        self.registrar = Registrar(self)

        window = Tk()

        window.title("Registro de jornada. @ Javier Felipe Toribio 2019")

        window.geometry('510x200')

        title = Label(window,
                width = LARGE_WIDTH,
                font  = FONT,
                text  = "Registro de jornada",
                bg    = "blue",
                fg    = "white")

        title.grid(column=0, row=0)

        self.controls = {
                "start"        : { "text" : "Comenzar jornada" },
                "startDinner"  : { "text" : "Comenzar pausa comida" },
                "finishDinner" : { "text" : "Terminar pausa comida" },
                "finish"       : { "text" : "Terminar jornada" } }

        row = 1

        for action, values in self.controls.items():

            values["button"] = Button(window,
              width   = BASE_WIDTH,
              bg      = BUTTON_BG,
              text    = values["text"],
              command = self.registrar.execute(action))

            values["button"].grid(column = 0, row = row)

            values["label"] = Label(window,
                          font  = FONT,
                          width = BASE_WIDTH,
                          bg    = LABEL_BG,
                          fg    = LABEL_FG)
            values["label"].grid(column = 1, row = row)
            row += 1


        self.total = Label(window,
                           font  = FONT,
                           width = LARGE_WIDTH,
                           text  = "Total",
                           bg    = "#cce6ff",
                           fg    = "#00264d")

        self.total.grid(column = 0, row = row)

        self.totalDinner = Label(window,
                          font  = FONT,
                          width = LARGE_WIDTH,
                          text  = "Total comida",
                          bg    = FIELD_2_BG,
                          fg    = FIELD_2_FG)

        self.totalDinner.grid(column = 1, row = row)

        window.mainloop()

    def warn(self,time):
        def show():
            record = Record()
            init = record.start()
            messagebox.showwarning("Timer",
              "Hora de irse a casa \n{}".format(time))
            end = record.finish()
            timeStr = str(end-init).partition(".")[0]
            messagebox.showinfo("Tiempo extra",
              "Tiempo extra desde fin de jornada\n{}".format(timeStr))

        return show


display = Display()




