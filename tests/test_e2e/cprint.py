def cprint(color: str, string: str) -> None:
    if color == "green":
        print("\033[32m" + string + "\033[0m")
    elif color == "blue":
        print("\033[46m" + string + "\033[0m")
    elif color == "red":
        print("\033[31m" + string + "\033[0m")
    else:
        print(string)
