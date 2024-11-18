import pyautogui
from pynput import mouse, keyboard
import threading
import time
import tkinter as tk

class ScreenshotTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        
        self.rect_id = None
        self.screenshot_count = 0
        
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)  # Fullscreen window
        self.root.attributes("-alpha", 0.3)        # Transparent window
        self.root.config(bg="black")               # Black background

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        self.root.mainloop()
        
    def on_mouse_press(self, event):
        # Record the starting position
        self.start_x = event.x
        self.start_y = event.y
        # Create a rectangle
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        # Update the rectangle as the mouse is dragged
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        # Get the rectangle's coordinates
        self.end_x, self.end_y = event.x, event.y
        self.root.withdraw()  # Hide the Tkinter window
        self.root.destroy()
        
    def get_coords(self):
        return self.start_x, self.end_x, self.start_y, self.end_y

    def screenshot(self):
        # Capture the screen and crop to the selected area
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)

        # Capture the screen using pyautogui or PIL
        screenshot = pyautogui.screenshot()
        cropped_image = screenshot.crop((x1, y1, x2, y2))

        # Save the cropped image
        cropped_image.save(f"screenshot_{self.screenshot_count}.png")
        self.screenshot_count += 1
        
        print("Screenshot saved as screenshot.png")
        

# Main entry point
if __name__ == "__main__":
    # Start mouse listener
    canvas = ScreenshotTool()

    def on_click(x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
            canvas.screenshot()
        else:
            print(f"Mouse released at ({x}, {y}) with {button}")
    
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    
    def stop_program(mouse_listener):
        """Stop the mouse listener and exit the program."""
        print("Exiting the program...")
        mouse_listener.stop()
    

    def on_key_press(key):
        try:
            # Detect Ctrl+Q
            if key == keyboard.Key.ctrl_l:  # Left Control
                print("Ctrl key pressed")
            elif hasattr(key, 'char') and key.char == 'q':
                print("Ctrl+Q pressed. Exiting...")
                stop_program(mouse_listener)  # Stop the mouse listener
                return False  # Stop the keyboard listener
        except AttributeError:
            pass
    
    with keyboard.Listener(on_press=on_key_press) as keyboard_listener:
        # Keep the program running until the listeners are stopped
        mouse_listener.join()
        keyboard_listener.join()
    

