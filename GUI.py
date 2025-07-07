import tkinter as tk
from tkinter import ttk
import pandas as pd
import socket

# Load the CSV file
file_path = 'finalChannelList.csv'
channel_data = pd.read_csv(file_path)

# Define functions to filter different types of channels
def filter_analog_channels(data):
    return data[data['unitType'].str.contains('analog', case=False, na=False)]

def filter_digital_input_channels(data):
    return data[data['unitType'].str.contains('DI', case=False, na=False)]

def filter_digital_output_channels(data):
    return data[data['unitType'].str.contains('DO', case=False, na=False)]

def filter_j1939_channels(data):
    return data[data['unitType'].str.contains('J1939', case=False, na=False)]

# Function to read data from cRIO over Ethernet
def read_crio_data(ip, port, channel_id):
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            # Send a request for the specific channel data
            request_message = f"GET {channel_id}\n"
            s.sendall(request_message.encode())
            # Receive the response from the cRIO
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return f"Error reading {channel_id}: {e}"

# Define the GUI application
class ChannelReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("cRIO Channel Reader")

        # IP address and port input
        self.ip_label = ttk.Label(root, text="cRIO IP Address:")
        self.ip_label.pack(pady=2)
        self.ip_entry = ttk.Entry(root)
        self.ip_entry.pack(pady=2)
        self.ip_entry.insert(0, "192.168.1.100")  # Default IP address

        self.port_label = ttk.Label(root, text="Port:")
        self.port_label.pack(pady=2)
        self.port_entry = ttk.Entry(root)
        self.port_entry.pack(pady=2)
        self.port_entry.insert(0, "12345")  # Default port

        self.connect_button = ttk.Button(root, text="Connect", command=self.connect_to_crio)
        self.connect_button.pack(pady=10)

        # Create a notebook for tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Create frames for each type of channel
        self.analog_frame = ttk.Frame(self.notebook, width=400, height=280)
        self.di_frame = ttk.Frame(self.notebook, width=400, height=280)
        self.do_frame = ttk.Frame(self.notebook, width=400, height=280)
        self.j1939_frame = ttk.Frame(self.notebook, width=400, height=280)

        self.analog_frame.pack(fill='both', expand=True)
        self.di_frame.pack(fill='both', expand=True)
        self.do_frame.pack(fill='both', expand=True)
        self.j1939_frame.pack(fill='both', expand=True)

        # Add frames to notebook
        self.notebook.add(self.analog_frame, text='Analog Channels')
        self.notebook.add(self.di_frame, text='DI Channels')
        self.notebook.add(self.do_frame, text='DO Channels')
        self.notebook.add(self.j1939_frame, text='J1939 Channels')

    def connect_to_crio(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        self.add_channel_data_display(ip, port)

    def add_channel_data_display(self, ip, port):
        self.clear_frames()
        self.add_channels_to_frame(self.analog_frame, filter_analog_channels(channel_data), ip, port)
        self.add_channels_to_frame(self.di_frame, filter_digital_input_channels(channel_data), ip, port)
        self.add_channels_to_frame(self.do_frame, filter_digital_output_channels(channel_data), ip, port)
        self.add_channels_to_frame(self.j1939_frame, filter_j1939_channels(channel_data), ip, port)

    def clear_frames(self):
        for frame in [self.analog_frame, self.di_frame, self.do_frame, self.j1939_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

    def add_channels_to_frame(self, frame, channels, ip, port):
        for _, channel in channels.iterrows():
            data = read_crio_data(ip, port, channel['id'])
            label = ttk.Label(frame, text=f"{channel['name']} ({channel['id']}): {data}")
            label.pack(pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    app = ChannelReaderApp(root)
    root.mainloop()
