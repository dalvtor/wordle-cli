import curses
import random

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
import data


class Wordle:

    def __init__(self, screen):
        self.screen = screen
        self.keyboard = [
            ["Q", " ", "W", " ", "E", " ", "R", " ", "T", " ", "Y", " ", "U", " ", "I", " ", "O", " ", "P"],
            [" ", "A", " ", "S", " ", "D", " ", "F", " ", "G", " ", "H", " ", "J", " ", "K", " ", "L"],
            [" ", " ", "Z", " ", "X", " ", "C", " ", "V", " ", "B", " ", "N", " ", "M"],
        ]
        self.valid_chars = {}
        self.main()

    def draw_keyboard(self):
        """
        Draws the keyboard at the bottom so the user knows which characters have been used
        """
        n_row = 10
        n_col = 0
        for row in self.keyboard:
            for ch in row:
                try:
                    self.screen.addstr(n_row, curses.COLS // 2 + n_col - len(row) // 2, ch, self.valid_chars[ch])
                except KeyError:
                    self.screen.addstr(n_row, curses.COLS // 2 + n_col - len(row) // 2, ch)
                n_col += 1
                self.screen.refresh()
            n_row += 1
            n_col = 0

    def delete_last_char(self, pos, guess):
        """
        Moves the cursor one position back and clears the rest of the line
        """
        self.screen.move(pos, curses.COLS // 2 + len(guess) - 2)
        self.screen.clrtoeol()

    def main(self):
        """
        Main game loop
        """
        words = pkg_resources.read_text(data, "words.txt").split("\n")
        word = random.choice(words).upper()
        curses.start_color()
        curses.use_default_colors()
        title = 'WORDLE IN A TERMINAL'
        num_guesses = 0

        self.screen.addstr(0, curses.COLS // 2 - (len(title) + 1) // 2, title)
        self.draw_keyboard()

        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, 245, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)

        while num_guesses < 6:
            guess = ""

            while True:
                k = self.screen.getch(num_guesses + 2, curses.COLS // 2 + len(guess) - 2)
                if k == 127:  # backspace
                    guess = guess[:-1]
                    self.delete_last_char(num_guesses + 2, guess)
                elif chr(k) == "\n" and len(guess) == 5:  # 5 characters already in and RETURN pressed
                    if guess.lower() in words:
                        self.screen.clrtoeol()
                        break
                elif len(guess) == 5:  # 5 characters already in, delete other characters
                    self.delete_last_char(num_guesses + 2, guess)
                elif chr(k).isalpha() and chr(k).isascii() and len(guess) < 5:  # Valid input
                    guess += chr(k)
                elif not chr(k).isalpha():  # Weird symbol, remove it
                    self.delete_last_char(num_guesses + 2, guess)

            # Draw guess
            for i, letter in enumerate(guess):
                char = letter.upper()
                if char in word and word[i] == char:
                    color = curses.color_pair(1)
                    self.valid_chars[char] = color
                elif char in word:
                    color = curses.color_pair(2)
                    if char not in self.valid_chars or \
                            char in self.valid_chars and self.valid_chars[char] != curses.color_pair(1):
                        self.valid_chars[char] = color
                else:
                    color = curses.color_pair(3)
                    self.valid_chars[char] = color
                self.screen.addstr(num_guesses + 2, curses.COLS // 2 + i - 2, char, color)
            num_guesses += 1

            # Redraw keyboard
            self.draw_keyboard()

            # Check win condition
            if guess.upper() == word.upper():
                text = "You won"
                self.screen.addstr(9, curses.COLS // 2 - (len(text)) // 2, text, curses.color_pair(1))
                self.screen.refresh()
                exit(0)

        # Game lost
        text = f"You lost, the word was {word}"
        self.screen.addstr(9, curses.COLS // 2 - (len(text)) // 2, text, curses.color_pair(4))
        self.screen.clrtobot()
        self.screen.refresh()


def main():
    screen = curses.initscr()
    try:
        Wordle(screen)
    except KeyboardInterrupt:
        exit()
    except curses.error:
        text = "An error occurred while launching the game, the terminal might not be tall enough"
        screen.addstr(0, curses.COLS // 2 - (len(text)) // 2, text)
        screen.refresh()


if __name__ == '__main__':
    main()
