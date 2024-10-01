# 'pip install PySide6' tarvitaan 
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu, QGraphicsTextItem
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QPixmap
from PySide6.QtCore import Qt, QTimer

# vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Vaikeustasojen nopeudet (ms)
DIFFICULTY_LEVELS = {
    "Helppo": 400,  # Hitaampi nopeus
    "Normaali": 250,  # Keskinopeus
    "Vaikea": 100  # Nopea
}

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        
        self.is_game_started = False  # Peli ei ole käynnissä aluksi
        self.is_game_over = False  # Pelin tila (päättynyt vai ei)
        self.score = 0  # Pistelaskuri
        self.difficulty_index = 0  # Vaikeustason indeksi (helppo, normaali, vaikea)
        self.difficulties = list(DIFFICULTY_LEVELS.keys())  # Vaikeustasojen nimet
        self.difficulties.append("Sulje peli")  # Lisätään "Sulje peli" vaihtoehto
        self.selected_difficulty = self.difficulties[self.difficulty_index]  # Oletustaso on "Helppo"
        self.return_to_menu = False  # Tila, joka kertoo palaako päävalikkoon pelin jälkeen
        self.start_menu()  # Näytetään aloitusvalikko

    def start_menu(self):
        self.is_game_started = False  # Nollataan pelin käynnistys
        self.return_to_menu = False  # Nollataan tila, jotta valikko toimii normaalisti
        self.scene().clear()

        # Ladataan ja asetetaan taustakuva
        background = QPixmap("matokuva.png")

        # Tarkistetaan, että kuva on ladattu oikein
        if background.isNull():
            print("Kuvaa ei löytynyt tai sitä ei voitu ladata.")
        else:
            # Skaalataan kuva sopimaan pelialueelle
            background = background.scaled(CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT, Qt.KeepAspectRatioByExpanding)
            self.scene().addPixmap(background)

        self.show_difficulty_options()

    def show_difficulty_options(self):
        # Näytetään valittava vaikeustaso ja sen ohje
        instruction_text = QGraphicsTextItem("Valitse vaikeustaso tai sulje peli: ")
        instruction_text.setFont(QFont("Arial", 16))
        instruction_text.setPos(50, 50)
        self.scene().addItem(instruction_text)

        # Näytetään vaikeustasot ja korostetaan valittua
        for i, difficulty in enumerate(self.difficulties):
            difficulty_text = QGraphicsTextItem(difficulty)
            difficulty_text.setFont(QFont("Arial", 14))
            # Korostetaan valittua vaihtoehtoa
            if i == self.difficulty_index:
                difficulty_text.setDefaultTextColor(Qt.red)  # Korostettu punainen väri
            else:
                difficulty_text.setDefaultTextColor(Qt.black)
            difficulty_text.setPos(50, 100 + i * 30)
            self.scene().addItem(difficulty_text)

        # Näytetään ohje valinnan vahvistamiseksi
        start_text = QGraphicsTextItem("Paina Enter vahvistaaksesi valinnan")
        start_text.setFont(QFont("Arial", 12))
        start_text.setPos(50, 200 + len(self.difficulties) * 30)
        self.scene().addItem(start_text)

    def keyPressEvent(self, event):
        key = event.key()

        # Jos peli ei ole alkanut ja pelaaja palaa päävalikkoon, käsitellään vaikeustason valintaa
        if not self.is_game_started and not self.return_to_menu:
            if key == Qt.Key_Up:
                self.difficulty_index = (self.difficulty_index - 1) % len(self.difficulties)
                self.selected_difficulty = self.difficulties[self.difficulty_index]
                self.show_difficulty_options()
            elif key == Qt.Key_Down:
                self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulties)
                self.selected_difficulty = self.difficulties[self.difficulty_index]
                self.show_difficulty_options()
            elif key == Qt.Key_Enter or key == Qt.Key_Return:  # Aloita peli tai sulje sovellus kun Enter painetaan
                if self.selected_difficulty == "Sulje peli":
                    QApplication.quit()  # Suljetaan sovellus
                else:
                    self.is_game_started = True
                    self.is_game_over = False  # Nollataan pelin tila
                    self.start_game()
            return

        # Jos peli on päättynyt, sallitaan paluu päävalikkoon Enterillä
        if self.is_game_over:
            if key == Qt.Key_Enter or key == Qt.Key_Return:
                self.is_game_over = False
                self.return_to_menu = True  # Asetetaan tila paluuseen päävalikkoon
                self.start_menu()
            return

        # Jos peli on käynnissä, ohjataan matoa
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
        if not self.is_game_started or self.is_game_over:
            return  # Ei päivitetä peliä ennen kuin peli on alkanut tai jos peli on ohi

        head_x, head_y = self.snake[0]

        # Päivitetään maton pään paikka suunnan perusteella
        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Tarkista, osuuko mato seinään tai itseensä
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):  # Jos pää osuu maton vartaloon
            self.game_over()  # Peli päättyy, jos mato osuu seinään tai itseensä
            return

        self.snake.insert(0, new_head)

        # Tarkista, osuuko mato palloon
        if new_head == self.food:
            self.generate_food()  # Luodaan uusi pallo
            self.score += 10  # Päivitä pistelaskuri
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

        # Näytetään pistemäärä
        self.scene().addText(f"Pisteet: {self.score}", QFont("Arial", 12))

    def generate_food(self):
        # Luodaan satunnainen paikka pallolle, varmistetaan ettei se ole maton päällä
        while True:
            food_x = random.randint(0, GRID_WIDTH - 1)
            food_y = random.randint(0, GRID_HEIGHT - 1)
            if (food_x, food_y) not in self.snake:
                self.food = (food_x, food_y)
                break

    def game_over(self):
        self.is_game_over = True  # Pelin tila on nyt "päättynyt"
        self.timer.stop()  # Pysäytetään pelin päivitys
        
        # Näytetään "Game Over" -teksti keskellä ruutua
        game_over_text = QGraphicsTextItem("GAME OVER")
        game_over_text.setFont(QFont("Arial", 24))
        text_width = game_over_text.boundingRect().width()
        text_height = game_over_text.boundingRect().height()
        
        # Sijoitetaan teksti keskelle ruutua
        game_over_text.setPos((CELL_SIZE * GRID_WIDTH - text_width) / 2, 
                              (CELL_SIZE * GRID_HEIGHT - text_height) / 2)
        self.scene().addItem(game_over_text)

        # Näytetään ohjeteksti uuden pelin aloittamiseksi
        restart_text = QGraphicsTextItem("Paina Enter palataksesi päävalikkoon")
        restart_text.setFont(QFont("Arial", 16))
        restart_text_width = restart_text.boundingRect().width()
        restart_text.setPos((CELL_SIZE * GRID_WIDTH - restart_text_width) / 2, 
                            (CELL_SIZE * GRID_HEIGHT - text_height) / 2 + 40)
        self.scene().addItem(restart_text)

    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.generate_food()  # Luodaan ensimmäinen pallo
        self.score = 0  # Nollataan pistemäärä
        
        # Asetetaan nopeus valitun vaikeustason mukaan
        selected_speed = DIFFICULTY_LEVELS[self.selected_difficulty]
        self.timer.start(selected_speed)

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
