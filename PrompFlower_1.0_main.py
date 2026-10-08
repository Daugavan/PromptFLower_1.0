import os
import sys
import subprocess
import importlib.util
import argparse

def resource_path(relative_path):
    """Returns the absolute path to a resource, works for development and for PyInstaller exe."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_models(filename="ollama_list_of_models_final.txt"):
    """Load available models from a text file using resource_path."""
    try:
        file_path = resource_path(filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip().strip('",') for line in file if line.strip()]
    except Exception:
        return ["deepseek-r1:14b"]

def prompt_generator_cmd():
    """CMD mode: collects inputs, clears screen between questions, and shows final prompt."""
    clear_console()

    models = load_models()
    print("Available AI Models:")
    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")
    model_choice = input("\nEnter model number: ").strip()
    selected_model = models[int(model_choice) - 1] if model_choice.isdigit() and 1 <= int(model_choice) <= len(models) else models[0]

    clear_console()
    goal = input("Step 1 - Goal: Clearly define what you want. ").strip()
    clear_console()
    return_format = input("Step 2 - Return Format: Specify how you want the response structured. ").strip()
    clear_console()
    warnings = input("Step 3 - Warnings: Set guardrails for accuracy. ").strip()
    clear_console()
    context_dump = input("Step 4 - Context Dump: Add background info for better results. ").strip()

    clear_console()
    print(f"Generating prompt using {selected_model}...\n")
    prompt = generate_prompt_with_local_ai(selected_model, goal, return_format, warnings, context_dump)

    clear_console()
    print("\n" + "=" * 50)
    print("AI-Generated Prompt:\n")
    print(prompt)
    print("=" * 50)
    input("\nPress Enter to return to the main menu...")

def generate_prompt_with_local_ai(model, goal, return_format, warnings, context_dump):
    """Creates a composite prompt and sends it via Ollama CLI."""
    prompt = (
        "You are an expert in crafting effective AI prompts. Create a final prompt that a user can use to query an AI. "
        "Do NOT provide a direct answer; output only the prompt text. Follow these four pillars:\n"
        "1. Goal: {goal}\n"
        "2. Return Format: {return_format}\n"
        "3. Warnings: {warnings}\n"
        "4. Context Dump: {context_dump}\n"
    ).format(goal=goal, return_format=return_format, warnings=warnings, context_dump=context_dump)

    try:
        result = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error in generating prompt: {e}")
        return prompt

def run_web_mode():
    """Web mode: starts a Flask-based web server labeled as 'PromptFlower_1.0'."""
    try:
        from flask import Flask, request, render_template_string
    except ImportError:
        print("Flask is not installed. Please install it with 'pip install flask'")
        sys.exit(1)

    app = Flask("PromptFlower_1.0")

    html_template = """<!doctype html>
    <html>
      <head><title>PromptFlower 1.0</title></head>
      <body>
        <h1>PromptFlower 1.0 - Web Interface</h1>
        <form method="post">
          <label for="model">Select AI Model:</label>
          <select name="model">
            {% for model in models %}
              <option value="{{ model }}">{{ model }}</option>
            {% endfor %}
          </select>
          <br><br>
          <label>Goal:</label><textarea name="goal" rows="2" required></textarea><br>
          <label>Return Format:</label><textarea name="return_format" rows="2" required></textarea><br>
          <label>Warnings:</label><textarea name="warnings" rows="2"></textarea><br>
          <label>Context Dump:</label><textarea name="context_dump" rows="4"></textarea><br><br>
          <input type="submit" value="Generate Prompt">
        </form>
        {% if generated_prompt %}
          <hr><h2>Generated Prompt:</h2><pre>{{ generated_prompt }}</pre>
        {% endif %}
      </body>
    </html>"""

    @app.route("/", methods=["GET", "POST"])
    def index():
        generated_prompt = None
        if request.method == "POST":
            generated_prompt = generate_prompt_with_local_ai(
                request.form.get("model"),
                request.form.get("goal"),
                request.form.get("return_format"),
                request.form.get("warnings"),
                request.form.get("context_dump")
            )
        return render_template_string(html_template, models=load_models(), generated_prompt=generated_prompt)

    print("Starting Web Mode...")
    print("Starting web server on http://127.0.0.1:5000")
    print("* Serving Flask app 'PromptFlower_1.0'")
    print("* Debug mode: off")
    print("WARNING: This is a development server. Do not use it in a production deployment.")
    print(" * Running on http://127.0.0.1:5000")

    app.run(host="127.0.0.1", port=5000, debug=False)

def run_promptflower_from_exe():
    """Dynamically load and run PromptFlower from the bundled .exe."""
    try:
        promptflower_path = resource_path("PromptFlower_1.0.py")
        if not os.path.exists(promptflower_path):
            print("Error: PromptFlower_1.0.py not found!")
            input("Press Enter to return to the main menu...")
            return

        spec = importlib.util.spec_from_file_location("PromptFlower_1_0", promptflower_path)
        promptflower = importlib.util.module_from_spec(spec)
        sys.modules["PromptFlower_1_0"] = promptflower
        spec.loader.exec_module(promptflower)
        promptflower.main()
    except Exception as e:
        print(f"Error running PromptFlower: {e}")

    input("Press Enter to return to the main menu...")

def main_menu():
    while True:
        clear_console()
        print("Choose an option:")
        print("1. Start PromptFlower 1.0 (in default mode with CMD and LLM-engine)")
        print("2. Start PromptFlower 1.0 (without an LLM-engine)")
        print("3. Start Web Mode")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            print("Starting PromptFlower 1.0 (default mode with CMD and LLM-engine)...")
            prompt_generator_cmd()
        elif choice == "2":
            print("Starting PromptFlower 1.0 (without an LLM-engine)...")
            run_promptflower_from_exe()
        elif choice == "3":
            print("Starting Web Mode...")
            run_web_mode()
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        main_menu()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--web", action="store_true")
        args = parser.parse_args()
        if args.web:
            run_web_mode()
        else:
            main_menu()
