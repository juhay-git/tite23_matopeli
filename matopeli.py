# 'pip install PySide6' tarvitaan 
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
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
        
        self.is_game_started = False  # Peli ei ole käynnissä aluksi
        self.start_menu()  # Näytetään aloitusvalikko

    def start_menu(self):
        self.scene().clear()
        self.scene().addText("Aloita peli painamalla Enter", QFont("Arial", 16))

    def keyPressEvent(self, event):
        key = event.key()
        if not self.is_game_started:
            if key == Qt.Key_Enter or key == Qt.Key_Return:  # Aloita peli kun Enter painetaan
                self.is_game_started = True
                self.start_game()
        else:
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
        if not self.is_game_started:
            return  # Ei päivitetä peliä ennen kuin peli on alkanut

        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        self.snake.insert(0, new_head)

        # Tarkista, osuuko mato palloon
        if new_head == self.food:
            self.generate_food()  # Luodaan uusi pallo
        else:
            self.snake.pop()  # Jos mato ei syönyt palloa, poistetaan hännästä pala

        self.print_game()

    def print_game(self):
        self.scene().clear()

        # Piirretään mato
        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.black))
        
        # Piirretään pallo
        fx, fy = self.food
        self.scene().addEllipse(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.red), QBrush(Qt.red))

    def generate_food(self):
        # Luodaan satunnainen paikka pallolle, varmistetaan ettei se ole maton päällä
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1)
            food_y = random.randint(0, GRID_HEIGHT - 1)
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.generate_food()  # Luodaan ensimmäinen pallo
        self.timer.start(300)

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
