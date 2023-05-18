import random


class Ship:
    def __init__(self, positions):
        self.positions = positions
        self.hits = [False] * len(positions)

    def is_sunk(self):
        return all(self.hits)


class Board:
    def __init__(self):
        self.grid_size = 6
        self.ships = []
        self.board = [['О'] * self.grid_size for _ in range(self.grid_size)]

    def place_ship(self, ship):
        for x, y in ship.positions:
            self.board[y][x] = '■'
        self.ships.append(ship)

    def display(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6|")
        for i in range(self.grid_size):
            row = ' | '.join(self.board[i])
            print(f"{i + 1} | {row} |")

    def check_shot(self, x, y):
        if self.board[y][x] == 'X' or self.board[y][x] == 'T':
            raise Exception("Вы уже стреляли в эту клетку!")
        for ship in self.ships:
            for i, (ship_x, ship_y) in enumerate(ship.positions):
                if ship_x == x and ship_y == y:
                    ship.hits[i] = True
                    self.board[y][x] = 'X'
                    return True
        self.board[y][x] = 'T'
        return False

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)


def generate_ships():
    ships = []
    positions = []

    while len(ships) < 1:
        positions.clear()
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        for ship in ships:
            if any(abs(x - pos[0]) <= 1 and abs(y - pos[1]) <= 1 for pos in ship.positions):
                break
        else:
            positions.append((x, y))
            if random.random() < 0.5:
                if x + 2 < 6:
                    positions.append((x + 1, y))
                    positions.append((x + 2, y))
                else:
                    positions.append((x - 1, y))
                    positions.append((x - 2, y))
            else:
                if y + 2 < 6:
                    positions.append((x, y + 1))
                    positions.append((x, y + 2))
                else:
                    positions.append((x, y - 1))
                    positions.append((x, y - 2))
            ships.append(Ship(positions))

    while len(ships) < 3:
        positions.clear()
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        for ship in ships:
            if any(abs(x - pos[0]) <= 1 and abs(y - pos[1]) <= 1 for pos in ship.positions):
                break
        else:
            positions.append((x, y))
            if random.random() < 0.5:
                if x + 1 < 6:
                    positions.append((x + 1, y))
                else:
                    positions.append((x - 1, y))
            else:
                if y + 1 < 6:
                    positions.append()
def main():
    player_board = Board()
    computer_board = Board()
    computer_ships = generate_ships()

    for ship in computer_ships:
        computer_board.place_ship(ship)

    while True:
        print("Ваша доска:")
        player_board.display()
        print("\nДоска компьютера:")
        computer_board.display()

        try:
            x = int(input("\nВведите номер столбца (1-6): "))
            y = int(input("Введите номер строки (1-6): "))
        except ValueError:
            print("Некорректный ввод. Введите числа от 1 до 6.")
            continue

        if x < 1 or x > 6 or y < 1 or y > 6:
            print("Некорректные координаты. Введите числа от 1 до 6.")
            continue

        x -= 1
        y -= 1

        try:
            if player_board.check_shot(x, y):
                print("Попадание!")
                if player_board.all_ships_sunk():
                    print("Вы победили!")
                    break
            else:
                print("Промах.")
        except Exception as e:
            print(str(e))
            continue

        while True:
            computer_x = random.randint(0, 5)
            computer_y = random.randint(0, 5)
            try:
                if computer_board.check_shot(computer_x, computer_y):
                    print(f"Компьютер попал в клетку {computer_x + 1}, {computer_y + 1}!")
                    if computer_board.all_ships_sunk():
                        print("Компьютер победил!")
                        break
                else:
                    print(f"Компьютер промахнулся по клетке {computer_x + 1}, {computer_y + 1}.")
                break
            except Exception:
                continue

    print("Игра завершена.")

if __name__ == "__main__":
    main()