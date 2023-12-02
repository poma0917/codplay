import requests
import re
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
from threading import Thread
import time

class YouTubeSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube 검색 및 링크")

        # 검색 입력 창
        self.entry = tk.Entry(root, width=40)
        self.entry.grid(row=0, column=0, padx=10, pady=10)

        # 검색 버튼
        self.search_button = tk.Button(root, text="검색", command=self.search_and_display)
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        # 결과 표시 창
        self.result_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def search_youtube(self, query):
        video_links = []
        try:
            search_url = f"https://www.youtube.com/results?search_query={query}"
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            video_ids = re.findall(r'watch\?v=(\S{11})', str(soup))
            video_links = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids]
            video_links.sort(key=self.get_video_views, reverse=True)
        except Exception as e:
            print(f"Error during search: {e}")

        return video_links

    def get_video_views(self, video_link):
        try:
            response = requests.get(video_link)
            match = re.search(r'watch-view-count">([\d,]+) views', response.text)
            if match:
                views = match.group(1).replace(',', '')
                return int(views)
        except Exception as e:
            print(f"Error getting views: {e}")

        return 0

    def open_youtube(self, video_link):
        webbrowser.open(video_link)

    def search_and_display(self):
        query = self.entry.get()

        loading_label = tk.Label(self.root, text="로딩중...", font=("Helvetica", 14))
        loading_label.grid(row=2, column=0, columnspan=2, pady=10)

        try:
            loading_dots = tk.StringVar()
            loading_dots.set("")
            dots_label = tk.Label(self.root, textvariable=loading_dots, font=("Helvetica", 14))
            dots_label.grid(row=3, column=0, columnspan=2, pady=10)

            loading_thread = Thread(target=self.animate_loading, args=(loading_dots,))
            loading_thread.start()

            video_links = self.search_youtube(query)

            # 결과를 스크롤 텍스트에 표시
            self.result_text.delete(1.0, tk.END)
            if video_links:
                self.result_text.insert(tk.END, "유튜브 검색 결과 조회수 순 상위 5개 동영상 링크:\n")
                for i, link in enumerate(video_links[:5], start=1):
                    self.result_text.insert(tk.END, f"{i}. {link}\n", "link")

                # 링크가 뜨자마자 조회수에 따라 정렬
                self.result_text.tag_configure("link", foreground="blue", underline=True)
                self.result_text.tag_bind("link", "<Button-1>", self.link_clicked)
                self.result_text.tag_add("link", 1.0, tk.END)
            else:
                self.result_text.insert(tk.END, "검색 결과가 없습니다.")

        finally:
            # 로딩 관련 위젯 숨기기
            loading_label.grid_forget()
            dots_label.grid_forget()
            loading_thread.join()

    def link_clicked(self, event):
        # 클릭하면 조회수에 따라 정렬
        self.result_text.tag_configure("link", foreground="blue", underline=True)
        self.result_text.tag_bind("link", "<Button-1>", lambda event: None)
        self.result_text.tag_add("link", 1.0, tk.END)

        self.result_text.delete(1.0, tk.END)
        query = self.entry.get()
        video_links = self.search_youtube(query)
        if video_links:
            self.result_text.insert(tk.END, "유튜브 검색 결과 조회수 순 상위 5개 동영상 링크:\n")
            for i, link in enumerate(video_links[:5], start=1):
                self.result_text.insert(tk.END, f"{i}. {link}\n", "link")
        else:
            self.result_text.insert(tk.END, "검색 결과가 없습니다.")

    def animate_loading(self, loading_dots_var):
        while True:
            time.sleep(0.2)
            dots = loading_dots_var.get()
            if len(dots) == 4:
                dots = ""
            else:
                dots += "."
            loading_dots_var.set(dots)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeSearchApp(root)
    root.mainloop()
