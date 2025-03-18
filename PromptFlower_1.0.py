#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retro-Futuristic Prompt Generator 2.0
-------------------------------------
A console-based Python script to generate various ChatGPT prompts,
now with clarifying questions to optimize each prompt’s clarity.

Features:
1. Language selection (English or Swedish)
2. Retro design using minimal ASCII/ANSI styling
3. Secure approach: no external scripting or system calls
4. Menu-driven prompt generation for 8 common use cases
5. Asks clarifying questions to tailor each prompt

Author: [Your Name]
"""

import sys
import time

# -------------------------------------------------------------------
# ASCII-ART (Retro-Futuristic Banner)
# -------------------------------------------------------------------
banner_english = r"""
 ▗▄▄▖ ▗▄▄▖  ▗▄▖ ▗▖  ▗▖▗▄▄▖▗▄▄▄▖
▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌ █  
▐▛▀▘ ▐▛▀▚▖▐▌ ▐▌▐▌  ▐▌▐▛▀▘  █  
▐▌   ▐▌ ▐▌▝▚▄▞▘▐▌  ▐▌▐▌    █  

▗▄▄▄▖▗▖    ▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌
▐▛▀▀▘▐▌   ▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘▐▛▀▚▖
▐▌   ▐▙▄▄▖▝▚▄▞▘▐▙█▟▌▐▙▄▄▖▐▌ ▐▌                                                                     
"""

banner_swedish = r"""
 ▗▄▄▖ ▗▄▄▖  ▗▄▖ ▗▖  ▗▖▗▄▄▖▗▄▄▄▖
▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▛▚▞▜▌▐▌ ▐▌ █  
▐▛▀▘ ▐▛▀▚▖▐▌ ▐▌▐▌  ▐▌▐▛▀▘  █  
▐▌   ▐▌ ▐▌▝▚▄▞▘▐▌  ▐▌▐▌    █  

