# Hangman Game in Java

A simple console-based Hangman game implemented in Java. The player attempts to guess a randomly selected animal name, one letter at a time, before the hangman is fully drawn.

---

## 🧩 Features

- Randomly selects a word from a predefined list of animal names.
- ASCII gallows visuals update with each wrong guess.
- Validates user input (ensures only single letters are allowed).
- Tracks both correct and incorrect guesses.
- Ends game when player either guesses the word or reaches 6 incorrect guesses.

---

## 🎮 How to Play

1. Run the program.
2. You'll see a blank word represented by underscores (`_`), and a hangman gallows.
3. Type in a letter to guess.
4. If the letter is in the word, it will be revealed in its correct position(s).
5. If not, the hangman drawing progresses.
6. You lose after 6 incorrect guesses or win by completing the word.

---

## 🛠️ Requirements

- Java Development Kit (JDK) 8 or later

---

## 🚀 How to Run

1. Compile the Java program:

   ```bash
   javac Hangman.java
