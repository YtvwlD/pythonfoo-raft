from typing import Any, Dict, Optional, Tuple

class StateMachine:
    state: Dict[str, Any]

    def __init__(self):
        self.state = dict()
    
    def handle(self, cmd: Tuple[str]) -> Optional[Any]:
        command, *arguments = cmd
        if command == "get":
            key, = arguments
            return self.state.get(key)
        if command == "set":
            key, value = arguments
            self.state[key] = value
            return
        if command == "del":
            key, = arguments
            if key in self.state:
                del self.state[key]
            return
        raise NotImplementedError(command)