▗▄▄▄▖▗▖    ▗▄▖ ▗▖ ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌ ▐▌
▐▛▀▀▘▐▌   ▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘▐▛▀▚▖
▐▌   ▐▙▄▄▖▝▚▄▞▘▐▙█▟▌▐▙▄▄▖▐▌ ▐▌                                                                 
"""

# ANSI escape codes for coloring and styling
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

# Retro-inspired color palette
COLOR_CYAN = "\033[36m"
COLOR_MAGENTA = "\033[35m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_GREEN = "\033[32m"

# -------------------------------------------------------------------
# Language Data (Menus, Banners, Base Prompts)
# -------------------------------------------------------------------
LANG_DATA = {
    "english": {
        "banner": banner_english + f"\n{DIM}A Retro-Futuristic Prompt Generator{RESET} v2.0\n",
        "welcome": "Please select your language / Välj språk:",
        "lang_option": "Press 1 for English / Tryck 2 för Svenska: ",
        "menu_title": f"{COLOR_CYAN}MAIN MENU{RESET}",
        "menu_options": [
            "1) Structured Learning",
            "2) Content Transformation",
            "3) Custom Skill Assessment & Improvement Plan",
            "4) Personal Finance Brainstorm (Disclaimer: Not professional financial advice)",
            "5) Personalized Event or Trip Planning",
            "6) Quick Brainstorming Session",
            "7) Mental Health Journal Support (Disclaimer: Not a substitute for professional help)",
            "8) In-Depth Analysis",
            "9) Exit"
        ],
        "menu_prompt": "Select an option (1-9): ",
        "invalid_option": "Invalid option. Please try again.",
        "exit_message": "Thank you for using the Retro-Futuristic Prompt Generator 2.0!",
        "continue_msg": "Press Enter to continue...",

        "base_prompts": {
            "1": (
                "Act as a personal tutor to help me learn [SkillOrTopic]. "
                "Create a [Timeframe] study plan with weekly goals, practice exercises, and quizzes. "
                "Include recommended resources like articles or videos. "
                "Ensure the difficulty increases progressively."
            ),
            "2": (
                "Rewrite the following text in a [ToneOrStyle]. "
                "Then provide a short summary for [PlatformOrContext].\n[UserText]"
            ),
            "3": (
                "Act as a [SkillArea] coach. Assess my current level based on [CurrentAbility]. "
                "Provide a [Timeframe] plan with daily or weekly tasks to help me progress to an advanced level."
            ),
            "4": (
                "Act as a general financial advisor. I need help with [FinancialGoal]. "
                "Suggest possible approaches, budgeting tips, and common pitfalls to avoid. "
                "Avoid offering any direct professional, legal, or personalized advice."
            ),
            "5": (
                "Plan a [EventType] for [NumPeople] in [Location] within a [BudgetRange]. "
                "Include lodging options, daily activities, and must-see attractions."
            ),
            "6": (
                "I'm working on [ProjectOrTopic]. Generate [NumberIdeas] diverse ideas that address [SpecificGoal]. "
                "Include pros, cons, and any potential challenges."
            ),
            "7": (
                "Act as a reflective journaling assistant. Ask me thoughtful questions about my day, mood, and stressors, "
                "and suggest simple mindfulness techniques. Avoid medical or diagnostic language. "
                "My main concern is [PersonalConcern]."
            ),
            "8": (
                "Break down complex or lengthy materials like articles, research papers, or datasets into easy-to-digest "
                "summaries, bullet points, or GLA formats. Include a concise summary (2-3 sentences) and any relevant "
                "references or data points.\n[UserText]"
            )
        },

        "questions": {
            "1": [
                "What skill or topic do you want to learn?",
                "What is your desired timeframe (e.g., 4-week, 2-month)?",
                "Any special learning focus or resources you'd like to emphasize?"
            ],
            "2": [
                "Which tone or style do you need? (e.g., Friendly, Formal, Quirky)",
                "Which platform or context do you need a summary for? (e.g., LinkedIn, Instagram)",
                "Please paste or briefly describe the text to transform."
            ],
            "3": [
                "Which skill area? (e.g., Public speaking, Digital art, French language)",
                "Describe your current ability level (e.g., Beginner, Intermediate).",
                "What is your timeframe? (e.g., 6-week, 3-month)"
            ],
            "4": [
                "What is your main financial goal? (e.g., Saving for a vacation, Reducing debt)",
                "Any specific constraints or concerns you have around budgeting or investing?"
            ],
            "5": [
                "What type of event or trip is this? (e.g., Family reunion, Bachelorette party, Team-building)",
                "How many people will attend?",
                "Where is the location (city, country, or type of destination)?",
                "What is the approximate budget range?"
            ],
            "6": [
                "What project or topic are you working on?",
                "How many ideas do you need? (e.g., 5, 10, 20)",
                "What specific goal or problem do you want to address?"
            ],
            "7": [
                "Any particular concern or situation you're reflecting on? (e.g., mild work anxiety, unwinding after a long day)"
            ],
            "8": [
                "Please paste or summarize the text or material you'd like analyzed.",
                "Any specific focus areas? (e.g., controversies, data insights, practical applications)"
            ]
        },

        "prompt_titles": {
            "1": "→ Structured Learning Prompt",
            "2": "→ Content Transformation Prompt",
            "3": "→ Custom Skill Assessment & Improvement Plan Prompt",
            "4": "→ Personal Finance Brainstorm Prompt (General info; Not professional advice)",
            "5": "→ Personalized Event or Trip Planning Prompt",
            "6": "→ Quick Brainstorming Session Prompt",
            "7": "→ Mental Health Journal Support Prompt (Not a substitute for professional help)",
            "8": "→ In-Depth Analysis Prompt"
        }
    },

    "swedish": {
        "banner": banner_swedish + f"\n{DIM}En Retro-Futuristisk Promptgenerator{RESET} v2.0\n",
        "welcome": "Vänligen välj språk / Please select your language:",
        "lang_option": "Tryck 1 för Engelska / Press 2 för Svenska: ",
        "menu_title": f"{COLOR_CYAN}HUVUDMENY{RESET}",
        "menu_options": [
            "1) Strukturerat Lärande",
            "2) Texttransformation",
            "3) Skräddarsydd Färdighetsbedömning & Förbättringsplan",
            "4) Privata Ekonomitips (Ansvarsfriskrivning: Ej professionell rådgivning)",
            "5) Personlig Event- eller Resplanering",
            "6) Snabb Idégenereringssession",
            "7) Stöd för Mental Hälsodagbok (Ej ersättning för professionell hjälp)",
            "8) Djupgående Analys",
            "9) Avsluta"
        ],
        "menu_prompt": "Välj ett alternativ (1-9): ",
        "invalid_option": "Ogiltigt val. Försök igen.",
        "exit_message": "Tack för att du använde den Retro-Futuristiska Promptgeneratorn 2.0!",
        "continue_msg": "Tryck Enter för att fortsätta...",

        "base_prompts": {
            "1": (
                "Var en personlig handledare som hjälper mig att lära mig [SkillOrTopic]. "
                "Skapa en [Timeframe] studieplan med veckomål, praktiska övningar och frågesporter. "
                "Inkludera rekommenderade resurser som artiklar eller videor. "
                "Säkerställ att svårighetsgraden ökar stegvis."
            ),
            "2": (
                "Skriv om följande text i en [ToneOrStyle]. "
                "Ge sedan en kort sammanfattning för [PlatformOrContext].\n[UserText]"
            ),
            "3": (
                "Agera som en [SkillArea]-coach. Bedöm min nuvarande nivå baserat på [CurrentAbility]. "
                "Ge en [Timeframe]-plan med dagliga eller veckovisa uppgifter för att hjälpa mig nå en avancerad nivå."
            ),
            "4": (
                "Agera som en allmän finansiell rådgivare. Jag behöver hjälp med [FinancialGoal]. "
                "Föreslå möjliga tillvägagångssätt, budgeteringstips och vanliga fallgropar att undvika. "
                "Undvik att ge direkta professionella, juridiska eller personligt anpassade råd."
            ),
            "5": (
                "Planera en [EventType] för [NumPeople] i [Location] inom en [BudgetRange]. "
                "Ta med boendealternativ, dagliga aktiviteter och sevärdheter."
            ),
            "6": (
                "Jag arbetar med [ProjectOrTopic]. Skapa [NumberIdeas] olika idéer som uppfyller [SpecificGoal]. "
                "Inkludera för- och nackdelar samt potentiella utmaningar."
            ),
            "7": (
                "Agera som en reflekterande dagboksassistent. Ställ eftertänksamma frågor om min dag, sinnesstämning "
                "och stressfaktorer, och föreslå enkla mindfulness-tekniker. Undvik medicinskt eller diagnostiskt språk. "
                "Mitt huvudsakliga problem är [PersonalConcern]."
            ),
            "8": (
                "Bryt ner komplexa eller långa material som artiklar, forskningsrapporter eller dataset till lättsmälta "
                "sammanfattningar, punktlistor eller GLA-format. Inkludera en kort sammanfattning (2-3 meningar) "
                "och eventuella relevanta referenser eller datapunkter.\n[UserText]"
            )
        },

        "questions": {
            "1": [
                "Vilken färdighet eller vilket ämne vill du lära dig?",
                "Vilken tidsram vill du ha? (t.ex. 4 veckor, 2 månader)",
                "Finns det något särskilt fokus eller resurser du vill betona?"
            ],
            "2": [
                "Vilken ton eller stil önskar du? (t.ex. Vänlig, Formell, Lekfull)",
                "Vilken plattform eller kontext är sammanfattningen för? (t.ex. LinkedIn, Instagram)",
                "Klistra in eller beskriv texten du vill transformera."
            ],
            "3": [
                "Vilket färdighetsområde? (t.ex. Presentationsteknik, Digital konst, Franska)",
                "Beskriv din nuvarande nivå (t.ex. Nybörjare, Medel).",
                "Vilken är din tidsram? (t.ex. 6 veckor, 3 månader)"
            ],
            "4": [
                "Vilket är ditt huvudsakliga ekonomiska mål? (t.ex. Spara till semester, Minska skulder)",
                "Har du några specifika begränsningar eller funderingar gällande budget eller investering?"
            ],
            "5": [
                "Vilken typ av event eller resa är det? (t.ex. Familjeträff, Möhippa, Teambuilding)",
                "Hur många personer ska delta?",
                "Vilken är platsen (stad, land eller typ av destination)?",
                "Vad är ungefärlig budget?"
            ],
            "6": [
                "Vilket projekt eller ämne arbetar du med?",
                "Hur många idéer behöver du? (t.ex. 5, 10, 20)",
                "Vilket specifikt mål eller problem vill du lösa?"
            ],
            "7": [
                "Finns det någon speciell situation eller oro du reflekterar över? (t.ex. mild jobbstress, koppla av efter en lång dag)"
            ],
            "8": [
                "Klistra in eller sammanfatta texten/materialet du vill få analyserat.",
                "Finns det något speciellt fokus? (t.ex. kontroverser, data-insikter, praktiska tillämpningar)"
            ]
        },

        "prompt_titles": {
            "1": "→ Prompt för Strukturerat Lärande",
            "2": "→ Prompt för Texttransformation",
            "3": "→ Prompt för Skräddarsydd Färdighetsbedömning & Förbättringsplan",
            "4": "→ Prompt för Privata Ekonomitips (Ej professionell rådgivning)",
            "5": "→ Prompt för Personlig Event- eller Resplan",
            "6": "→ Prompt för Snabb Idégenerering",
            "7": "→ Prompt för Stöd i Mental Hälsodagbok (Ej ersättning för professionell hjälp)",
            "8": "→ Prompt för Djupgående Analys"
        }
    }
}

# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------

def clear_console():
    """Clear the console screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(language_choice):
    """Print the retro-futuristic banner."""
    print(LANG_DATA[language_choice]["banner"])


