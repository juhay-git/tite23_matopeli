# 'pip install PySide6' tarvitaan 
import sys, time
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor
from PySide6.QtCore import Qt, QTimer

# vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)        
        self.start_game()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # päivitetään suunta vain jos se ei ole vastakkainen valitulle suunnalle
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # board limits
        """*if new_head in self.snake or not (0 <= new_head < GRID_WIDTH) or not (0 <= new_head < GRID_HEIGHT):
            self.timer.stop()
            return
        """
        self.snake.insert(0, new_head)
        
        self.snake.pop()
        ## self.score += 1 ## pisteen lisäys kun syödään -JH
        self.print_game()
        if(self.food in self.snake):
            self.score = self.score + 1
            self.food = self.spawn_food()

    def rainbow(self): ## lisätty RGB
        r = random.randrange(0, 255+1)
        g = random.randrange(0, 255+1)
        b = random.randrange(0, 255+1)
        
        self.pen.setColor(QColor(r, g, b, 255))
        self.brush.setColor(QColor(r, g, b, 255))
        

    def print_game(self):
        self.scene().clear()
        

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, self.pen, self.brush)

        self.scene().addText(f"Points: {self.score}", QFont("Arial", 10)) ## pistelaskun piirto -JH
        self.rainbow()

        #print food
        fx,fy = self.food
        self.scene().addRect(fx * CELL_SIZE,fy * CELL_SIZE, CELL_SIZE, CELL_SIZE,QPen(Qt.black),QBrush(Qt.red))
        
    def start_game(self):
        self.score = 0 ## pistelaskun muuttuja -JH
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.timer.start(300)       
        self.pen = QPen(Qt.green) ##rgb -JH
        self.brush = QBrush(Qt.red) ##rgb -JH
        self.food = self.spawn_food() 

    def spawn_food(self):
        while True:
            x=random.randint(0,GRID_WIDTH -1)
            y=random.randint(0, GRID_HEIGHT-1)
            if(x, y) not in self.snake:
                return x, y

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
