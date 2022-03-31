from typing import Any, Dict, Optional, Tuple

class StateMachine:
    state: Dict[str, Any]

    def __init__(self):
        self.state = dict()
    
    def handle(self, cmd: Tuple[str]) -> Optional[Any]:
        command, *arguments = cmd
        if command == "get":
            key, = arguments
            if not isinstance(key, str):
                raise TypeError("Key must be a string")
            return self.state[key]
        if command == "set":
            key, value = arguments
            if not isinstance(key, str):
                raise TypeError("Key must be a string")
            self.state[key] = value
            return
        if command == "del":
            key, = arguments
            if not isinstance(key, str):
                raise TypeError("Key must be a string")
            del self.state[key]
            return
        raise NotImplementedError(command)
