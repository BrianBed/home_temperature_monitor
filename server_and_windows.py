import socket
import threading

from graphics import *
import queue
import re
import schedule
import time
import datetime
import csv
import math

# Create a threading event to signal the server to stop
stop_event = threading.Event()
# Create a global variable to hold the graphics window and text fields
# win = None
my_rec = []
text_boxes = []
no_good = Text(Point(500, 700), "")
# input_box = None
setpoint_boxes = []
room_id = []
onoff = [False, False, False, False, False, False, False, False]
temp = ["22.5", "22.5", "22.5", "22.5", "22.5", "22.5", "22.5"]
message_queue = queue.Queue()  # Queue to handle messages from server to GUI
server = False
aline = []

hi_today = 0
hi_time = ""
lo_today = 111
lo_time = ""
hi_year = 0
hi_date = ""
lo_year = 111
lo_date = ""
hi_yes = 0
hi_yestime = ""
lo_yes = 111
lo_yestime = ""
center = Point(270, 815)
last_temp = 50.0
new_temp = 0.0
ave_temp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
ave_pointer = 0
askheat = 0
row = 0
visible = True
number_pad = None

# Function to handle each ESP32 connection
def handle_client(client_socket, client_address):
    # print(f"New connection from {client_address}")

    while True:
        try:
            # Receive data from the ESP32
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            print(f"Received from {client_address}: {data}")
            # message_queue.put(f"{client_address}: {data}")  # Add message to queue
            # message_queue.put(f" {data}")
            if len(data) < 12:
                row2 = int(data[0])
                set_p = setpoint_boxes[row2].getText()
                client_socket.sendall(f"{set_p} : {onoff[row2]} : {temp[row2]}".encode())
                print(f"\n\n ****** {row2}")

            message_queue.put(f" {data}")
            # Optionally, send a response back to the ESP32
            # client_socket.sendall("Data received\n".encode())

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

    while not stop_event.is_set():
        client_socket, client_address = server.accept()
        # Create a new thread for each ESP32 connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    print("Shutting down the server...")
    server.close()

def toggle_visibility(objects, visible):
    """Toggles visibility of a group of objects (both button and label)."""
    for obj in objects:
        if visible:
            obj['button'].draw(win)
            obj['label'].draw(win)
        else:
            obj['button'].undraw()
            obj['label'].undraw()


def create_number_pad():
    """Creates a number pad with buttons for digits 0-9, decimal, and clear."""
    # Create a list to store the number buttons
    buttons = []

    # Coordinates for the buttons on the window
    x_start = 1100
    y_start = 700
    button_width = 25
    button_height = 25
    spacing = 10

    # Create buttons for numbers 1-9
    for i in range(1, 10):
        row = (i - 1) // 3
        col = (i - 1) % 3
        x = x_start + col * (button_width + spacing)
        y = y_start + row * (button_height + spacing)
        button = Rectangle(Point(x, y), Point(x + button_width, y + button_height))
        button.setFill("lightblue")
        button.setOutline("black")
        label = Text(Point(x + button_width / 2, y + button_height / 2), str(i))
        label.setSize(16)
        buttons.append({'button': button, 'label': label, 'value': str(i)})

    # Create a button for 0
    button_0 = Rectangle(Point(x_start, y_start + 3 * (button_height + spacing)),
                         Point(x_start + button_width, y_start + 3 * (button_height + spacing) + button_height))
    button_0.setFill("lightblue")
    button_0.setOutline("black")
    label_0 = Text(Point(x_start + button_width / 2, y_start + 3 * (button_height + spacing) + button_height / 2), "0")
    label_0.setSize(16)
    buttons.append({'button': button_0, 'label': label_0, 'value': "0"})

    # Create button for decimal point
    button_dot = Rectangle(Point(x_start + button_width + spacing, y_start + 3 * (button_height + spacing)),
                           Point(x_start + 1 * (button_width + spacing) + button_width,
                                 y_start + 3 * (button_height + spacing) + button_height))
    button_dot.setFill("lightblue")
    button_dot.setOutline("black")
    label_dot = Text(Point(x_start + button_width + spacing + button_width / 2,
                           y_start + 3 * (button_height + spacing) + button_height / 2), ".")
    label_dot.setSize(16)
    buttons.append({'button': button_dot, 'label': label_dot, 'value': "."})

    # Create button for Clear
    button_clear = Rectangle(Point(x_start + 2 * (button_width + spacing), y_start + 3 * (button_height + spacing)),
                             Point(x_start + 2 * (button_width + spacing) + button_width,
                                   y_start + 3 * (button_height + spacing) + button_height))
    button_clear.setFill("lightcoral")
    button_clear.setOutline("black")
    label_clear = Text(Point(x_start + 2 * (button_width + spacing) + button_width / 2,
                             y_start + 3 * (button_height + spacing) + button_height / 2), "C")
    label_clear.setSize(16)
    buttons.append({'button': button_clear, 'label': label_clear, 'value': "C"})

    return buttons