def display_menu(language_choice):
    """Display the main menu and return user selection."""
    print(LANG_DATA[language_choice]["menu_title"])
    for option in LANG_DATA[language_choice]["menu_options"]:
        print(option)
    return input(LANG_DATA[language_choice]["menu_prompt"])


def get_language():
    """Ask the user to select a language. Returns 'english' or 'swedish'."""
    print("---------------------------------------------------")
    print(BOLD + LANG_DATA["english"]["welcome"] + RESET)
    choice = input(LANG_DATA["english"]["lang_option"])
    print("---------------------------------------------------")

    if choice.strip() == '2':
        return "swedish"
    else:
        return "english"


def ask_clarifying_questions(language_choice, category):
    """
    Ask clarifying questions for the chosen category
    and return a dictionary of the user's answers.
    """
    questions = LANG_DATA[language_choice]["questions"][category]
    answers = {}
    for i, question in enumerate(questions, start=1):
        print(f"{COLOR_GREEN}{question}{RESET}")
        ans = input(">> ")
        answers[f"Q{i}"] = ans
    return answers


def fill_prompt(language_choice, category, answers):
    """
    Fills the base prompt with user answers.
    """
    base_prompt = LANG_DATA[language_choice]["base_prompts"][category]

    # Depending on the category, replace placeholders:
    if category == "1":
        final_prompt = base_prompt.replace("[SkillOrTopic]", answers.get("Q1", ""))
        final_prompt = final_prompt.replace("[Timeframe]", answers.get("Q2", ""))
        if answers.get("Q3"):
            final_prompt += f"\nAdditional focus or resources: {answers.get('Q3', '')}"
    elif category == "2":
        final_prompt = base_prompt.replace("[ToneOrStyle]", answers.get("Q1", ""))
        final_prompt = final_prompt.replace("[PlatformOrContext]", answers.get("Q2", ""))
        final_prompt = final_prompt.replace("[UserText]", answers.get("Q3", ""))
    elif category == "3":
        final_prompt = base_prompt.replace("[SkillArea]", answers.get("Q1", ""))
        final_prompt = final_prompt.replace("[CurrentAbility]", answers.get("Q2", ""))
        final_prompt = final_prompt.replace("[Timeframe]", answers.get("Q3", ""))
    elif category == "4":
        final_prompt = base_prompt.replace("[FinancialGoal]", answers.get("Q1", ""))
        if answers.get("Q2"):
            final_prompt += f"\nAdditional note: {answers.get('Q2', '')}"
    elif category == "5":
        final_prompt = base_prompt.replace("[EventType]", answers.get("Q1", ""))
        final_prompt = final_prompt.replace("[NumPeople]", answers.get("Q2", ""))
        final_prompt = final_prompt.replace("[Location]", answers.get("Q3", ""))
        final_prompt = final_prompt.replace("[BudgetRange]", answers.get("Q4", ""))
    elif category == "6":
        final_prompt = base_prompt.replace("[ProjectOrTopic]", answers.get("Q1", ""))
        final_prompt = final_prompt.replace("[NumberIdeas]", answers.get("Q2", ""))
        final_prompt = final_prompt.replace("[SpecificGoal]", answers.get("Q3", ""))
    elif category == "7":
        final_prompt = base_prompt.replace("[PersonalConcern]", answers.get("Q1", ""))
    elif category == "8":
        final_prompt = base_prompt.replace("[UserText]", answers.get("Q1", ""))
        if answers.get("Q2"):
            final_prompt += f"\nFocus areas: {answers.get('Q2', '')}"
    else:
        final_prompt = base_prompt  # fallback if no recognized category

    return final_prompt


