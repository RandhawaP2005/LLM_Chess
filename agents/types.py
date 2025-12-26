from dataclasses import dataclass

@dataclass(frozen=True)
class MoveRequest:
    fen: str
    legal_move_list: list[str]
    move_history: list[str]