def click_on_button(x, y, buttons):
    """Check if a click (x, y) is within any button's area."""
    for button in buttons:
        rect = button['button']
        top_left = rect.getP1()
        bottom_right = rect.getP2()
        if top_left.getX() <= x <= bottom_right.getX() and top_left.getY() <= y <= bottom_right.getY():
            print(button['value'])
            return button['value']
    return None


def update_textbox(textbox, current_text, value):
    """Update the textbox text with the clicked value."""
    if value == "C":  # Clear the textbox
        textbox.setText("")
    elif value == "." and "." not in current_text:
        textbox.setText(current_text + value)
    elif value != ".":
        textbox.setText(current_text + value)


def draw_line(row1, length):
    aline[row1].undraw()
    aline[row1] = Line(Point(330, 25 + row * 75), Point(330 + length/19, 25 + row * 75))
    aline[row1].setFill("red")
    aline[row1].setWidth(5)
    aline[row1].draw(win)

def initialize():
    global lo_yes, hi_yes, hi_date, lo_date, hi_year, lo_year, hi_yestime, lo_yestime,hi_today, lo_today, hi_time, lo_time
    for k in range(6):
        f = open(f"{rooms[k]}.txt", "r")
        data1 = f.readline().strip()
        data = f.readline().strip()
        f.close()
        # print(data)
        onoff[k] = data == 'True'
        setpoint_boxes[k].setText(data1)
        # print(k)
        # print(onoff[k])

    for k in range(6):
        for i in range(5):
            # print(onoff[k])
            if onoff[k]:
                my_rec[k + i * 7].setFill(color_rgb(0, 255, 0))
            else:
                my_rec[k + i * 7].setFill(color_rgb(255, 0, 0))

    # Only read the last line if the file has more than one line
    if has_more_than_one_line('temperature_stats.csv'):
        last_line = read_last_line('temperature_stats.csv')
        last_line_columns = next(csv.reader([last_line]))
        hi_today = last_line_columns[1]
        hi_time = last_line_columns[2]
        lo_today = last_line_columns[3]
        lo_time = last_line_columns[4]
        hi_yes = last_line_columns[5]
        hi_yestime = last_line_columns[6]
        lo_yes = last_line_columns[7]
        lo_yestime = last_line_columns[8]
        hi_year = last_line_columns[9]
        hi_date = last_line_columns[10]
        lo_year = last_line_columns[11]
        lo_date = last_line_columns[12]


