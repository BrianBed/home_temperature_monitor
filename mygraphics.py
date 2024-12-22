from graphics import *
def main():

    win2 = GraphWin("screen", 500,500)
    win2.setCoords(1200, 1100, 1200, 100)
    win2.setBackground("white")



    win = GraphWin("My Window", 1000,1000)
    #win.setCoords()
    win.setBackground(color_rgb(25,156,38))
    pt = Point(250,250)
    cir = Circle(pt,100)
    cir.setFill(color_rgb(100,159,200))
    cir.draw(win)

    pt = Point(500,500)
    cir = Circle(pt,150)
    cir.setFill(color_rgb(100,40,200))
    cir.draw(win)

    rec = Rectangle(Point(50,900), Point(800,800))
    rec.setFill(color_rgb(20, 20 ,200))
    rec.draw(win)


    win.getMouse()



    message1 = Text(Point(350, 850), "Hello!  this is my text test")
    message1.setTextColor("pink")
    message1.draw(win)

    win.getMouse()
    win.close()

main()