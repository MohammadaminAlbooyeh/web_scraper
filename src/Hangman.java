import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Hangman {

    // List of words to pick randomly
    public static String[] words = {
        "ant", "baboon", "badger", "bat", "bear", "beaver",
        "camel", "cat", "clam", "cobra", "cougar", "coyote",
        "crow", "deer", "dog", "donkey", "duck", "eagle",
        "ferret", "fox", "frog", "goat", "goose", "hawk",
        "lion", "lizard", "llama", "mole", "monkey", "moose",
        "mouse", "mule", "newt", "otter", "owl", "panda",
        "parrot", "pigeon", "python", "rabbit", "ram", "rat",
        "raven", "rhino", "salmon", "seal", "shark", "sheep",
        "skunk", "sloth", "snake", "spider", "stork", "swan",
        "tiger", "toad", "trout", "turkey", "turtle", "weasel",
        "whale", "wolf", "wombat", "zebra"
    };

    // Gallows array showing hangman stages based on wrong guesses
    public static String[] gallows = {
        "+---+\n" +
        "|   |\n" +
        "    |\n" +
        "    |\n" +   // 0 misses
        "    |\n" +
        "    |\n" +
        "=========\n",

        "+---+\n" +
        "|   |\n" +
        "O   |\n" +   // 1 miss
        "    |\n" +
        "    |\n" +
        "    |\n" +
        "=========\n",

        "+---+\n" +
        "|   |\n" +
        "O   |\n" +    // 2 misses
        "|   |\n" +
        "    |\n" +
        "    |\n" +
        "=========\n",

        " +---+\n" +
        " |   |\n" +
        " O   |\n" +   // 3 misses
        "/|   |\n" +
        "     |\n" +
        "     |\n" +
        " =========\n",

        " +---+\n" +
        " |   |\n" +
        " O   |\n" +   // 4 misses
        "/|\\  |\n"+
        "     |\n" +
        "     |\n" +
        " =========\n",

        " +---+\n" +
        " |   |\n" +
        " O   |\n" +   // 5 misses
        "/|\\  |\n" +
        "/    |\n" +
        "     |\n" +
        " =========\n",

        " +---+\n" +
        " |   |\n" +
        " O   |\n" +   // 6 misses - lost
        "/|\\  |\n" +
        "/ \\  |\n" +
        "     |\n" +
        " =========\n"
    };

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // Pick a random word
        String word = words[random.nextInt(words.length)];

        // Create placeholders filled with '_'
        char[] placeholders = new char[word.length()];
        for(int i = 0; i < placeholders.length; i++) {
            placeholders[i] = '_';
        }

        // List to store wrong guesses
        ArrayList<Character> missedGuesses = new ArrayList<>();

        int missedCount = 0;  // Count of wrong guesses

        // Game loop until win or lose
        while(true) {
            // Print current gallows stage
            System.out.println(gallows[missedCount]);

            // Print current word status with placeholders
            printPlaceholders(placeholders);

            // Print missed guesses
            printMissedGuesses(missedGuesses);

            // Get user guess
            System.out.print("Enter your guess: ");
            String guessInput = scanner.nextLine().toLowerCase();

            // Validate input: must be one letter
            if (guessInput.length() != 1 || !Character.isLetter(guessInput.charAt(0))) {
                System.out.println("Please enter a single letter.\n");
                continue;
            }
            char guess = guessInput.charAt(0);

            // Check if already guessed
            if (missedGuesses.contains(guess) || contains(placeholders, guess)) {
                System.out.println("You already guessed that letter. Try again.\n");
                continue;
            }

            // Check if guess is correct
            if (checkGuess(word, guess)) {
                // Update placeholders with correct guess
                updatePlaceholders(word, placeholders, guess);

                // Check if player won
                if (isWordGuessed(placeholders)) {
                    System.out.println("\n" + word);
                    System.out.println("Congratulations! You won.");
                    break;
                }
            } else {
                // Add to missed guesses and increment count
                missedGuesses.add(guess);
                missedCount++;

                // If 6 misses, player loses
                if (missedCount == 6) {
                    System.out.println(gallows[missedCount]);
                    System.out.println("You lost! The correct word was: " + word);
                    break;
                }
            }

            System.out.println();  // blank line for spacing
        }

        scanner.close();
    }

    // Print the current placeholders for the word
    public static void printPlaceholders(char[] placeholders) {
        for(char c : placeholders) {
            System.out.print(c + " ");
        }
        System.out.println("\n");
    }

    // Print the missed guesses
    public static void printMissedGuesses(ArrayList<Character> missedGuesses) {
        System.out.print("Missed guesses: ");
        for(char c : missedGuesses) {
            System.out.print(c + " ");
        }
        System.out.println("\n");
    }

    // Check if guess is in the word
    public static boolean checkGuess(String word, char guess) {
        return word.indexOf(guess) >= 0;
    }

    // Update placeholders with the correct guessed letter
    public static void updatePlaceholders(String word, char[] placeholders, char guess) {
        for(int i = 0; i < word.length(); i++) {
            if(word.charAt(i) == guess) {
                placeholders[i] = guess;
            }
        }
    }

    // Check if all letters are guessed (no more '_')
    public static boolean isWordGuessed(char[] placeholders) {
        for(char c : placeholders) {
            if(c == '_') {
                return false;
            }
        }
        return true;
    }

    // Check if char is already in placeholders array
    public static boolean contains(char[] array, char c) {
        for(char ch : array) {
            if(ch == c) return true;
        }
        return false;
    }
}


