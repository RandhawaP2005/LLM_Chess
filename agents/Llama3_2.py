import ollama
import requests
import json

from agents.agents_types import MoveRequest
from agents.move_request_parser import MoveRequestParser

class Llama3_1:
    name = "Llama3_1"
    move_parser = MoveRequestParser()

    def choose_move(self, request: MoveRequest):
        req = self.move_parser.parse_move(request)

        response = ollama.chat(
            model = "chess_llama3.1:latest",
            messages=[
                {"role" : "user", "content" : req + "\n" + "REMINDER: Return only one UCI move. Do not add any other text."}
            ]
        )

        print(response)

        return response["message"]["content"].strip()






