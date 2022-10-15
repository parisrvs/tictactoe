from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
#from tempfile import mkdtemp

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def record_move(turn, move):
    turn.append(move)


def checkgame(board):
    c=0
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                c=1
                break
        if c == 1:
            break
    if c == 0:
        return "Game Over"
    else:
        return None

def winner(board):
    if (board[0][0] == board[0][1] and board[0][1] == board[0][2]) and board[0][0] is not None:
        return board[0][0]
    elif (board[1][0] == board[1][1] and board[1][1] == board[1][2]) and board[1][0] is not None:
        return board[1][0]
    elif (board[2][0] == board[2][1] and board[2][1] == board[2][2]) and board[2][0] is not None:
        return board[2][0]
    elif (board[0][0] == board[1][0] and board[1][0] == board[2][0]) and board[0][0] is not None:
        return board[0][0]
    elif (board[0][1] == board[1][1] and board[1][1] == board[2][1]) and board[0][1] is not None:
        return board[0][1]
    elif (board[0][2] == board[1][2] and board[1][2] == board[2][2]) and board[0][2] is not None:
        return board[0][2]
    elif (board[0][0] == board[1][1] and board[1][1] == board[2][2]) and board[0][0] is not None:
        return board[0][0]
    elif (board[0][2] == board[1][1] and board[1][1] == board[2][0]) and board[0][2] is not None:
        return board[0][2]
    else:
        return None


@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None
        session["O"] = []
        session["X"] = []
  
    session["status"] = checkgame(session["board"])
    return render_template("index.html", game=session["board"], turn=session["turn"], status=session["status"], winner=session["winner"])

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):    
    if session["winner"] is not None:
        return redirect(url_for("index"))        
    move = [row, col]
    Turn = session["turn"]
    record_move(session[Turn], move)

    board = session["board"]
    board[row][col] = session["turn"]

    session["winner"] = winner(session["board"])
    if session["winner"] is not None:
        return redirect(url_for("index"))        

    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    
    return redirect(url_for("index"))

@app.route("/undo")
def undo():
    if session["winner"] is not None:
        return redirect(url_for("index"))        
    if session["status"] == "Game Over":
        return redirect(url_for("index"))        

    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    Turn = session["turn"]
    moves = session[Turn]
    if moves == []:
        if session["turn"] == "X":
            session["turn"] = "O"
        else:
            session["turn"] = "X"
        return redirect(url_for("index"))

    last_move = moves[-1]    
    row = last_move[0]
    col = last_move[1]    
    board = session["board"]
    board[row][col] = None
    moves.pop(-1)
    return redirect(url_for("index"))