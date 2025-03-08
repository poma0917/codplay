import tkinter as tk
from tkinter import messagebox
import serial
import time

# Arduino와의 시리얼 통신 설정
arduino = serial.Serial('COM3', 9600)

# 초기 비밀번호 설정
correct_password = "1111"
input_password = ""

# 얼굴 인식 상태 (예시로 True로 설정)
face_detected = True

# Tkinter 창 설정
root = tk.Tk()
root.title("Door Lock System")

# 비밀번호 입력 텍스트
password_label = tk.Label(root, text="비밀번호를 입력하세요:")
password_label.pack()

# 입력된 비밀번호 표시
password_display = tk.Label(root, text="")
password_display.pack()

# 비밀번호 확인 함수
def check_password():
    global input_password
    if input_password[:-1] == correct_password:
        arduino.write(b'SUCCESS')  # 성공 신호
        messagebox.showinfo("Success", "어서오세요!")
        # 서보모터 90도 회전
        arduino.write(b'SERVO 90')
        time.sleep(3)
        # 서보모터 제자리
        arduino.write(b'SERVO 0')
    else:
        messagebox.showerror("Error", "비밀번호가 틀렸습니다.")
    input_password = ""
    password_display.config(text="")

# 아두이노에서 버튼 입력을 받는 함수
def read_from_arduino():
    global input_password
    if arduino.in_waiting > 0:
        data = arduino.readline().decode().strip()
        if face_detected:
            if data in '1234567890*#':
                input_password += data
                password_display.config(text=input_password)
                arduino.write(b'BEEP')  # 피에조 부저 비프음
                if len(input_password) == 5 and input_password[-1] == '*':
                    check_password()
    root.after(100, read_from_arduino)

# 얼굴 인식 상태 확인 (예시로 3초 후 얼굴 인식 상태 변경)
def check_face():
    global face_detected
    face_detected = True
    root.after(3000, lambda: setattr(face_detected, False))

root.after(3000, check_face)
root.after(100, read_from_arduino)

root.mainloop()