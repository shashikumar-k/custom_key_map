import tkinter as tk
import os

# Define the mapping of keys to Kannada letters for Sargam
key_mappings = {
    "a": "ಸ",
    "s": "ರಿ",
    "d": "ಗ",
    "f": "ಮ",
    "j": "ಪ",
    "k": "ದ",
    "l": "ನಿ",
    ";": "ಸ'"
}

swara_length = 0
file_path = "kannada_swara_output.txt"  # File path for saving/loading the content

# Function to display the mapped Kannada letter or special keys (space, enter, backspace)
def on_key_press(event):
    global swara_length
    char = event.char
    # Handle backspace
    if event.keysym == "BackSpace":
        current_line = int(text_widget.index("insert").split('.')[0])
        if swara_length > 16:
            # If more than one line is typed (more than 16 chars), delete both lines
            text_widget.delete(f"{current_line-1}.0", f"{current_line}.end")
        else:
            # If within the first line, delete just the first line
            text_widget.delete(f"{current_line}.0", f"{current_line}.end")
        swara_length = 0
    # Handle Enter key
    elif event.keysym == "Return":
        text_widget.insert(tk.END, '|\n')
        swara_length = 0
    # Handle space
    elif event.keysym == "space":
        text_widget.insert(tk.END, ' | ')
    # Handle mapped characters
    elif char in key_mappings:
        text_widget.insert(tk.END, key_mappings[char])
        # Automatically insert a pipe after every four characters
        swara_length += 1
        if swara_length % 4 == 0:
            text_widget.insert(tk.END, ' | ')
        if swara_length % 16 == 0:
            text_widget.delete("insert-1c")
            text_widget.insert(tk.END, '|\n')
        if swara_length == 32:
            text_widget.insert(tk.END, '\n')
            swara_length = 0
    # Scroll to the bottom to ensure visibility of the latest text
    text_widget.see(tk.END)
    # Prevent unmapped keys from being inserted
    return "break"  # Block unmapped keys

# Function to save the content of the text widget to a text file
def save_to_file():
    content = text_widget.get("1.0", tk.END)  # Get all the content of the text widget
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)  # Write the content to the file

# Function to load content from the file when the window starts
def load_from_file():
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_widget.insert(tk.END, content)  # Load the file content into the text widget

# Create a basic tkinter window
root = tk.Tk()
root.title("Kannada Swara Mapper")
root.geometry("900x600")

# Create a frame to hold the text widget and scrollbar
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Add a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget to display the typed characters
text_widget = tk.Text(frame, font=("Arial", 20), wrap=tk.WORD, insertbackground="black", yscrollcommand=scrollbar.set)
text_widget.pack(expand=True, fill=tk.BOTH)

# Attach the scrollbar to the text widget
scrollbar.config(command=text_widget.yview)

# Enable a blinking cursor
text_widget.config(insertontime=600, insertofftime=300)

# Allow selection, backspace, and navigation (Arrow keys)
def allow_selection_and_navigation(event):
    # Allow specific keys like BackSpace, arrow keys, etc.
    if event.keysym in ["BackSpace", "Left", "Right", "Up", "Down", "Shift_L", "Shift_R", "Control_L", "Control_R"]:
        return  # Allow these keys to work
    return "break"  # Block everything else

# Bind key press event to the function
root.bind("<Key>", on_key_press)

# Load the content from file when the application starts
load_from_file()

# Save the content to file when the window is closed
root.protocol("WM_DELETE_WINDOW", lambda: (save_to_file(), root.destroy()))

# Allow mouse click, key release, and focus-related events while blocking unwanted behavior
text_widget.bind("<Button-1>", allow_selection_and_navigation)
text_widget.bind("<KeyRelease>", allow_selection_and_navigation)
text_widget.bind("<FocusIn>", allow_selection_and_navigation)

# Run the tkinter event loop
root.mainloop()