def has_more_than_one_line(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        second_line = file.readline()  # Try reading the second line
    return bool(second_line)  # If there's a second line, return True


def read_last_line(file_name):
    with open(file_name, 'rb') as file:
        # Move the cursor to the second-to-last byte
        file.seek(-2, 2)
        while file.tell() > 1:  # Avoid going before the start of the file
            if file.read(1) == b'\n':  # Stop when a newline is found
                break
            file.seek(-2, 1)  # Move 2 bytes back
        last_line = file.readline().decode('utf-8').strip()  # Read and decode the last line
    return last_line


def display_data(num, location, d1, d2, d3, d4):
    # global temperature, humidity, heat_part, time_part
    text_boxes[num].setText(location)
    text_boxes[num + 7].setText(f"Temperature: {d1}°C")
    text_boxes[num + 14].setText(f"Humidity: {d2}%")
    text_boxes[num + 21].setText(f"Heat index: {d3}")
    text_boxes[num + 28].setText(f"Time: {d4}")
    temp[num] = d1


def update_stats(temp2):
    global hi_today, hi_time, lo_today, lo_time, hi_year, hi_date, lo_year, lo_date

    if hi_today is None or temp2 > float(hi_today):
        hi_today = temp2
        hi_time = datetime.datetime.now().strftime('%H:%M')
    if lo_today is None or temp2 < float(lo_today):
        lo_today = temp2
        lo_time = datetime.datetime.now().strftime('%H:%M')

    if hi_year is None or temp2 > float(hi_year):
        hi_year = temp2
        hi_date = datetime.datetime.now().strftime('%b:%d')
    if lo_year is None or temp2 < float(lo_year):
        lo_year = temp2
        lo_date = datetime.datetime.now().strftime('%b:%d')


def reset_daily_stats():
    global hi_today, lo_today, hi_yes, lo_yes, hi_yestime,lo_yestime
    hi_yes = hi_today
    hi_yestime = hi_time
    lo_yes = lo_today
    lo_yestime = lo_time
    stats_loyes.setText(stats_loyes.getText())
    hi_today = None
    lo_today = None


def reset_yearly_stats():
    global lo_year, hi_year
    lo_year = None
    hi_year = None


def yearly_task():
    current_date = datetime.datetime.now()
    if current_date.month == 1 and current_date.day == 1:
        reset_yearly_stats()


def display_stats():
    stats_hiday.setText(str(hi_today) + "°C : " + hi_time)
    stats_loday.setText(str(lo_today) + "°C : " + lo_time)
    stats_hiyes.setText(str(hi_yes) + "°C : " + hi_yestime)
    stats_loyes.setText(str(lo_yes) + "°C : " + lo_yestime)
    stats_hiyear.setText(str(hi_year) + "°C : " + hi_date)
    stats_loyear.setText(str(lo_year) + "°C: " + lo_date)

def calc_average():
    sum_ave = 0.0
    for i in range(8):
        sum_ave = sum_ave + ave_temp[i]
    return  sum_ave/8

def append_to_file():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("temperature_stats.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [timestamp, hi_today, hi_time, lo_today, lo_time, hi_yes, hi_yestime, lo_yes, lo_yestime, hi_year, hi_date,
             lo_year, lo_date])
        no_good.setText("writing file on the hour")


def write_data(num):
    f = open(f"{rooms[num]}.txt", "w")
    f.write(f"{setpoint_boxes[num].getText()}\n")
    f.write(f"{onoff[num]}")
    print(f"{rooms[num]} + {'  '} {onoff[num]}  {'  set  '}  {setpoint_boxes[num]} ")
    f.close()


def toggle_onoff(num):
    with open(f"{rooms[num]}.txt", "r") as f:
        data1 = f.readline().strip
        data = f.readline().strip
        # onoff[num] = data == 'True'
        # i = 0
        for k in range(5):
            if onoff[num]:
                my_rec[num + k * 7].setFill(color_rgb(255, 0, 0))

            else:
                my_rec[num + k * 7].setFill(color_rgb(0, 255, 0))
            # i = i + 7
    onoff[num] = not onoff[num]
    f = open(f"{rooms[num]}.txt", "w")
    f.write(f"{setpoint_boxes[num].getText()}\n")
    f.write(f"{onoff[num]}")
    print(f"{rooms[num]} + {'  '} {onoff[num]}  {'  set  '}  {setpoint_boxes[num]} ")
    f.close()


