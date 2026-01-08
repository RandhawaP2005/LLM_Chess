from agents.agents_types import MoveRequest

class MoveRequestParser:
    def parse_move(self, move_req: MoveRequest) -> str:
        legal_moves_lst = move_req.legal_move_list
        move_history = move_req.move_history
        legal_moves_str = ""
        move_history_str = ""

        for move in legal_moves_lst:
            legal_moves_str += str(move) + " "
        legal_moves_str = legal_moves_str[:-1].replace("[", "").replace("]", "").replace("'", "").strip()

        print(legal_moves_str + "\n")
        for move in move_history:
            move_history_str += str(move) + " "
        move_history_str = move_history_str[:-1].strip()

        print(move_history_str + "\n")
        return "Board: " + "\n" + move_req.game_board + "\n" + "FEN: " + move_req.fen + "\n" + "Legal Moves: " + legal_moves_str + "\n" + "Alliance: " + move_req.alliance






