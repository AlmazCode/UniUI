import sys, os, inspect, time, linecache, ast

class Color:

    class Style:

        RESET:          str = '\033[0m'
        BOLD:           str = '\033[1m'
        DIM:            str = '\033[2m'
        ITALIC:         str = '\033[3m'
        UNDERLINE:      str = '\033[4m'
        BLINK:          str = '\033[5m'
        INVERSE:        str = '\033[7m'
        HIDDEN:         str = '\033[8m'
        STRIKETHROUGH:  str = '\033[9m'
    
    class Fore:

        BLACK:          str = '\033[30m'
        RED:            str = '\033[31m'
        GREEN:          str = '\033[32m'
        YELLOW:         str = '\033[33m'
        BLUE:           str = '\033[34m'
        MAGENTA:        str = '\033[35m'
        CYAN:           str = '\033[36m'
        WHITE:          str = '\033[37m'
        BRIGHT_BLACK:   str = '\033[90m'
        BRIGHT_RED:     str = '\033[91m'
        BRIGHT_GREEN:   str = '\033[92m'
        BRIGHT_YELLOW:  str = '\033[93m'
        BRIGHT_BLUE:    str = '\033[94m'
        BRIGHT_MAGENTA: str = '\033[95m'
        BRIGHT_CYAN:    str = '\033[96m'
        BRIGHT_WHITE:   str = '\033[97m'
    
    class Back:

        BLACK:          str = '\033[40m'
        RED:            str = '\033[41m'
        GREEN:          str = '\033[42m'
        YELLOW:         str = '\033[43m'
        BLUE:           str = '\033[44m'
        MAGENTA:        str = '\033[45m'
        CYAN:           str = '\033[46m'
        WHITE:          str = '\033[47m'
        BRIGHT_BLACK:   str = '\033[100m'
        BRIGHT_RED:     str = '\033[101m'
        BRIGHT_GREEN:   str = '\033[102m'
        BRIGHT_YELLOW:  str = '\033[103m'
        BRIGHT_BLUE:    str = '\033[104m'
        BRIGHT_MAGENTA: str = '\033[105m'
        BRIGHT_CYAN:    str = '\033[106m'
        BRIGHT_WHITE:   str = '\033[107m'

class CallerInfo:
    def __init__(self, filename: str, lineno: int, code_context: list[str] | str | None):
        self.filename = filename
        self.lineno = lineno
        self.code_context = code_context

    def __repr__(self):
        return f"CallerInfo(filename={self.filename!r}, lineno={self.lineno}, code_context={self.code_context!r})"

class Console:

    @staticmethod
    def _get_formatted_time() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def _print_message(message: str, type: str, color: str, print_extra_info: bool = True,
                       lineno_color: str = '', filename_color: str = '', code_context_color: str = '',
                       custom_info: bool = False, caller_info: CallerInfo = None
    ) -> None:
        
        if print_extra_info:
            info = Console._get_root_caller_info() if not custom_info else caller_info
            print(
                f"{color}UniUI {type} in " + 
                f"{filename_color}\"{info.filename}\"{Color.Style.RESET if filename_color else ''}" + 
                f", {color}line {lineno_color}{info.lineno}{Color.Style.RESET if lineno_color else ''}:" + 
                f"\n  {code_context_color}{info.code_context}{Color.Style.RESET if code_context_color else ''}" + 
                f"\n{color}{message}{Color.Style.RESET}"
            )
        else:
            print(f"[{Console._get_formatted_time()}] {color}UniUI : {message}{Color.Style.RESET}")
    
    @staticmethod
    def _get_root_caller_info() -> CallerInfo:
        stack = inspect.stack()

        update_index = None
        for i, frame in enumerate(stack):
            if frame.function == "update":
                update_index = i
                break

        if update_index is not None and update_index + 1 < len(stack):
            target_frame = stack[update_index]
        else:
            target_frame = stack[-1]

        filename = target_frame.filename
        lineno = target_frame.lineno

        source_lines = []
        offset = 0
        
        while 1:
            line = linecache.getline(filename, lineno + offset)
            if not line:
                break
            source_lines.append(line)
            try:
                ast.parse("".join(source_lines))
                break
            except SyntaxError:
                ...
            offset += 1

        code_context = "".join(source_lines).strip() if source_lines else None

        return CallerInfo(filename, lineno, code_context)

    @staticmethod
    def Log(message: str) -> None:
        Console._print_message(message, "Log", Color.Fore.WHITE, False)
    
    @staticmethod
    def error(message: str, custom_info: bool = False, caller_info: CallerInfo = None) -> None:
        Console._print_message(
            message, "Error", Color.Fore.RED, True,
            lineno_color = Color.Style.RESET,
            filename_color = Color.Fore.CYAN,
            code_context_color = Color.Style.RESET,
            custom_info = custom_info,
            caller_info = caller_info
        )
    
    @staticmethod
    def warning(message: str, custom_info: bool = False, caller_info: CallerInfo = None) -> None:
        Console._print_message(
            message, "Warning", Color.Fore.YELLOW, True,
            lineno_color = Color.Style.RESET,
            filename_color = Color.Fore.CYAN,
            code_context_color = Color.Style.RESET,
            custom_info = custom_info,
            caller_info = caller_info
        )
    

    @staticmethod
    def clear() -> None:
        os.system("cls" if sys.platform == "win32" else "clear -r")