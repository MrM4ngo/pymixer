from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import tkinter as tk
from tkinter import StringVar, ttk, DoubleVar
from random import randint
from customtkinter import *
from tkinter import *
import customtkinter
from tkinter.ttk import *
import time

INTERVAL = 25  # 2 seconds

color = {
    'grey': '#202020'
}


class WindowsAudioProcess:
    MxValue = None  # Class variable to hold MxValue

    def __init__(self, name, frame) -> None:
        self.name = name
        self.frame = frame
        self.volume = 1
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == self.name + ".exe":
                self.volume = volume.GetMasterVolume()

    def create_panel(self, x: int):
        name = CTkLabel(self.frame, text=self.name.capitalize(), fg_color=color['grey'], bg_color=color['grey'])
        name.grid(row=2, column=x, pady=(10, 5), padx=(10, 1))

        process_volume = DoubleVar(value=self.volume)
        scale = CTkSlider(self.frame, from_=0, to=1, orientation='VERTICAL', variable=process_volume,
                          command=lambda x: self.set_volume(process_volume.get()))
        scale.grid(row=3, column=x, padx=20, pady=20, sticky="nsew")
        
        global formatted_output
        scale_text = round(self.volume, 2) * 100
        formatted_output = '{:03d}'.format(int(scale_text)) 
        if formatted_output <= "0":
            formatted_output = "0"
        # scale_text = str(scale_text)

        WindowsAudioProcess.MxValue = CTkLabel(self.frame, text=formatted_output+"%", bg_color=color['grey'], font=("Arial", 15))
        WindowsAudioProcess.MxValue.grid(row=4, column=x)
        # WindowsAudioProcess.MxValue.pack()

    @classmethod
    def update_value(cls):
        if cls.MxValue:
            cls.MxValue.configure(formatted_output+"%") 

            

    def set_volume(self, volume):
        self.volume = volume
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == self.name + ".exe":
                volume.SetMasterVolume(self.volume, None)


class VolumeControllerApp:
    def __init__(self) -> None:
        self.processes = []
        self.root = customtkinter.CTk()
        self.root.geometry("750x450")
        self.root.resizable(True, True)
        self.root.title("Windows Volume Controller")

        self.mainframe = CTkFrame(self.root, fg_color=color['grey'])
        self.mainframe.pack(fill='both', expand=True)
        self.process_names = self.create_process_list()

        self.update()

        self.root.mainloop()
        return

    def update(self):
        WindowsAudioProcess.update_value()  # Call update_value from WindowsAudioProcess
        self.create_panel()
        if self.get_process_names != self.processes:
            self.create_process_list()
        self.root.after(INTERVAL, self.update)

    def create_panel(self):
        for column, process in enumerate(self.processes):
            process.create_panel(column)

    def create_process_list(self) -> None:
        self.processes = []
        for process in self.get_process_names():
            self.processes.append(WindowsAudioProcess(process.split('.')[0], self.mainframe))
        return self.processes

    def get_process_names(self) -> list:
        process_names = []
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name():
                process_names.append(session.Process.name())
        return process_names


if __name__ == "__main__":
    VolumeControllerApp()

