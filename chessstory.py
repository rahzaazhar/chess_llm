import chess.pgn
import chess.svg
import chess.engine
import ollama

system_prompt = """You are a prolific story teller with an immense knowledge of chess. You are tasked with creating an 
                    engaging story for a given game of chess. 
                    
                    ### Representation of the Game of Chess ###
                    The game of chess is represented as follows each line of text represents a valid move by either the black or white player along with an associated 
                    Score. Score corresponds to the centipawn score of the current chess position observed from white's
                    perspective. A positive Score value indicates an advantage for white and disadvantage for black the converse
                    also holds. Greater the value greater is the advantage. Another detail to remember #-n indicates white checkmate 
                    in n moves and #+n indicates black checkmate in n moves. Here some examples illustrating how the Score works:   
                    
                    Examples 
                    1) Score: +300 (implies white is up by 300 centipawns or to 3 pawns while black is down by
                    300 centipawns or 3 pawns.)

                    2) Score: -200 (implies white is down by 200 centipawns or to 2 pawns while black is up by
                    200 centipawns or 2 pawns.)

                    3) Score: #-1  (implies white checkmate in 1 move)

                    4) Score: #+3 (implies black checkmate in 3 moves)

                    ### Points to Keep in mind while writing the story ###
                    *Mention all the moves made of the the game in the story, while keeping the story entertaining

                    *The Score is to be only used as a proxy to identify key moments in the game and use this 
                    information to spice up the narrative for those key moments. 
                    
                    *DONOT MENTION THE SCORE IN THE STORY AT ALL.
                    """

class ChessStoryGen:
    def __init__(self, system_prompt : str) -> None:
        self.engine = chess.engine.SimpleEngine.popen_uci("./stockfish/src/stockfish")
        self.colours = {True: 'white', False: 'black'}
        self.system_prompt = system_prompt
    
    def gen_move_description(self, move : chess.Move, piece : chess.Piece) -> str:
        a2b = move.uci()
        a2b = a2b[0:2]+'->'+a2b[2:4]
        
        return f"{self.colours[piece.color]} plays {chess.piece_name(piece.piece_type)} {a2b}"

    def analyse(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=10))
        return info['score']
    
    def generate_story(self, pgn):
        #pgn = open('sample.pgn')
        game = chess.pgn.read_game(pgn)
        board = game.board()
        llm_input = ''
        for move in game.mainline_moves():
            piece = board.piece_at(move.from_square)
            move_description = self.gen_move_description(move, piece)
            board.push(move)
            score = self.analyse(board)
            # normalise scores from white's perspective
            score = score.white()
            text = move_description + f"   (Score: {score})"
            llm_input += text+'\n'



        prompt = 'Write a long story for the following Chess Game:\n'+llm_input
        response = ollama.generate(model='llama3', prompt=prompt, system=self.system_prompt)

        return response["response"]


    
    
