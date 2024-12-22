from graphics import *

# Create a global variable to hold the graphics window and text fields
win = None
data_boxes = []
highlighted_box = None
input_box = None
setpoint_boxes = []

# Function to create the graphics window and text boxes
def setup_window():
    global win, text_boxes, highlighted_box, input_box, setpoint_boxes

    win = GraphWin("Home Temperature", 1000, 500)  # Create the window
    win.setBackground("cyan")

    # Create an input box for user input
    input_box = Entry(Point(400, 450), 20)  # Create an entry box
    input_box.setSize(12)
    input_box.draw(win)

    # Create text boxes
    for i in range(5):
        message_box = Text(Point(150 + i * 150, 100), "")  # Place them horizontally
        message_box.setSize(12)
        message_box.setTextColor("blue")
        message_box.draw(win)
        data_boxes.append(message_box)



    for i in range(6):
        message_box = Text(Point(150 + i * 150, 150), "setpoint")  # Place them horizontally
        message_box.setSize(12)
        message_box.setTextColor("blue")
        message_box.draw(win)
        setpoint_boxes.append(message_box)

    message_box = Text(Point(200, 300), "")  # Place them horizontally
    message_box.setSize(12)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)

    message_box = Text(Point(500, 300), "Clear")  # Place them horizontally
    message_box.setSize(12)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)

    message_box = Text(Point(700, 300), "Clear all")  # Place them horizontally
    message_box.setSize(12)
    message_box.setTextColor("orange")
    message_box.draw(win)
    setpoint_boxes.append(message_box)

    # Add highlight functionality
    for box in data_boxes:
        box.setText("Click to highlight")  # Placeholder text for other boxes

    setpoint_boxes[6].setText("CLOSE NOW")

# Function to highlight the clicked box
def highlight_box(point):
    global highlighted_box

    for box in setpoint_boxes:
        # Get the bounding box for each text box
        if box.getAnchor().getX() - 50 < point.getX() < box.getAnchor().getX() + 50 and \
           box.getAnchor().getY() - 10 < point.getY() < box.getAnchor().getY() + 10:
            if highlighted_box:  # Remove highlight from previously highlighted box
                highlighted_box.setTextColor("blue")
            box.setTextColor("red")  # Highlight the selected box
            highlighted_box = box
            break

def closeWin():
    global win
    win.close()


# Main loop
def main():
    setup_window()

    while True:
        click_point = win.getMouse()  # Wait for mouse click (blocking)

        # Ignore clicks on the input box
        if input_box.getAnchor().getX() - 100 < click_point.getX() < input_box.getAnchor().getX() + 100 and \
           input_box.getAnchor().getY() - 10 < click_point.getY() < input_box.getAnchor().getY() + 10:
            continue


        # Check if setpoint_boxes[6] (the "CLOSE NOW" box) is clicked
        close_box = setpoint_boxes[6]
        if close_box.getAnchor().getX() - 50 < click_point.getX() < close_box.getAnchor().getX() + 50 and \
           close_box.getAnchor().getY() - 10 < click_point.getY() < close_box.getAnchor().getY() + 10:
            closeWin()  # Close the window if the "CLOSE NOW" box is clicked
            break  # Break the loop to ensure the program terminates
# Run the program
if __name__ == "__main__":
    main()