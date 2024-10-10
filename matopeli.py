import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15
INITIAL_SPEED = 300  # Alkuperäinen nopeus (ms)
SPEED_INCREMENT = 10  # Nopeus kasvaa, kun käärme kasvaa
MIN_SPEED = 50

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT + 50)  # Lisätilaa pisteille

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        self.game_started = False
        self.init_screen()

    def keyPressEvent(self, event):
        key = event.key()

        # starting game by button
        if not self.game_started:
            if key == event.key():
                self.game_started = True
                self.scene().clear()
                self.start_game()

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
        if new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.timer.stop()
            return 

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1  
            self.spawn_food() 
            self.increase_speed() 
        else:
            self.snake.pop()  

        self.print_game()

    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    def spawn_food(self):
       
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:  
                self.food = (x, y)
                break
        
    def increase_speed(self):
        self.speed = max(self.speed - SPEED_INCREMENT, MIN_SPEED)
        self.timer.start(self.speed)

    def print_game(self):
        self.scene().clear()

        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.black))

        food_x, food_y = self.food
        self.scene().addEllipse(food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.red), QBrush(Qt.red))

        self.print_score()

    def print_score(self):
 
        score_text = f"Score: {self.score}"
        self.scene().addText(score_text, QFont("Arial", 16)).setPos(10, CELL_SIZE * GRID_HEIGHT + 10)

    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.score = 0 
        self.speed = INITIAL_SPEED
        self.spawn_food()  
        self.timer.start(self.speed)  

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
