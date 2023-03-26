from typing import List

from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    KWARGS_KEY,
)


class APITextExtractor:
    def __init__(self, text: str):
        self.__apis = []

        for line in text.split('\n'):
            self.__extract_line(line)

    def __extract_line(self, line: str):
        words = line.split(' ')
        _args = []
        kw_args = {}
        index = 1

        while index < len(words):
            if self.__is_key(words[index]):
                if index + 1 >= len(words) or self.__is_key(words[index + 1]):
                    kw_args[words[index][1:]] = None
                    index += 1
                else:
                    kw_args[words[index][1:]] = self.__get_value_from_string(
                        words[index + 1])
                    index += 2
            else:
                _args.append(self.__get_value_from_string(words[index]))
                index += 1

        self.__apis.append(
            {
                API_KEY: words[0],
                ARGS_KEY: _args,
                KWARGS_KEY: kw_args,
            }
        )

    def __is_key(self, word: str) -> bool:
        print(type(self.__get_value_from_string(word)), word)
        return word.startswith('-') and type(self.__get_value_from_string(word[1:])) == str

    def __get_value_from_string(self, value: str) -> object:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
            return int(value)
        elif value.replace('.', '', 1).isdigit() or (value.startswith('-') and value[1:].replace('.', '', 1).isdigit()):
            return float(value)
        else:
            return value

    @ property
    def apis(self) -> List[dict]:
        return self.__apis
