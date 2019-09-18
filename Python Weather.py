import sys, requests, datetime, json
import tkinter as tk
from threading import Thread, RLock
from tkinter import ttk


class GUI(Thread):
    def __init__(self):
        super().__init__(target=self.run)
        self.main_window = None


    def run(self):
        self.main_window = MainWindow(self)
        self.main_window.run()


class Window(object):
    """Set Shared Window Variables"""
    def __init__(self, title):
        self.root = tk.Tk()
        self.title = title
        self.root.title(title)


class MainWindow(Window):
    """Main Window"""
    def __init__(self, gui):
        super().__init__('Python Weather')
        self.gui= gui
        self.location = tk.StringVar()
        self.time = tk.StringVar()
        self.weather_condition = tk.StringVar()
        self.tempature = tk.StringVar()
        self.humidity = tk.StringVar()
        self.temphigh = tk.StringVar()
        self.templow = tk.StringVar()
        self.pressure = tk.StringVar()
        self.sunrise = tk.StringVar()
        self.sunset = tk.StringVar()


        ##Build GUI
        self.build_window()


    def build_window(self):
        """Build Main Window, Widgets and Event Bindings"""
        self.root.geometry('400x450+400+300')
        self.root.minsize(400, 450)

        #Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0)

        #User Input Label Frame
        self.user_lbframe = ttk.LabelFrame(self.main_frame, text="Weather Observation for:")
        self.user_lbframe.grid(row=0, column=0, padx=15, pady=5)

        #Location Box
        ttk.Label(self.user_lbframe, text="City: ").grid(row=1, column=0, sticky="W")
        self.station = ttk.Entry(self.user_lbframe, width=25)
        self.station.grid(row=1, column=1, padx=0, pady=5, sticky="E")

        #Submit Button
        self.submit_button = ttk.Button(self.user_lbframe, text="Get Weather", command= self.get_weather)
        self.submit_button.grid(row=2, column=1, pady=5)

        #Output Frame
        self.output_lbframe = ttk.LabelFrame(self.main_frame, text="Current Weather Conditions")
        self.output_lbframe.grid(row=1, column=0, padx=0, pady=5)

        ttk.Label(self.output_lbframe, text="Location: ").grid(row=1 ,column=0, sticky="W")
        self.location_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.location)
        self.location_entry.grid(row=1, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text="Last Updated: ").grid(row=2, column=0, sticky="W")
        self.time_entry = ttk.Entry(self.output_lbframe, width=40, state="readonly", textvariable=self.time)
        self.time_entry.grid(row=2, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text="Weather: ").grid(row=3, column=0, sticky="W")
        self.weather_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.weather_condition)
        self.weather_entry.grid(row=3, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text="Tempature: ").grid(row=4, column=0, sticky='W')
        self.tempature_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.tempature)
        self.tempature_entry.grid(row=4, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Humidity: ').grid(row=5, column=0, sticky='W')
        self.humidity_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.humidity)
        self.humidity_entry.grid(row=5, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Tempature High: ').grid(row=6, column=0, sticky='W')
        self.temphigh_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.temphigh)
        self.temphigh_entry.grid(row=6, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Tempature Low: ').grid(row=7, column=0, sticky='W')
        self.templow_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.templow)
        self.templow_entry.grid(row=7, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Pressure: ').grid(row=8, column=0, sticky='W')
        self.pressure_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.pressure)
        self.pressure_entry.grid(row=8, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Sunrise: ').grid(row=9, column=0, sticky='W')
        self.sunrise_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.sunrise)
        self.sunrise_entry.grid(row=9, column=1, padx=0, pady=5, sticky='E')

        ttk.Label(self.output_lbframe, text='Sunset: ').grid(row=10, column=0, sticky='W')
        self.sunset_entry = ttk.Entry(self.output_lbframe, width=40, state='readonly', textvariable=self.sunset)
        self.sunset_entry.grid(row=10, column=1, padx=0, pady=5, sticky='E')


    def get_weather(self):
        api_key = None      # " "
        if api_key == None:
            self.location.set('Please go to openweathermap.org and get an API key')
            self.time.set('Then edit line 115, pass your api_key as string')
        else:
            try:
                city = self.station.get()
                city = city.replace(' ', '%20')
                request = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(city.lower(), api_key))
                if request.status_code == 200:
                    j = request.text
                    jsondata = json.loads(j)
                    self.json_parser(jsondata)
                else:
                    self.location.set('Invalid City Name')
            finally:
                pass

    def json_parser(self, jsondata):
        ts = datetime.datetime.fromtimestamp(int(jsondata["dt"]))
        risets = datetime.datetime.fromtimestamp(int(jsondata["sys"]["sunrise"]))
        setts = datetime.datetime.fromtimestamp(int(jsondata["sys"]["sunset"]))

        def kelvin_to_fahrenheit(temp):
            return "{:.1f}".format((temp - 273.15) * 1.800 + 32)

        def kelvin_to_celsius(temp):
            return "{:.1f}".format(temp - 273.15)


        self.location.set(jsondata["name"] + ", " +jsondata["sys"]["country"])
        self.time.set(ts.strftime("%a %B %d, %Y  %I:%M %p %Z"))
        self.weather_condition.set(str(jsondata["weather"][0]["main"]) + ": " +
                    str(jsondata["weather"][0]["description"]))
        self.tempature.set(str(kelvin_to_fahrenheit(jsondata["main"]["temp"]) + ' °F      ' +
                    str(kelvin_to_celsius(jsondata["main"]["temp"])) + '°C'))
        self.humidity.set(str(jsondata["main"]["humidity"]) + '%' )
        self.temphigh.set(str(kelvin_to_fahrenheit(jsondata["main"]["temp_max"]) + ' °F      ' +
                    str(kelvin_to_celsius(jsondata["main"]["temp_max"]) + ' °C')))
        self.templow.set(str(kelvin_to_fahrenheit(jsondata["main"]["temp_min"]) + ' °F      ' +
                    str(kelvin_to_celsius(jsondata["main"]["temp_min"]) + ' °C')))
        self.pressure.set(str(jsondata["main"]["pressure"]) + ' Hg')
        self.sunrise.set(risets.strftime("%I:%M %p %Z"))
        self.sunset.set(setts.strftime("%I:%M %p %Z"))



    def run(self):
        """Main Class Function"""
        self.root.mainloop()



def main():
    app = GUI()
    app.run()

if __name__ == "__main__": main()