# Function to update the graphics window with new messages
def update_display():
    global text_boxes, win, my_rec, temperature, no_good, new_temp, last_temp, ave_pointer, askheat, row

    while not message_queue.empty():  # Process all messages in the queue
        message = message_queue.get()

        # Check if there's an invalid value in the message
        if message.find("nanC") != -1:
            # print(f"Before updating wrong_box, its current text: {wrong_box.getText()}")
            if no_good is not None:  # Ensure wrong_box is initialized
                no_good.setText(message)  # Set the message in the wrong_box
                continue

        if len(message) < 12:
            match = re.search(r'(\d+)[,:](\d+)', message)
            if match:
                row = int(match.group(1))
                askheat = int(match.group(2))
                # print(f"Extracted integer: {integer_value}")
                # send_back(integer_value)
                draw_line(row, askheat)
                print(f"   123456    askheat  {askheat} ' row:' {row}")

                print(f"                        askheat: {askheat}")


            else:
                print("No integer found in the string")
            break




        try:
            # Split the string to isolate the relevant parts
            parts = message.split(",")

            print(parts)

            if len(parts) != 5:
                no_good.setText("Error: Message does not have the expected format.")  # Set the message in the wrong_box
                continue

            # Extract temperature
            if "Temp:" in parts[1]:
                temp_part = parts[1].split("Temp: ")[1]  # Get the part after "Temp: "
                temperature = temp_part[:-1]  # Remove the 'C'
            else:
                no_good.setText("Error: Temperature information missing.")
                continue

            # Extract humidity
            if "Humidity:" in parts[2]:
                humidity_part = parts[2].split("Humidity: ")[1]  # Get the part after "Humidity: "
                humidity = humidity_part[:-1]  # Remove the '%'
            else:
                no_good.setText("Error: Humidity information missing.")
                continue

            # Extract heat index
            if "heat" in parts[3]:
                heat_part = parts[3].split("heat index: ")[1]  # Get the part after "Time: "
            else:
                no_good.setText("Error: heat index  -   information missing")
                continue

            # Extract time
            if "Time:" in parts[4]:
                time_part = parts[4].split("Time: ")[1]  # Get the part after "Time: "
            else:
                no_good.setText("Error: Time information missing.")
                continue

            timestamp = datetime.datetime.now().strftime('%H:%M:%S')

            if message.find("kitchen") != -1:
                display_data(2, "kitchen", temperature, humidity, heat_part, timestamp)

            if message.find("bedroom") != -1:
                display_data(4, "bedroom", temperature, humidity, heat_part, timestamp)

            if message.find("dining") != -1:
                display_data(3, "dining room", temperature, humidity, heat_part, timestamp)

            if message.find("office") != -1:
                display_data(0, "office", temperature, humidity, heat_part, timestamp)

            if message.find("living") != -1:
                display_data(1, "living room", temperature, humidity, heat_part, timestamp)

            if message.find("basement") != -1:
                display_data(5, "basement", temperature, humidity, heat_part, timestamp)

            if message.find("outside") != -1:
                display_data(6, "outside", temperature, humidity, heat_part, timestamp)
                update_stats(float(temperature))
                display_stats()
                new_temp = float(temperature)

                ave_temp[ave_pointer] = new_temp
                ave_pointer = ave_pointer + 1
                if ave_pointer > 7:
                    ave_pointer = 0



                print(calc_average())

        except IndexError:
            no_good.setText("Error: Unable to process message.")

            # Function to initialize the graphics window and text boxes

def calc_angle():
    global last_temp,arrow,t_display
    temp_change = calc_average()
    if last_temp == 50.0:
        last_temp = temp_change
    change = temp_change - last_temp
    if change > 0.9:
        change = 0.9
    if change < -0.9:
        change = -0.9

    if change > 0:
        color = "green"
    elif change < 0:
        color = "red"
    else:
        color = "white"
    print("change: " + str(change) + "  new temp: " + str(temp_change) + "  last temp: " + str(last_temp))
    angle = change * 100  # Positive goes counterclockwise, negative clockwise (corrected)
    t_display.setText(round(change,2))
    last_temp = temp_change
    arrow = update_arrow(arrow, center, angle, color)

# Function to update the arrow direction
def update_arrow(arrow, center, angle, color):
    length = 38  # length of the arrow
    radians = math.radians(angle)
    x_end = center.getX() + length * math.cos(radians)
    y_end = center.getY() - length * math.sin(radians)  # inverted y-axis in graphics.py

    # Update the arrow's endpoint
    arrow.undraw()  # Remove the previous arrow
    new_arrow = Line(center, Point(x_end, y_end))
    new_arrow.setArrow('last')  # Draw arrow at the end of the line
    new_arrow.setWidth(5)
    new_arrow. setFill(color)
    new_arrow.draw(win)
    return new_arrow