def show_progress_bar(duration=80, steps=100):
    """
    Displays a console progress bar that goes from 0 to 100% in the specified duration.
    """
    interval = duration / steps
    bar_length = 50  # Length of the progress bar in characters
    for i in range(steps + 1):
        progress = i  # percentage value (0 to 100)
        filled_length = int(bar_length * i / steps)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        # Skriver ut uppdaterad progressionsrad
        sys.stdout.write(f'\rProgression: {progress}% |{bar}|')
        sys.stdout.flush()
        time.sleep(interval)
    print()  # Radbrytning efter färdig progressbar


def generate_prompt(language_choice, category):
    """Asks clarifying questions, then shows the final tailored prompt."""
    lang_dict = LANG_DATA[language_choice]

    # Print the selected prompt title
    print(f"{BOLD}{lang_dict['prompt_titles'][category]}{RESET}\n")

    # 1) Ask for clarifying questions
    answers = ask_clarifying_questions(language_choice, category)
    print()

    # 2) Fill the base prompt with user answers
    final_prompt = fill_prompt(language_choice, category, answers)

    # 3) Visa progressionsbaren innan den slutgiltiga prompten skrivs ut
    print("\nGenererar din prompt, vänligen vänta...")
    show_progress_bar(duration=3)

    # 4) Show final result
    print(f"\n{BOLD}Your Tailored Prompt:{RESET}")
    print(final_prompt)


def main():
    clear_console()

    # Language selection
    language_choice = get_language()
    clear_console()
    print_banner(language_choice)

    while True:
        selection = display_menu(language_choice).strip()
        if selection == '9':
            print("\n" + LANG_DATA[language_choice]["exit_message"])
            print()
            sys.exit(0)
        elif selection in [str(i) for i in range(1, 9)]:
            clear_console()
            print_banner(language_choice)
            generate_prompt(language_choice, selection)
            print()
            input(LANG_DATA[language_choice]["continue_msg"])
            clear_console()
            print_banner(language_choice)
        else:
            print(LANG_DATA[language_choice]["invalid_option"])


if __name__ == "__main__":
    main()