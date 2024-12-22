from graphics import *
def main():

    win = GraphWin("My Window", 1000,1000)
    win.setBackground(color_rgb(25,156,38))

    text_boxes = []


    rec = Rectangle(Point(450,450), Point(550,500))
    rec.setFill(color_rgb(20, 20 ,200))
    rec.draw(win)


    setpoint_box = Text(Point(200, 900), "Setpoint")
    setpoint_box.setSize(12)
    setpoint_box.setTextColor("blue")
    setpoint_box.draw(win)
    text_boxes.append(setpoint_box)

    setpoint_box = Text(Point(400, 900), "Setpoint")
    setpoint_box.setSize(12)
    setpoint_box.setTextColor("blue")
    setpoint_box.draw(win)
    text_boxes.append(setpoint_box)

    setpoint_box = Text(Point(600, 900), "Setpoint")
    setpoint_box.setSize(12)
    setpoint_box.setTextColor("blue")
    setpoint_box.draw(win)
    text_boxes.append(setpoint_box)

    message1 = Text(Point(500, 475), "close")
    message1.setTextColor("pink")
    message1.draw(win)

    input_box = Entry(Point(500, 700), 10)  # Input box for the user
    input_box.draw(win)

    message = Text(Point(350, 850), "Hello!  this is my text test")
    message.setTextColor("pink")
    message.draw(win)

    def find_clicked_textbox(point):
        for textbox in text_boxes:
            if textbox.getAnchor().getX() - 50 <= point.getX() <= textbox.getAnchor().getX() + 50 and \
                    textbox.getAnchor().getY() - 10 <= point.getY() <= textbox.getAnchor().getY() + 10:
                return textbox
        return None

    def transfer_to_box():
        while True:
            click = detect_click()

            # Check if a rectangle or text box was clicked
            rect = find_clicked_rectangle(click)
            textbox = find_clicked_textbox(click)

            if rect:
                highlight_rectangle(rect)  # Highlight the rectangle

            if textbox:
                highlight_textbox(textbox)  # Highlight the text box
                user_input = input_box.getText()  # Get the input from the input box
                textbox.setText(user_input)

    win.getMouse()
    win.close()

main()