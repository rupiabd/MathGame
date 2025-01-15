from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Function to generate a random math problem
def generate_problem():
    operators = ['+', '-', '*', '/']
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(operators)

    # Ensure division is exact for simplicity
    if operator == '/':
        num1 = num1 * num2

    problem = f"{num1} {operator} {num2}"
    answer = eval(problem)
    return problem, answer

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'score' not in session:
        session['score'] = 0

    if request.method == 'POST':
        # Get user's answer from the form
        user_answer = request.form.get('answer')
        correct_answer = session.get('correct_answer')

        # Check if the answer is correct
        if user_answer is not None and float(user_answer) == correct_answer:
            session['score'] += 1
            session['message'] = "Correct!"
        else:
            session['message'] = f"Incorrect! The correct answer was {correct_answer}"

    # Generate a new problem
    problem, answer = generate_problem()
    session['problem'] = problem
    session['correct_answer'] = answer

    return render_template('index.html', problem=problem, score=session['score'], message=session.get('message'))

@app.route('/reset')
def reset():
    # Reset the game score and message
    session['score'] = 0
    session.pop('message', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
