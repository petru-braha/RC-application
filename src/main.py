from dotenv import dotenv_values

from core import Config, Operator
from frontend import open_window

def main(dotenv_path: str | None = None) -> None:
    dotenv_dict = dotenv_values(dotenv_path)
    Config.init(dotenv_dict)
    Operator.start()

    if Config.cli:
        return # todo
    else:
        open_window()
    
    Operator.close()

if __name__ == "__main__":
    main()
