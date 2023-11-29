import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import threading
from enum import Enum
from google_search import GoogleCustomSearch
from downloader import ImageDownloader
import math

class ColorType(Enum):
    UNDEFINED = 'imgColorTypeUndefined'
    MONO = 'mono'
    GRAY = 'gray'
    COLOR = 'color'
    TRANS = 'trans'
class DominantColor(Enum):
    UNDEFINED = 'imgDominantColorUndefined'
    BLACK = 'black'
    BLUE = 'blue'
    BROWN = 'brown'
    GRAY = 'gray'
    GREEN = 'green'
    ORANGE = 'orange'
    PINK = 'pink'
    PURPLE = 'purple'
    RED = 'red'
    TEAL = 'teal'
    WHITE = 'white'
    YELLOW = 'yellow'
class ImgSize(Enum):
    UNDEFINED = 'imgSizeUndefined'
    HUGE = 'HUGE'
    ICON = 'ICON'
    LARGE = 'LARGE'
    MEDIUM = 'MEDIUM'
    SMALL = 'SMALL'
    XLARGE = 'XLARGE'
    XXLARGE = 'XXLARGE'
class ImageType(Enum):
    UNDEFINED = 'imgTypeUndefined'
    CLIPART = 'clipart'
    FACE = 'face'
    LINEART = 'lineart'
    STOCK = 'stock'
    PHOTO = 'photo'
    ANIMATED = 'animated'


class MyTkinterWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My Tkinter Window")
        self.window.geometry("1000x600")

        self.completed_count = 0

    # Top Half
        top_frame = tk.Frame(self.window)
        top_frame.grid(row=0, column=0, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    # Left Frame
        left_frame = tk.Frame(top_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.grid_columnconfigure(0, weight=1)

    #Search part
        placeholder_text = "Search"
        placeholder_number = "N. of Search"
        self.search_label = tk.Label(left_frame, text='Search')
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_entry = tk.Entry(left_frame, width=40)
        self.search_entry.insert(0, placeholder_text)
        self.search_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, placeholder_text))
        self.search_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, placeholder_text))
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        self.number_entry = tk.Entry(left_frame, width=15)
        self.number_entry.insert(0, placeholder_number)
        self.number_entry.bind("<FocusIn>", lambda event: self.on_number_focus_in(event, placeholder_number))
        self.number_entry.bind("<FocusOut>", lambda event: self.on_number_focus_out(event, placeholder_number))
        self.number_entry.grid(row=0, column=2, padx=10, pady=10)

    #Positive path
        self.positive_path_label = tk.Label(left_frame, text='Download Path')
        self.positive_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.positive_path = tk.Entry(left_frame, width=40)
        self.positive_path.insert(0, os.path.abspath('positive'))
        self.positive_path.grid(row=1, column=1, padx=10, pady=10, sticky="we", columnspan=2)
        left_frame.grid_columnconfigure(1, weight=1)
        self.open_folder_dialog(self.positive_path)

    # Right Frame
        right_frame = tk.Frame(top_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        top_frame.grid_columnconfigure(1, weight=1)

        self.search_button = tk.Button(right_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=0, column=0, padx = 0, pady=10)
        self.progress_bar = ttk.Progressbar(right_frame, length=500, mode='determinate')
        self.progress_bar.grid(row=1, column=0, pady=10, sticky="ew")

        # Error half
        self.error_label = tk.Text(right_frame,height=6, width=55)
        self.error_label.grid(row=2, column=0, padx=20, pady=50, sticky="w")
        self.error_label.insert(tk.END, "\t\t--- ERROR LABEL ---")
        self.error_label.insert(tk.END, "\nChoose the download path carefully, as the program will remove everything in that path before downloading!")
        self.error_label.config(state=tk.DISABLED)
    
        # Advanced half
        self.google_search = GoogleCustomSearch("YOUR-API-KEY", "YOUR-SEARCH-ENGINE-ID")

        self.infoLabel = tk.Label(left_frame, text="ADVANCED SETTINGS")
        self.infoLabel.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        self.imgTypeLabel = tk.Label(left_frame, text="Image Type")
        self.imgTypeLabel.grid(row=5, column = 0, padx=10, pady=10)
        self.selected_image_type = tk.StringVar()
        self.selected_image_type.set(ImageType.UNDEFINED.name)
        self.dropdown_img_type = tk.OptionMenu(left_frame, self.selected_image_type, *ImageType.__members__.keys())
        self.dropdown_img_type.grid(row=6, column=0, padx=10, pady=10)

        self.colorTypeLabel = tk.Label(left_frame, text="Color type")
        self.colorTypeLabel.grid(row=5, column = 1, padx=10, pady=10)
        self.selected_color_type = tk.StringVar()
        self.selected_color_type.set(ColorType.UNDEFINED.name)
        self.dropdown_color_type = tk.OptionMenu(left_frame, self.selected_color_type, *ColorType.__members__.keys())
        self.dropdown_color_type.grid(row=6, column=1, padx=10, pady=10)

        self.imgSizeLabel = tk.Label(left_frame, text="Image Size")
        self.imgSizeLabel.grid(row=5, column = 2, padx=10, pady=10)
        self.selected_size_type = tk.StringVar()
        self.selected_size_type.set(ImgSize.UNDEFINED.name)
        self.dropdown_img_size = tk.OptionMenu(left_frame, self.selected_size_type, *ImgSize.__members__.keys())
        self.dropdown_img_size.grid(row=6, column=2, padx=10, pady=10)

        self.dominantColorLabel = tk.Label(left_frame, text="Dominant Color")
        self.dominantColorLabel.grid(row=11, column = 0, padx=10, pady=10)
        self.selected_dom_color = tk.StringVar()
        self.selected_dom_color.set(DominantColor.UNDEFINED.name)
        self.dropdown_dom_color = tk.OptionMenu(left_frame, self.selected_dom_color, *DominantColor.__members__.keys())
        self.dropdown_dom_color.grid(row=12, column=0, padx=10, pady=10)
        

        self.window.mainloop()


    def printer(self, item):
        print(item)

    def open_folder_dialog(self, entry_widget):
        def browse_folder():
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                entry_widget.configure(state='normal')
                entry_widget.delete(0, tk.END)
                entry_widget.insert(tk.END, folder_selected)
                entry_widget.configure(state='disabled')
        entry_widget.configure(state='normal')
        entry_widget.bind('<Button-1>', lambda event: browse_folder())
        entry_widget.configure(state='disabled')

    def on_entry_focus_in(self, event, placeholder_text):
        if self.search_entry.get() == placeholder_text:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(fg='black')
    def on_entry_focus_out(self, event, placeholder_text):
        if not self.search_entry.get():
            self.search_entry.insert(0, placeholder_text)
            self.search_entry.configure(fg='gray')


    def on_number_focus_in(self, event, placeholder_text):
        if self.number_entry.get() == placeholder_text:
            self.number_entry.delete(0, tk.END)
            self.number_entry.configure(fg='black')
    def on_number_focus_out(self, event, placeholder_text):
        if not self.number_entry.get():
            self.number_entry.insert(0, placeholder_text)
            self.number_entry.configure(fg='gray')
    

    def perform_search(self):
        search_query = self.search_entry.get()
        num = self.number_entry.get()
        domColor = self.selected_dom_color.get()
        colType = self.selected_color_type.get()
        size = self.selected_size_type.get()
        imgType = self.selected_image_type.get()
        domColor_value = DominantColor[domColor].value
        colType_value = ColorType[colType].value
        size_value = ImgSize[size].value
        imgType_value = ImageType[imgType].value
        downloader = ImageDownloader()
        try:
            num = int(num)
            self.search(search_query, colType_value, domColor_value, size_value, imgType_value, num, downloader)
        except ValueError or tk.TclError:
           self.show_error("Invalid input on number of searches!")

    def search(self, search_query, colType_value, domColor_value, size_value, imgType_value, num, downloader):
        self.completed_count = 0
        self.google_search.reset_i()
        self.progress_bar['maximum'] = num
        self.progress_bar['value'] = 0
        self.clean_folder(self.positive_path.get())
        start = 0
        number = 10
        if num > 10:
            print(num)
            iterations = math.floor(num / 10)
            remainder = num % 10

            for _ in range(iterations):
                # Perform the task with start and num
                response = self.google_search.search(search_query, colType_value, domColor_value, size_value, imgType_value, number, start)
                self.runSearch(response, downloader, num)
                start += 10

            if remainder > 0:
                # Perform the task with the final start and remainder as num
                response = self.google_search.search(search_query, colType_value, domColor_value, size_value, imgType_value, remainder, start)
                self.runSearch(response, downloader, num)
        else:
            if num == 0:
                self.show_error("Number of Search is 0, no search will be done!")
            else:
                # Perform the task with the given number as num
                response = self.google_search.search(search_query, colType_value, domColor_value, size_value, imgType_value, num, start)
                self.runSearch(response, downloader, num)

    def runSearch(self, response, downloader, num):
        # Create a lock object
        lock = threading.Lock()

        # Define the target function to run in the thread
        def search_thread():
            # Acquire the lock
            lock.acquire()
            try:
                results = self.google_search.display_results(response)
                for key, value in results.items():
                    name = f'{key}.png'
                    downloader.download_image(value, self.positive_path.get(), name)
                    self.completed_count += 1
                    self.show_error(f"Completed: {self.completed_count}/{num}")

                    self.progress_bar.after(0, self.update_progress_bar, self.completed_count, num)
            finally:
                # Release the lock
                lock.release()

        # Create and start a new thread
        thread = threading.Thread(target=search_thread)
        thread.start()


    def update_progress_bar(self, completed_count, num):
        current_value = self.progress_bar['value']
        self.progress_bar['value'] = current_value + 1
        self.progress_bar.update()
        if completed_count >= num:
            # If all images have been processed, perform any necessary cleanup or additional actions here
            pass
    def download_image_thread(self, downloader, url, filename, total_images):
        self.progress_bar.start()
        downloader.download_image(url, self.positive_path.get(), filename)
        self.progress_bar.stop()
        self.progress_bar.step(self.google_search.get_i())  # Increment progress bar value
        if self.progress_bar['value'] == total_images:
            print("All images downloaded.")  # All images downloaded

    def show_error(self, error):
        self.error_label.config(state=tk.NORMAL)
        self.error_label.insert(tk.END, "\n"+error)
        self.error_label.config(state=tk.DISABLED)
        self.error_label.see(tk.END)

    def run(self):
        self.window.mainloop()

    def clean_folder(self, folder):
        # Check if the folder exists
        if not os.path.exists(folder):
            # Create the folder if it doesn't exist
            os.makedirs(folder)
            self.show_error("Folder created successfully.")
        # Check if the folder is empty
        if not os.listdir(folder):
            self.show_error("Folder is empty.")
            return

        # Remove all files and subdirectories within the folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        self.show_error("Folder cleared successfully.")

tkinter_window = MyTkinterWindow()
tkinter_window.run()
