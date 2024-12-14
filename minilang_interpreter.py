import time
import random
import math

class MiniLangInterpreter:
    def __init__(self):
        self.variables = {}
        self.current_game = None
        self.game_state = {
            "cookie_game": {
                "ingredients": [],
                "cookies_baked": 0,
                "points": 0
            },
            "dark_room": {
                "collected_wood": 0,
                "survival_days": 0
            }
        }

    def show(self, expression):
        if expression in self.variables:
            return str(self.variables[expression])

        expression = expression.strip()
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error: {str(e)}"

    def set_variable(self, name, value):
        self.variables[name] = value
        return f"Variable {name} set to {value}"

    def getinp(self, prompt):
        return prompt

    def run(self, code):
        commands = [cmd.strip() for cmd in code.split(';') if cmd.strip()]
        results = []
        for cmd in commands:
            if cmd == "help":
                results.append(self.show_help())
            elif cmd == "cookie_game":
                results.append(self.start_cookie_game())
            elif cmd == "dark_room":
                results.append(self.start_dark_room_game())
            elif "=" in cmd:
                var_name, value = cmd.split("=")
                var_name = var_name.strip()
                value = value.strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                self.set_variable(var_name, value)
                results.append(f"Variable {var_name} set to {value}")
            elif "show" in cmd:
                expression = cmd.replace("show", "").strip()
                results.append(self.show(expression))
            elif "getinp" in cmd:
                prompt = cmd.replace("getinp", "").strip()
                results.append(self.getinp(prompt))
            elif cmd.startswith("add "):
                results.append(self.perform_math_operation(cmd, "+"))
            elif cmd.startswith("subtract "):
                results.append(self.perform_math_operation(cmd, "-"))
            elif cmd.startswith("multiply "):
                results.append(self.perform_math_operation(cmd, "*"))
            elif cmd.startswith("divide "):
                results.append(self.perform_math_operation(cmd, "/"))

        return "\n".join(results)

    def process_game_command(self, game, command):
        if game == "cookie_game":
            return self.process_cookie_game_command(command)
        elif game == "dark_room":
            return self.process_dark_room_command(command)
        else:
            return "Invalid game mode"
    
    def process_cookie_game_command(self, command):
        state = self.game_state["cookie_game"]
        
        if command == "flour":
            if "flour" not in state["ingredients"]:
                state["ingredients"].append("flour")
                return "Added flour to ingredients."
            return "Flour is already in ingredients."
        
        elif command == "sugar":
            if "sugar" not in state["ingredients"]:
                state["ingredients"].append("sugar")
                return "Added sugar to ingredients."
            return "Sugar is already in ingredients."
        
        elif command == "bake":
            if len(state["ingredients"]) == 2:
                state["cookies_baked"] += 1
                state["points"] += 10
                return f"Baked a batch of cookies! You now have {state['cookies_baked']} cookies and {state['points']} points."
            return "You need flour and sugar to bake cookies!"
        
        elif command == "sell":
            if state["cookies_baked"] > 0:
                points_earned = state["cookies_baked"] * 5
                state["points"] += points_earned
                state["cookies_baked"] = 0
                return f"Sold all cookies! Earned {points_earned} points. Total points: {state['points']}"
            return "You have no cookies to sell!"
        
        elif command == "exit":
            final_points = state["points"]
            self.game_state["cookie_game"] = {
                "ingredients": [],
                "cookies_baked": 0,
                "points": 0
            }
            return f"Game Over! You earned a total of {final_points} points."
        
        else:
            return "Invalid command. Try 'flour', 'sugar', 'bake', 'sell', or 'exit'"
    
    def process_dark_room_command(self, command):
        state = self.game_state["dark_room"]
        
        if command == "1":
            state["survival_days"] += 1
            return f"You stayed in place. Survival is tough. Days survived: {state['survival_days']}"
        
        elif command == "2":
            state["collected_wood"] += 1
            state["survival_days"] += 1
            return f"You collected some wood. Might be useful later. Wood collected: {state['collected_wood']}. Days survived: {state['survival_days']}"
        
        elif command == "exit":
            final_days = state["survival_days"]
            final_wood = state["collected_wood"]
            self.game_state["dark_room"] = {
                "collected_wood": 0,
                "survival_days": 0
            }
            return f"Game Over! You survived {final_days} days and collected {final_wood} wood."
        
        else:
            return "Invalid command. Try '1', '2', or 'exit'"

    def show_help(self):
        return """MiniLang Commands:
show -- for print
getinp -- to get input from user
cookie_game -- to run the cookie game 
dark_room -- to run dark room game
= -- to set variables
add/subtract/multiply/divide -- for mathematical operations"""

    def start_cookie_game(self):
        self.game_state["cookie_game"] = {
            "ingredients": [],
            "cookies_baked": 0,
            "points": 0
        }
        return """
Welcome to Cookie Baking Game!
You need to bake and sell cookies to earn points.
Commands:
- 'flour': Add flour to ingredients
- 'sugar': Add sugar to ingredients
- 'bake': Bake cookies (needs flour and sugar)
- 'sell': Sell your cookies
- 'exit': End the game
"""

    def start_dark_room_game(self):
        self.game_state["dark_room"] = {
            "collected_wood": 0,
            "survival_days": 0
        }
        return """
A plane crashed into an island. All people died. You are the only survivor.
The real challenge begins now.
Options:
1. Stay here (survive a day)
2. Travel 20m and collect wood
Type 1, 2, or 'exit' to end game
"""

