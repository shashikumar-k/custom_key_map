import tkinter as tk

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

# Function to display the mapped Kannada letter or special keys (space, enter, backspace)
def on_key_press(event):
    char = event.char
    # Handle backspace
    if event.keysym == "BackSpace":
        text_widget.delete("insert-1c")
    # Handle Enter key
    elif event.keysym == "Return":
        text_widget.insert(tk.END, ' ||\n')
    # Handle space
    elif event.keysym == "space":
        text_widget.insert(tk.END, ' | ')
    # Handle mapped characters
    elif char in key_mappings:
        text_widget.insert(tk.END, key_mappings[char])
    # Prevent unmapped keys from being inserted
    return "break"  # Block unmapped keys

# Create a basic tkinter window
root = tk.Tk()
root.title("Kannada Swara Mapper")
root.geometry("900x600")

# Create a text widget to display the typed characters
text_widget = tk.Text(root, font=("Arial", 20), wrap=tk.WORD, insertbackground="black")
text_widget.pack(expand=True, fill=tk.BOTH)

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

# Allow mouse click, key release, and focus-related events while blocking unwanted behavior
text_widget.bind("<Button-1>", allow_selection_and_navigation)
text_widget.bind("<KeyRelease>", allow_selection_and_navigation)
text_widget.bind("<FocusIn>", allow_selection_and_navigation)

# Run the tkinter event loop
root.mainloop()
