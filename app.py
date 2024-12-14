from flask import Flask, request, jsonify, render_template
from minilang_interpreter import MiniLangInterpreter

app = Flask(__name__)
interpreter = MiniLangInterpreter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    try:
        code = request.json.get('code', '')
        response = interpreter.run(code)
        return jsonify({'output': response})
    except Exception as e:
        return jsonify({'output': f"Error: {str(e)}"}), 400

@app.route('/game_command', methods=['POST'])
def game_command():
    game = request.json.get('game', '')
    command = request.json.get('command', '')
    
    try:
        response = interpreter.process_game_command(game, command)
        return jsonify({'output': response, 'game_over': response.lower().startswith('game over')})
    except Exception as e:
        return jsonify({'output': f"Error: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)