def setup_window():
    global win, text_boxes, my_rec, no_good, setpoint_boxes, input_box, close_box, rooms, stats_hiday, stats_loday, stats_hiyes, stats_loyes, stats_hiyear, stats_loyear,arrow, t_display, last_temp
    global aline, number_pad, textbox_label, current_text

    win = GraphWin("Home Temperature Monitor", 1530, 1000)  # Create the window
    win.setBackground("cyan")
    win.master.geometry("+50+50")

    rooms = ["office", "living room", "kitchen", "dining room", "bedroom", "basement", "outside"]

    # Create heat lines
    for i in range(6):
        my_line = Line(Point(330, 25 + i * 75), Point(330, 25 + i * 75))
        my_line.setFill("red")
        my_line.setWidth(5)
        my_line.draw(win)
        aline.append(my_line)

    set_box = Text(Point(750, 725), "SET")
    set_box.setSize(14)
    set_box.setTextColor("black")
    set_box.draw(win)

    for i in range(6):
        message_box = Text(Point(150 + i * 240, 660), "set")  # Place them horizontally
        message_box.setSize(18)
        message_box.setTextColor("blue")
        message_box.draw(win)
        setpoint_boxes.append(message_box)

        message_box = Text(Point(150 + i * 240, 625), rooms[i])  # Place them horizontally
        message_box.setSize(18)
        message_box.setTextColor("blue")
        message_box.draw(win)
        room_id.append(message_box)

    # for i in range(6):
    # write_data(i)

    close_box = Text(Point(200, 725), "CLOSE")  # Place them horizontally
    close_box.setSize(16)
    close_box.setTextColor("black")
    close_box.draw(win)
    # setpoint_boxes.append(message_box)

    message_box = Text(Point(1000, 725), "ClearError")  # Place them horizontally
    message_box.setSize(16)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)


    i = 1
    for x in range(5):
        for y in range(7):
            rect = Rectangle(Point(30 + x * 300, 30 + y * 75), Point(300 + x * 300, 75 + y * 75))
            rect.setFill(color_rgb(200, 200, 0))
            rect.draw(win)
            my_rec.append(rect)
            i += 1

        for i in range(len(my_rec)):
            my_rec[i].setFill(color_rgb(255, 0, 0))  # Change fill color to red for each rectangle
            my_rec[i].setOutline("black")  # Set the outline to black

    no_good = Text(Point(760, 575), "")
    no_good.setTextColor("red")
    no_good.setSize(16)
    no_good.draw(win)
    no_good.setText("no error")

    # Create text boxes to display messages (adjust number based on your needs)

    for x in range(5):
        for y in range(7):
            message_box = Text(Point(165 + x * 300, 53 + y * 75), "")  # Place them vertically
            message_box.setSize(18)
            message_box.setTextColor("blue")
            message_box.draw(win)
            text_boxes.append(message_box)

    stats_title = Text(Point(760, 840), "OUTSIDE STATS")
    stats_title.setSize(18)
    stats_title.setTextColor("blue")
    stats_title.draw(win)

    stats_hitoday = Text(Point(150, 890), "Hi today")
    stats_hitoday.setSize(18)
    stats_hitoday.setTextColor("blue")
    stats_hitoday.draw(win)

    stats_lotoday = Text(Point(390, 890), "Lo today")
    stats_lotoday.setSize(18)
    stats_lotoday.setTextColor("blue")
    stats_lotoday.draw(win)

    stats_hiyesterday = Text(Point(630, 890), "Hi yesterday")
    stats_hiyesterday.setSize(18)
    stats_hiyesterday.setTextColor("blue")
    stats_hiyesterday.draw(win)

    stats_loyesterday = Text(Point(870, 890), "Lo yesterday")
    stats_loyesterday.setSize(18)
    stats_loyesterday.setTextColor("blue")
    stats_loyesterday.draw(win)

    stats_hi_year = Text(Point(1110, 890), "Hi year")
    stats_hi_year.setSize(18)
    stats_hi_year.setTextColor("blue")
    stats_hi_year.draw(win)

    stats_lo_year = Text(Point(1350, 890), "Lo year")
    stats_lo_year.setSize(18)
    stats_lo_year.setTextColor("blue")
    stats_lo_year.draw(win)

    stats_hiday = Text(Point(150, 925), "hiday")
    stats_hiday.setSize(18)
    stats_hiday.setTextColor("blue")
    stats_hiday.draw(win)

    stats_loday = Text(Point(390, 925), "loday")
    stats_loday.setSize(18)
    stats_loday.setTextColor("blue")
    stats_loday.draw(win)

    stats_hiyes = Text(Point(630, 925), "hiyes")
    stats_hiyes.setSize(18)
    stats_hiyes.setTextColor("blue")
    stats_hiyes.draw(win)

    stats_loyes = Text(Point(870, 925), "loyes")
    stats_loyes.setSize(18)
    stats_loyes.setTextColor("blue")
    stats_loyes.draw(win)

    stats_hiyear = Text(Point(1110, 925), "hiyear")
    stats_hiyear.setSize(18)
    stats_hiyear.setTextColor("blue")
    stats_hiyear.draw(win)

    stats_loyear = Text(Point(1350,925), "loyear")
    stats_loyear.setSize(18)
    stats_loyear.setTextColor("blue")
    stats_loyear.draw(win)

    # draw rectangle for circle
    change_rectangle = Rectangle(Point(80,790), Point(370,840))
    change_rectangle.setFill("black")
    change_rectangle.setOutline("green")
    change_rectangle.draw(win)

    # Create the number pad (list of buttons)

    number_pad = create_number_pad()

    # Draw the number pad
    for button in number_pad:
        button['button'].draw(win)
        button['label'].draw(win)

    # Create the textbox to display the input
    textbox_rect = Rectangle(Point(800, 712), Point(860, 737))
    textbox_rect.setFill("white")
    textbox_rect.setOutline("black")
    textbox_rect.draw(win)

    textbox_label = Text(Point(830, 727), "22.5")
    textbox_label.setSize(16)
    textbox_label.draw(win)

    # Start with an empty string
    current_text = ""

    # Draw the circle
    circle = Circle(center, 40)
    circle.setOutline('green')
    circle.setFill("black")
    circle.setWidth(2)
    circle.draw(win)

    # Initial arrow (pointing right at 0 degrees on the circle)
    arrow = Line(center, Point(center.getX() + 38, center.getY()))  # Arrow points right
    arrow.setArrow('last')  # Arrow at the end
    arrow.setWidth(5)
    arrow.setFill("white")
    arrow.draw(win)

    t_change = Text(Point(150,819),"""Temperature
    change""")
    t_change.setFill("black")
    t_change.setSize(16)
    t_change.setTextColor("white")
    t_change.draw(win)

    t_display = Text(Point(340,815), "-0.0")
    t_display.setFill("black")
    t_display.setSize(16)
    t_display.setTextColor("white")
    t_display.draw(win)

    visible = False
    toggle_visibility(number_pad,visible)

    initialize()


