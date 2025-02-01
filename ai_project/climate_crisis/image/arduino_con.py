import serial
import time
import tkinter as tk

# Arduino와의 시리얼 통신 설정
arduino = serial.Serial('COM25', 9600)  # 'COM25'을 실제 Arduino가 연결된 포트로 변경하세요.
time.sleep(2)  # 시리얼 통신 안정화 대기

def send_command(command):
    arduino.write(command.encode())
    time.sleep(0.2)  # 디바운싱을 위한 대기 시간

def update_leds(event=None):
    red_value = red_slider.get()
    green_value = green_slider.get()
    blue_value = blue_slider.get()
    command = f'{red_value},{green_value},{blue_value}\n'
    send_command(command)

def all_off():
    red_slider.set(0)
    green_slider.set(0)
    blue_slider.set(0)
    send_command('0,0,0\n')

# GUI 설정
root = tk.Tk()
root.title("Arduino RGB LED Control")

red_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Red', command=update_leds)
red_slider.pack(pady=5)

green_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Green', command=update_leds)
green_slider.pack(pady=5)

blue_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Blue', command=update_leds)
blue_slider.pack(pady=5)

all_off_button = tk.Button(root, text="All Off", command=all_off)
all_off_button.pack(pady=5)

root.mainloop()

arduino.close()