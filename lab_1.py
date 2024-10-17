import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from math import ceil
from PIL import ImageTk, Image, ImageOps, ImageEnhance, ImageFilter

class App():
    def __init__(self, root, main_frame=None, photo_frame=None, buttons_frame=None, 
                 add_pic_button=None, photo_holder=None, remove_pic_button=None, 
                 invert_colors=None, extracted_image=None, tkinter_image=None,
                 gamma_selector=None, color_selector=None, sharpness_selector=None,
                 contrast_selector=None, blur_selector=None, emboss_selector=None, 
                 modified_image=None, placeholder_image=None, unfiltered_image=None,
                 kwargs=[]) -> None:
        # frames
        self.root = root
        self.main_frame = main_frame
        self.photo_frame = photo_frame
        self.buttons_frame = buttons_frame
        self.photo_holder = photo_holder
        
        # buttons
        self.add_pic_button = add_pic_button
        self.remove_pic_button = remove_pic_button
        self.invert_colors = invert_colors
        self.gamma_selector = gamma_selector
        self.color_selector = color_selector
        self.contrast_selector = contrast_selector
        self.sharpness_selector = sharpness_selector
        self.blur_selector = blur_selector
        self.emboss_selector = emboss_selector
        
        #images
        self.extracted_image = extracted_image
        self.modified_image = modified_image
        self.placeholder_image = placeholder_image
        self.unfiltered_image = unfiltered_image
        self.tkinter_image = tkinter_image
        self.image_reference_name = None
                
        #modifications track
        self.kwargs = kwargs
        
    def build_Window(self):
        # main frame
        self.main_frame = tk.Frame(self.root, highlightbackground='red', highlightthickness=2, height=self.root.winfo_height(), width=self.root.winfo_width())
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        # left window part
        self.photo_frame = tk.Frame(self.main_frame, highlightbackground='blue', highlightthickness=2, height=self.root.winfo_height(), width=self.root.winfo_width())
        self.photo_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        # right window part
        self.buttons_frame = tk.Frame(self.main_frame, highlightbackground='green', highlightthickness=2, height=self.root.winfo_height(), width=150)
        self.buttons_frame.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        
        # making window resizable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=10)  # left/right ratio
        self.main_frame.grid_columnconfigure(1, weight=2, minsize=200)  # input fields grid is smaller
        self.main_frame.grid_rowconfigure(0, weight=1)     # height resizing

        
        # buttons
        self.add_pic_button = tk.Button(self.photo_frame, text="Choose local image", command=self.get_image, width=20)
        self.add_pic_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.remove_pic_button = tk.Button(self.buttons_frame, text="Remove image", command=self.remove_image, state=tk.DISABLED, width=20)
        self.remove_pic_button.grid(row=12, column=0, padx=2, pady=3)
        
        self.save_pic_button = tk.Button(self.buttons_frame, text="Save image", command=self.save_image, state=tk.DISABLED, width=20)
        self.save_pic_button.grid(row=13, column=0, padx=2, pady=3)

        self.invert_colors = tk.Button(self.buttons_frame, text="Invert image colors", command=self.invert_image_colors, state= tk.DISABLED, width=20)
        self.invert_colors.grid(row=0, column=0, padx=2, pady=3)
        
        
        # sliders
        
        # gamma slider
        g_slider = tk.Label(self.buttons_frame, text="Brightness (1.00)")
        self.gamma_selector = ttk.Scale(self.buttons_frame, from_=0, to=500,  orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        self.gamma_selector.config(command = lambda value: self.modify_image(value, function=ImageEnhance.Brightness, text_value=("Brightness", g_slider, self.gamma_selector)), value=100)
        g_slider.grid(row=1, column=0,  padx=2)
        self.gamma_selector.grid(row=2, column=0,  padx=2)
        
        # color slider
        cl_slider = tk.Label(self.buttons_frame, text="Color (1.00)")
        self.color_selector = ttk.Scale(self.buttons_frame, from_=0, to=500,  orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        self.color_selector.config(command = lambda value: self.modify_image(value, function=ImageEnhance.Color, text_value=("Color", cl_slider)), value=100)
        self.color_selector.grid(row=4, column=0,  padx=2, pady=3)
        cl_slider.grid(row=3, column=0,  padx=2)
        
        # contrast slider
        con_slider = tk.Label(self.buttons_frame, text="Contrast (1.00)")
        self.contrast_selector = ttk.Scale(self.buttons_frame, from_=0, to=500, orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        self.contrast_selector.config(command = lambda value: self.modify_image(value, function=ImageEnhance.Contrast, text_value=("Contrast", con_slider)), value=100)
        self.contrast_selector.grid(row=6, column=0,  padx=2, pady=3)
        con_slider.grid(row=5, column=0,  padx=2)
        
        # sharpness slider
        shrp_slider = tk.Label(self.buttons_frame, text="Sharpness (1.00)")
        self.sharpness_selector = ttk.Scale(self.buttons_frame, from_=-500, to=500,orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        self.sharpness_selector.config(command = lambda value: self.modify_image(value, function=ImageEnhance.Sharpness, text_value=("Sharpness", shrp_slider)), value=100)
        self.sharpness_selector.grid(row=8, column=0,  padx=2, pady=3)
        shrp_slider.grid(row=7, column=0,  padx=2)
        
        # blur filter
        blur_slider = tk.Label(self.buttons_frame, text="Blur (0.00)")
        self.blur_selector = ttk.Scale(self.buttons_frame, from_=0, to=1000,orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        self.blur_selector.config(command = lambda value: self.modify_image(value, function=ImageFilter.GaussianBlur, text_value=("Blur", blur_slider)), value=0)
        self.blur_selector.grid(row=10, column=0,  padx=2, pady=3)
        blur_slider.grid(row=9, column=0,  padx=2)
        
        # embossment filter
        # emboss_slider = tk.Label(self.buttons_frame, text="Embossment (0.00)")
        # self.emboss_selector = ttk.Scale(self.buttons_frame, from_=0, to=1000,orient=tk.HORIZONTAL, state=tk.DISABLED, length=150)
        # self.emboss_selector.config(command = lambda value: self.modify_image(value, func=ImageFilter.EMBOSS, text_value=("Embossment", emboss_slider)), value=0)
        # self.emboss_selector.grid(row=12, column=0,  padx=2, pady=3)
        # emboss_slider.grid(row=11, column=0,  padx=2)
    
    def display_image(callback):
        current_func = None

        def wrapper(*args, **kwargs):
            nonlocal current_func
            self = args[0]
            
            # Assuming 'function' is passed in kwargs to identify which function is active
            if current_func != kwargs['function']:
                current_func = kwargs["function"]
                
                effect_methods = {
                    "Brightness": (ImageEnhance.Brightness, self.gamma_selector),
                    "Color": (ImageEnhance.Color, self.color_selector),
                    "Contrast": (ImageEnhance.Contrast, self.contrast_selector),
                    "Sharpness": (ImageEnhance.Sharpness, self.sharpness_selector),
                    "Blur": (ImageFilter.GaussianBlur, self.blur_selector),
                }
                
                self.modified_image = self.extracted_image.copy()
                
                for _, (effect_class, selector) in effect_methods.items():
                    
                    effect_value = float(selector.get()) / 100
                    
                    if effect_class.__module__ == "PIL.ImageEnhance" and effect_class.__name__ != current_func.__name__:
                        # Update the modified image with the selected effect
                        effect_enhancer = effect_class(self.modified_image)
                        self.modified_image = effect_enhancer.enhance(effect_value)
                    elif effect_class.__module__ == "PIL.ImageFilter" and effect_class.__name__ != current_func.__name__:
                        # Apply the filter effect
                        effected_image = self.modified_image.filter(effect_class(effect_value))
                        self.modified_image = effected_image

            # Call the callback function (the original method)
            callback(*args, **kwargs)
            
            # Update the tkinter image display
            self.tkinter_image = ImageTk.PhotoImage(self.placeholder_image)
            self.photo_holder.config(image=self.tkinter_image)
        
        return wrapper

    def resize_image(self, event):
        #self.photo_frame.unbind("<Configure>")
        
        frame_h, frame_w = self.photo_frame.winfo_height(), self.photo_frame.winfo_width()
        img_w, img_h = self.extracted_image.size
        
        scale_w = min(frame_w / img_w, 1.0)
        scale_h = min(frame_h / img_h, 1.0)
        
        resized = self.extracted_image.resize((ceil(img_w*scale_w), ceil(img_h*scale_h)), Image.Resampling.BICUBIC)
        
        self.modified_image = resized
        self.extracted_image = resized
        self.tkinter_image = ImageTk.PhotoImage(self.modified_image)
        self.photo_holder.config(image=self.tkinter_image)    
        
        #self.photo_frame.bind("<Configure>", self.resize_image)
        
    def get_image(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("Picture Files", ".jpg .png .webp .svg")])
        if filename:
            self.extracted_image = Image.open(filename).convert("RGBA")
            self.modified_image = self.extracted_image.copy()
            self.placeholder_image = self.modified_image.copy()
            self.unfiltered_image = self.placeholder_image.copy()
            self.tkinter_image = ImageTk.PhotoImage(self.modified_image)
            self.image_reference_name = filename.split('/')[-1]
            
            # hide add button
            self.add_pic_button.place_forget()
            # show remove button

            self.photo_holder = tk.Label(self.photo_frame, image=self.tkinter_image)
            self.photo_holder.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            #enable button pack
            self.invert_colors.config(state="normal")
            self.remove_pic_button.config(state="normal")
            self.gamma_selector.config(state="normal")
            self.color_selector.config(state="normal")
            self.sharpness_selector.config(state="normal")
            self.contrast_selector.config(state="normal")
            self.blur_selector.config(state="normal")
            self.save_pic_button.config(state="normal")
            #self.emboss_selector.config(state="normal")
            
            # pic resize 
            self.resize_image(None)
            
    def remove_image(self):
        self.kwargs = []
        self.extracted_image = None
        self.modified_image = None
        self.placeholder_image = None
        self.tkinter_image = None
        self.main_frame.destroy()
        self.build_Window()
    
    def save_image(self):
        # Open a file dialog to select the save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="modified_" + self.image_reference_name,
            filetypes=[("All files", "*.*")],
            title="Save an image"
        )
        if file_path:
            try:
                # Save the modified image
                self.placeholder_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
        
    
    def invert_image_colors(self): 
        try:
            r, g, b, a =  self.modified_image.split()

            # Merge the RGB channels back and invert them
            rgb_image = Image.merge("RGB", (r, g, b))
            inverted_rgb = ImageOps.invert(rgb_image)

            # Combine the inverted RGB channels with the original alpha channel
            self.modified_image = Image.merge("RGBA", (*inverted_rgb.split(), a))
        except ValueError:
            self.modified_image = ImageOps.invert(self.modified_image)
        
        # Convert the inverted image back to ImageTk.PhotoImage
        self.tkinter_image = ImageTk.PhotoImage(self.modified_image)
        
        self.photo_holder.config(image=self.tkinter_image)
    
    @display_image
    def modify_image(self, value, function, text_value):
        try:
            effect_enhancement = function(self.modified_image.copy())
            effect_value = float(value) / 100
            self.placeholder_image = effect_enhancement.enhance(effect_value)
        except AttributeError:
            effect_value = float(value) / 100
            self.placeholder_image = self.modified_image.copy().filter(function(effect_value))
        
        text_value[1].config(text=f"{text_value[0]} ({effect_value:.2f})")
        

        
if __name__ == "__main__":
    
    root = tk.Tk()
    root.state("zoomed")  # init window size height x width
    root.resizable(True, True)
    root.title("Picture Editor")
    root.update()
    app = App(root)
    app.build_Window()
    root.mainloop()