def close_win():
    global win
    win.close()
    stop_event.set()


# Main function to run the graphics window and server
def run_gui_and_server():
    # Set up the graphics window
    setup_window()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # This ensures the server thread will exit when the program does
    server_thread.start()

    schedule.every(5).minutes.do(calc_angle)
    schedule.every().hour.at(":00").do(append_to_file)
    schedule.every().day.at("00:00").do(reset_daily_stats)
    schedule.every().day.at("00:00").do(yearly_task)

    # Main GUI loop
    while True:
        global input_box, close_box
        global setpoint_boxes
        global number_pad
        global textbox_label, current_text
        global visible

        schedule.run_pending()
        time.sleep(1)

        update_display()
        click_point = win.checkMouse()  # Wait for mouse click (blocking)

        keystop = win.checkKey()
        if keystop == "x":
            close_win()
            break
        # Ignore clicks on the input box

        if click_point is not None:
            clicked_value = click_on_button(click_point.getX(), click_point.getY(), number_pad)

            if clicked_value is not None:
                update_textbox(textbox_label, current_text, clicked_value)
                current_text = textbox_label.getText()

            if 800 < click_point.getX() < 860 and \
                    712 < click_point.getY() < 737:
                visible = not visible
                toggle_visibility(number_pad, visible)

            # click to close window
            input_x = 200
            input_y = 725
            if input_x - 75 < click_point.getX() < input_x + 75 and \
                            input_y - 12 < click_point.getY() < input_y + 12:
                 close_win()
                 break

                 # click to clear error box
            input_x = 1000
            input_y = 725
            if input_x - 50 < click_point.getX() < input_x + 50 and \
                        input_y - 12 < click_point.getY() < input_y + 12:
                no_good.setText("no error Now")

# click to change setpoint
        for i in range(6):
            input_x = 150 + i * 240
            input_y = 660
            if click_point is not None:
                if input_x - 50 < click_point.getX() < input_x + 50 and \
                        input_y - 12 < click_point.getY() < input_y + 12:
                    setpoint_boxes[i].setText(textbox_label.getText())
                    write_data(i)

# click to toggle heat on off
        for i in range(6):
            input_x = 165
            input_y = 50 + i * 75
            if click_point is not None:
                if input_x - 150 < click_point.getX() < input_x + 150 and \
                        input_y - 20 < click_point.getY() < input_y + 20:
                    toggle_onoff(i)




    server_thread.join()


if __name__ == "__main__":
    run_gui_and_server()
