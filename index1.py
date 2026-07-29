import tkinter as tk
from tkinter import messagebox, font
import random
import sys

# Optional sound on Windows (uncomment if needed)
# import winsound

class DigitalNumberGuessingGame:
    """
    A modern digital-style number guessing game using Tkinter.
    The player guesses a number between 1 and 100, and the game gives
    hints (Too High / Too Low) until the correct number is found.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Number Guessing Game")
        self.root.geometry("600x700")  # Fixed window size
        self.root.resizable(False, False)
        self.root.configure(bg="black")

        # Center the window on screen
        self.center_window()

        # Game state variables
        self.target_number = None
        self.attempts = 0
        self.best_score = float('inf')  # Initialize as infinity
        self.game_active = False
        self.guess_history = []  # List of (guess, feedback) tuples

        # Setup the main container and initialize the welcome screen
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_welcome_screen()

    def center_window(self):
        """Center the window on the user's screen."""
        self.root.update_idletasks()
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_welcome_screen(self):
        """Display the welcome screen with a start button."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Welcome title - digital style
        digital_font = font.Font(family="Courier New", size=30, weight="bold")
        title = tk.Label(
            self.main_frame,
            text="DIGITAL NUMBER\nGUESSING GAME",
            font=digital_font,
            fg="lime green",
            bg="black",
            justify=tk.CENTER
        )
        title.pack(pady=100)

        # Start button
        start_btn = tk.Button(
            self.main_frame,
            text="START GAME",
            font=("Helvetica", 16, "bold"),
            bg="lime green",
            fg="black",
            activebackground="dark green",
            activeforeground="white",
            padx=20,
            pady=10,
            command=self.start_game
        )
        start_btn.pack(pady=50)

        # Footer
        footer = tk.Label(
            self.main_frame,
            text="Guess the number between 1 and 100",
            font=("Helvetica", 12),
            fg="gray",
            bg="black"
        )
        footer.pack(side=tk.BOTTOM, pady=20)

    def start_game(self):
        """Initialize a new game and switch to the game screen."""
        # Generate a random target number between 1 and 100
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.game_active = True
        self.guess_history.clear()

        # Build the game interface
        self.build_game_interface()

    def build_game_interface(self):
        """Create all widgets for the game screen."""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Configure grid layout for main frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # ---- Title ----
        digital_font = font.Font(family="Courier New", size=24, weight="bold")
        title_lbl = tk.Label(
            self.main_frame,
            text="DIGITAL NUMBER GUESSING",
            font=digital_font,
            fg="lime green",
            bg="black"
        )
        title_lbl.grid(row=0, column=0, pady=10, sticky="n")

        # ---- Digital Display Area (status, attempts, best) ----
        display_frame = tk.Frame(self.main_frame, bg="black", relief=tk.RAISED, bd=2)
        display_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_rowconfigure(2, weight=1)

        # Large status message (e.g., "Too High", "Too Low", "Correct!")
        self.status_lbl = tk.Label(
            display_frame,
            text="Enter your guess",
            font=("Courier New", 20, "bold"),
            fg="lime green",
            bg="black",
            anchor="center"
        )
        self.status_lbl.grid(row=0, column=0, pady=5, sticky="nsew")

        # Attempts and Best Score
        info_font = font.Font(family="Courier New", size=14, weight="bold")
        self.attempts_lbl = tk.Label(
            display_frame,
            text="Attempts: 0",
            font=info_font,
            fg="lime green",
            bg="black",
            anchor="center"
        )
        self.attempts_lbl.grid(row=1, column=0, pady=5, sticky="nsew")

        self.best_lbl = tk.Label(
            display_frame,
            text="Best: --",
            font=info_font,
            fg="lime green",
            bg="black",
            anchor="center"
        )
        self.best_lbl.grid(row=2, column=0, pady=5, sticky="nsew")

        # ---- History / Guesses Display ----
        history_frame = tk.Frame(self.main_frame, bg="black")
        history_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(0, weight=1)

        # Use a Text widget to show guess history (like a log)
        self.history_text = tk.Text(
            history_frame,
            height=8,
            font=("Courier New", 12),
            fg="lime green",
            bg="black",
            relief=tk.SUNKEN,
            bd=2,
            state=tk.DISABLED
        )
        self.history_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for history
        scrollbar = tk.Scrollbar(history_frame, command=self.history_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_text.config(yscrollcommand=scrollbar.set)

        # ---- Input Area ----
        input_frame = tk.Frame(self.main_frame, bg="black")
        input_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        # Entry for guess
        self.guess_entry = tk.Entry(
            input_frame,
            font=("Courier New", 16),
            bg="black",
            fg="lime green",
            insertbackground="lime green",
            justify="center",
            relief=tk.SUNKEN,
            bd=2
        )
        self.guess_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # Guess button
        guess_btn = tk.Button(
            input_frame,
            text="GUESS",
            font=("Helvetica", 14, "bold"),
            bg="lime green",
            fg="black",
            activebackground="dark green",
            activeforeground="white",
            command=self.make_guess
        )
        guess_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # ---- Error Message Label ----
        self.error_lbl = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 12),
            fg="red",
            bg="black"
        )
        self.error_lbl.grid(row=4, column=0, pady=(0, 10))

        # ---- Control Buttons (New Game & Exit) ----
        control_frame = tk.Frame(self.main_frame, bg="black")
        control_frame.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        new_game_btn = tk.Button(
            control_frame,
            text="NEW GAME",
            font=("Helvetica", 14, "bold"),
            bg="lime green",
            fg="black",
            activebackground="dark green",
            activeforeground="white",
            command=self.reset_game
        )
        new_game_btn.grid(row=0, column=0, padx=5, sticky="ew")

        exit_btn = tk.Button(
            control_frame,
            text="EXIT",
            font=("Helvetica", 14, "bold"),
            bg="red",
            fg="white",
            activebackground="dark red",
            activeforeground="white",
            command=self.exit_game
        )
        exit_btn.grid(row=0, column=1, padx=5, sticky="ew")

        # Bind Enter key to guess
        self.guess_entry.bind('<Return>', lambda event: self.make_guess())

        # Focus on entry
        self.guess_entry.focus_set()

        # Update the display with initial info
        self.update_display()

    def update_display(self):
        """Refresh the status, attempts, best score, and history labels."""
        # Update attempts and best
        self.attempts_lbl.config(text=f"Attempts: {self.attempts}")
        if self.best_score == float('inf'):
            self.best_lbl.config(text="Best: --")
        else:
            self.best_lbl.config(text=f"Best: {self.best_score}")

        # Update history text widget
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        if self.guess_history:
            for guess, feedback in self.guess_history:
                self.history_text.insert(tk.END, f"{guess} → {feedback}\n")
        else:
            self.history_text.insert(tk.END, "Your guesses will appear here.\n")
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)  # Auto-scroll to bottom

    def make_guess(self):
        """Handle the player's guess input."""
        if not self.game_active:
            messagebox.showinfo("Game Over", "Please start a new game.")
            return

        # Get input and validate
        guess_str = self.guess_entry.get().strip()
        self.guess_entry.delete(0, tk.END)  # Clear entry

        if not guess_str:
            self.error_lbl.config(text="Please enter a number.")
            return

        try:
            guess = int(guess_str)
        except ValueError:
            self.error_lbl.config(text="Invalid input. Please enter an integer.")
            return

        if guess < 1 or guess > 100:
            self.error_lbl.config(text="Number must be between 1 and 100.")
            return

        # Clear error message
        self.error_lbl.config(text="")

        # Increment attempts
        self.attempts += 1

        # Check the guess
        if guess == self.target_number:
            feedback = "Correct!"
            self.status_lbl.config(text="🎉 CORRECT! 🎉")
            self.game_active = False
            # Update best score
            if self.attempts < self.best_score:
                self.best_score = self.attempts
            # Add to history
            self.guess_history.append((guess, feedback))
            self.update_display()
            # Show congratulation popup
            self.show_congratulations()
            # Optionally play a sound (Windows)
            # winsound.Beep(1000, 500)  # Uncomment if winsound available
            return
        elif guess > self.target_number:
            feedback = "Too High"
            self.status_lbl.config(text="⬆ TOO HIGH ⬆")
        else:  # guess < target_number
            feedback = "Too Low"
            self.status_lbl.config(text="⬇ TOO LOW ⬇")

        # Add to history and update display
        self.guess_history.append((guess, feedback))
        self.update_display()

        # Optional sound for each guess
        # winsound.Beep(500, 100)

    def show_congratulations(self):
        """Show a popup congratulating the player."""
        messagebox.showinfo(
            "Congratulations!",
            f"You guessed the number {self.target_number} in {self.attempts} attempts!\n"
            f"Best score: {self.best_score}"
        )

    def reset_game(self):
        """Reset the game with a new target number, keeping best score."""
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.game_active = True
        self.guess_history.clear()
        self.status_lbl.config(text="New game started!")
        self.error_lbl.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.update_display()
        self.guess_entry.focus_set()

    def exit_game(self):
        """Close the application."""
        self.root.destroy()
        sys.exit()


# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    game = DigitalNumberGuessingGame(root)
    root.mainloop()