import socket
import threading
from graphics import *
import queue

# Create a global variable to hold the graphics window and text fields
win = None
my_rec = []
text_boxes = []

message_queue = queue.Queue()  # Queue to handle messages from server to GUI


# Function to handle each ESP32 connection
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")

    while True:
        try:
            # Receive data from the ESP32
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            print(f"Received from {client_address}: {data}")
            #message_queue.put(f"{client_address}: {data}")  # Add message to queue
            message_queue.put(f" {data}")
            # Optionally, send a response back to the ESP32
            client_socket.sendall("Data received\n".encode())

        except ConnectionResetError:
            print(f"Connection with {client_address} closed")
            break

    client_socket.close()


# Function to set up the server and accept connections#
def start_server(host="0.0.0.0", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        #Create a new thread for each ESP32 connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


# Function to update the graphics window with new messages
def update_display():
    global text_boxes, win
    global my_rec
    while not message_queue.empty():  # Process all messages in the queue
        message = message_queue.get()


        if message.find("kitchen") != -1:
            text_boxes[0].setText(message)

        if message.find("bedroom") != -1:
            text_boxes[1].setText(message)

        if message.find("dining") != -1:
             text_boxes[2].setText(message)

        if message.find("office") != -1:
            text_boxes[3].setText(message)

        if message.find("living") != -1:
            text_boxes[4].setText(message)

        if message.find("basement") != -1:
            text_boxes[5].setText(message)

        if message.find("nan") != -1:
             text_boxes[7].setText(message)


            # Function to initialize the graphics window and text boxes
def setup_window():
    global win, text_boxes
    global win, my_rec
    win = GraphWin("ESP32 Messages", 900, 500)  # Create the window
    win.setBackground("cyan")



    i = 1
    for x in range (4):
        for y in range (6):

            rect = Rectangle(Point(20 + x * 200, 20 + y * 50), Point(200 + x * 200, 50 + y * 50))
            rect.setFill(color_rgb(200,200,0))
            rect.draw(win)

            my_rec.append(rect)
            i += 1

        for i in range(len(my_rec)):
            my_rec[i].setFill(color_rgb(255, 0, 0))  # Change fill color to red for each rectangle
            my_rec[i].setOutline("black")  # Set the outline to black

    # Create text boxes to display messages (adjust number based on your needs)

    for i in range(8):
        message_box = Text(Point(450, 35 + i * 50), "")  # Place them vertically
        message_box.setSize(12)
        message_box.setTextColor("blue")
        message_box.draw(win)
        text_boxes.append(message_box)


# Main function to run the graphics window and server
def run_gui_and_server():
    # Set up the graphics window
    setup_window()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # This ensures the server thread will exit when the program does
    server_thread.start()

    # Main GUI loop
    while True:
        update_display()  # Continuously check and update messages
        if win.checkMouse():  # Check if the window is clicked to close it
            break

    win.close()


if __name__ == "__main__":
    run_gui_and_server()

