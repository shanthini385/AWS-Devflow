# app.py
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='static')

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        a, b, c = combo
        if board[a] != '' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_board_full(board):
    return all(cell != '' for cell in board)

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':  # AI wins
        return 1
    elif winner == 'X':  # Human wins
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/ai-move', methods=['POST'])
def ai_move():
    data = request.get_json()
    board = data.get('board', [''] * 9)
    
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                best_move = i
    
    return jsonify({'move': best_move})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
