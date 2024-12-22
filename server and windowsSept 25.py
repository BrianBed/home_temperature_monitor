import socket
import threading
from graphics import *
import queue

# Create a global variable to hold the graphics window and text fields
#win = None
my_rec = []
text_boxes = []
no_good = Text(Point(500, 700), "")
#input_box = None
setpoint_boxes = []
room_id = []

message_queue = queue.Queue()  # Queue to handle messages from server to GUI


#win.close()

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


def display_data(num, location, d1, d2, d3, d4):
    #global temperature, humidity, heat_part, time_part
    text_boxes[num].setText(location)
    text_boxes[num + 7].setText(f"Temperature: {d1}C")
    text_boxes[num + 14].setText(f"Humidity: {d2}%")
    text_boxes[num + 21].setText(f"Heat index: {d3}")
    text_boxes[num + 28].setText(f"Time: {d4}")


# Function to update the graphics window with new messages
def update_display():
    global text_boxes, win
    global my_rec
    global temperature
    global no_good

    while not message_queue.empty():  # Process all messages in the queue
        message = message_queue.get()

        # Check if there's an invalid value in the message
        if message.find("nanC") != -1:
            # print(f"Before updating wrong_box, its current text: {wrong_box.getText()}")
            if no_good is not None:  # Ensure wrong_box is initialized
                no_good.setText(message)  # Set the message in the wrong_box
                continue

        try:
            # Split the string to isolate the relevant parts
            parts = message.split(",")

            print(parts)

            if len(parts) != 5:
                print("Error: Message does not have the expected format.")
                continue

            # Extract temperature
            if "Temp:" in parts[1]:
                temp_part = parts[1].split("Temp: ")[1]  # Get the part after "Temp: "
                temperature = temp_part[:-1]  # Remove the 'C'
            else:
                print("Error: Temperature information missing.")
                continue

            # Extract humidity
            if "Humidity:" in parts[2]:
                humidity_part = parts[2].split("Humidity: ")[1]  # Get the part after "Humidity: "
                humidity = humidity_part[:-1]  # Remove the '%'
            else:
                print("Error: Humidity information missing.")
                continue

            # Extract heat index
            if "heat" in parts[3]:
                heat_part = parts[3].split("heat index: ")[1]  # Get the part after "Time: "
            else:
                print("Error: heat index"
                      " information missing.")
                continue

            # Extract time
            if "Time:" in parts[4]:
                time_part = parts[4].split("Time: ")[1]  # Get the part after "Time: "
            else:
                print("Error: Time information missing.")
                continue

            if message.find("kitchen") != -1:
                display_data(2, "kitchen", temperature, humidity, heat_part, time_part)

            if message.find("bedroom") != -1:
                display_data(4, "bedroom", temperature, humidity, heat_part, time_part)

            if message.find("dining") != -1:
                display_data(3, "dining room", temperature, humidity, heat_part, time_part)

            if message.find("office") != -1:
                display_data(0, "office", temperature, humidity, heat_part, time_part)

            if message.find("living") != -1:
                display_data(1, "living room", temperature, humidity, heat_part, time_part)

            if message.find("basement") != -1:
                display_data(5, "basement", temperature, humidity, heat_part, time_part)

            if message.find("outside") != -1:
                display_data(6, "outside", temperature, humidity, heat_part, time_part)

        except IndexError:
            print("Error: Unable to process message.")

            # Function to initialize the graphics window and text boxes


def setup_window():
    global win, text_boxes, my_rec, no_good, setpoint_boxes, input_box, close_box

    win = GraphWin("Home Temperature", 1025, 550)  # Create the window
    win.setBackground("cyan")

    rooms = ["office", "living room", "kitchen", "dining room", "bedroom", "basement", "outside"]

    # Create an input box for user input
    input_box = Entry(Point(510, 500), 6)  # Create an entry box
    input_box.setSize(12)
    input_box.draw(win)
    input_box.setText("22.0")

    for i in range(6):
        message_box = Text(Point(150 + i * 150, 425), "set")  # Place them horizontally
        message_box.setSize(12)
        message_box.setTextColor("blue")
        message_box.draw(win)
        setpoint_boxes.append(message_box)

    for i in range(6):
        message_box = Text(Point(150 + i * 150, 400), rooms[i])  # Place them horizontally
        message_box.setSize(12)
        message_box.setTextColor("blue")
        message_box.draw(win)
        room_id.append(message_box)

    close_box = Text(Point(200, 460), "CLOSE NOW")  # Place them horizontally
    close_box.setSize(12)
    close_box.setTextColor("orange")
    close_box.draw(win)
    #setpoint_boxes.append(message_box)

    message_box = Text(Point(500, 460), "ClearError")  # Place them horizontally
    message_box.setSize(12)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)

    message_box = Text(Point(700, 460), "Clear all")  # Place them horizontally
    message_box.setSize(12)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)

    i = 1
    for x in range(5):
        for y in range(7):
            rect = Rectangle(Point(20 + x * 200, 20 + y * 50), Point(200 + x * 200, 50 + y * 50))
            rect.setFill(color_rgb(200, 200, 0))
            rect.draw(win)
            my_rec.append(rect)
            i += 1

        for i in range(len(my_rec)):
            my_rec[i].setFill(color_rgb(255, 0, 0))  # Change fill color to red for each rectangle
            my_rec[i].setOutline("black")  # Set the outline to black

    no_good = Text(Point(500, 370), "")
    no_good.setTextColor("red")
    no_good.setSize(12)
    no_good.draw(win)
    no_good.setText("no error")

    # Create text boxes to display messages (adjust number based on your needs)

    for x in range(5):
        for y in range(7):
            message_box = Text(Point(110 + x * 200, 35 + y * 50), "")  # Place them vertically
            message_box.setSize(12)
            message_box.setTextColor("blue")
            message_box.draw(win)
            text_boxes.append(message_box)


def close_win():
    global win
    win.close()


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
        global input_box, close_box
        global setpoint_boxes

        update_display()
        click_point = win.checkMouse()  # Wait for mouse click (blocking)
        keyStop = win.checkKey()
        if keyStop == "x":
            close_win()
            break
        # Ignore clicks on the input box

        #if input_box.getAnchor().getX() - 100 < click_point.getX() < input_box.getAnchor().getX() + 100 and \
        #input_box.getAnchor().getY() - 10 < click_point.getY() < input_box.getAnchor().getY() + 10:
        #$continue

        input_x = 200
        input_y = 460
        if click_point is not None:
            if input_x - 100 < click_point.getX() < input_x + 100 and \
                    input_y - 10 < click_point.getY() < input_y + 10:
                close_win()
                break

        input_x = 500
        input_y = 460
        if click_point is not None:
            if input_x - 100 < click_point.getX() < input_x + 100 and \
                    input_y - 10 < click_point.getY() < input_y + 10:
                no_good.setText("no error Now")

        input_x = 700
        input_y = 460
        if click_point is not None:
            if input_x - 100 < click_point.getX() < input_x + 100 and \
                    input_y - 10 < click_point.getY() < input_y + 10:
                continue


if __name__ == "__main__":
    run_gui_and_server()

