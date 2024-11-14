#!/usr/bin/env python3
import requests
import html
import random

# Dictionary of categories
categories = {
    9: "General Knowledge", 10: "Entertainment - Books", 11: "Entertainment - Film",
    12: "Entertainment - Music", 13: "Entertainment - Musicals & Theater", 
    14: "Entertainment - Television", 15: "Entertainment - Video Games",
    16: "Entertainment - Board Games", 17: "Science - Nature", 
    18: "Science - Computers", 19: "Science - Mathematics", 20: "Mythology",
    21: "Sports", 22: "Geography", 23: "History", 24: "Politics",
    25: "Art", 26: "Celebrities", 27: "Animals", 28: "Vehicles", 
    29: "Entertainment - Comics", 30: "Science - Gadgets", 
    31: "Entertainment - Japanese Anime & Manga", 
    32: "Entertainment - Cartoon Animations"
}

# Build the URL based on user choices
def build_url():
    num_questions = input("Enter the number of questions (e.g., 3): ")
    print("\nCategories:")
    for key, value in categories.items():
        print(f"{key}: {value}")
    category = input("\nChoose a category number from the list above: ")
    difficulty = input("Choose a difficulty level (easy, medium, hard): ").lower()
    q_type = input("Choose question type (multiple, boolean): ").lower()

    url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&difficulty={difficulty}&type={q_type}"
    return url

# Fetch trivia data
def fetch_trivia(url):
    data = requests.get(url).json()
    return data

# Display and process trivia questions
def process_questions(data):
    score = 0
    questions = data.get("results", [])
    for i, question_data in enumerate(questions, start=1):
        question = html.unescape(question_data["question"])
        correct_answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]
        
        # Prepare the answers list
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)  # Randomize answer order

        print(f"\nQuestion {i}: {question}")
        for idx, answer in enumerate(all_answers, start=1):
            print(f"{idx}. {answer}")

        # Get user answer and check if it's correct
        try:
            user_answer = int(input("Your answer (enter the number): "))
            if all_answers[user_answer - 1] == correct_answer:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer was: {correct_answer}")
        except (ValueError, IndexError):
            print(f"Invalid input. The correct answer was: {correct_answer}")

    print(f"\nYou scored {score} out of {len(questions)}.")

# Main function
def main():
    url = build_url()
    data = fetch_trivia(url)
    if data["response_code"] == 0:  # Check if trivia questions were retrieved successfully
        process_questions(data)
    else:
        print("Failed to retrieve trivia questions. Please try again.")

if __name__ == "__main__":
    main()

