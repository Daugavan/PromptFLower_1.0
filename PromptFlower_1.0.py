import os

# Function to clear screen for better readability
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to get user input
def get_input(prompt):
    return input(prompt)

# Structured Learning Prompt
def structured_learning():
    skill = get_input("What skill or topic do you want to learn? ")
    timeframe = get_input("How long do you want to spend on this? (e.g., '4 weeks', '2 months'): ")
    return f"Act as a personal tutor to help me learn {skill}. Create a {timeframe} study plan with weekly goals, practice exercises, and quizzes. Include recommended resources like articles or videos. Ensure the difficulty increases progressively."

# Content Transformation Prompt
def content_transformation():
    tone = get_input("What tone or style should the text have? ")
    platform = get_input("For what platform or context is the summary? ")
    return f"Rewrite the following text in a {tone} style. Then provide a short summary for {platform}.\n[Paste your text here]"

# Skill Assessment & Improvement Prompt
def skill_assessment():
    skill = get_input("What skill do you want to improve? ")
    level = get_input("Describe your current level (Beginner, Intermediate, Advanced): ")
    timeframe = get_input("How much time do you want to spend on this? (e.g., '6 weeks', '3 months'): ")
    return f"Act as a {skill} coach. Assess my current level based on {level}. Provide a {timeframe} plan with daily or weekly tasks to help me progress to an advanced level."

# Finance Brainstorming Prompt
def finance_brainstorm():
    goal = get_input("What financial goal do you have? ")
    return f"Act as a general financial advisor. I need help with {goal}. Suggest possible approaches, budgeting tips, and common pitfalls to avoid. Avoid offering any direct professional, legal, or personalized advice."

# Event or Trip Planning Prompt
def event_planning():
    event_type = get_input("What type of event or trip do you want to plan? ")
    people = get_input("How many people are attending? ")
    location = get_input("Which location? (e.g., 'Paris', 'Beach resort'): ")
    budget = get_input("What is your budget? (e.g., 'Under $1500', 'Luxury', 'Mid-range'): ")
    return f"Plan a {event_type} for {people} people in {location} within a {budget} budget. Include lodging options, daily activities, and must-see attractions."

# Quick Brainstorming Session Prompt
def brainstorming_session():
    project = get_input("What are you working on? ")
    number = get_input("How many ideas do you want? ")
    goal = get_input("What is the goal? ")
    return f"I'm working on {project}. Generate {number} diverse ideas that address {goal}. Include pros, cons, and any potential challenges."

# Mental Health Journal Prompt
def mental_health_journal():
    focus = get_input("What do you want to focus on? ")
    return f"Act as a reflective journaling assistant. Ask me thoughtful questions about my day, mood, and stressors, and suggest simple mindfulness techniques. Avoid medical or diagnostic language. My focus is: {focus}."

# In-Depth Analysis Prompt
def in_depth_analysis():
    focus = get_input("What type of analysis do you need? ")
    return f"Break down complex or lengthy materials into easy-to-digest summaries, bullet points, or key insights. Focus on {focus}.\n[Paste or summarize text here]"

# Main function
def main():
    clear_screen()

    options = {
        "1": ("Structured Learning", structured_learning),
        "2": ("Content Transformation", content_transformation),
        "3": ("Skill Assessment & Improvement", skill_assessment),
        "4": ("Finance Brainstorming", finance_brainstorm),
        "5": ("Event or Trip Planning", event_planning),
        "6": ("Quick Brainstorming Session", brainstorming_session),
        "7": ("Mental Health Journal", mental_health_journal),
        "8": ("In-Depth Analysis", in_depth_analysis)
    }

    while True:
        clear_screen()
        print("\n--- Prompt Generator ---")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")

        choice = input("\nChoose a category (1-8): ")
        
        if choice in options:
            prompt = options[choice][1]()
            print("\n--- Generated Prompt ---")
            print(prompt)
        else:
            print("Invalid choice. Try again.")

        retry = input("\nGenerate another prompt? (Y/N): ").strip().lower()
        if retry not in ["y"]:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()