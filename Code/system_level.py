import json
import os
from pathlib import Path


class FileOperations:
    @staticmethod
    def find_or_create_file(filename: str, parents_level_up: int = 2) -> str:
        """Find and open a file if it exists (include the path's logical parents), or create a new empty file"""
        if os.path.exists(filename):
            return filename
        for root, dirs, files in os.walk(Path(__file__).parents[parents_level_up]):
            if filename in files:
                return os.path.join(root, filename)

        # File doesn't exist in all project directories
        with open(filename, 'w'):  # Create file
            pass
        return filename

    @staticmethod
    def read_phrases(file_path: str) -> dict:
        """Read new phrases from file"""
        phrase_mapping: dict = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as phrf:
                for string in phrf:
                    if string[0] != '#' and '||' in string:  # No comment line and contains rus-eng separator
                        phrases_pair = list(map(str.strip, string.split('||')))

                        if len(phrases_pair) > 2:
                            print(
                                f'Error. String contains {len(phrases_pair)} "||" separators: {string}. String must contain only one "||" separator between phrases in different languages'
                            )
                        else:
                            rus_part, eng_part = phrases_pair[0], phrases_pair[1]

                            if '|' in eng_part:  # More than one English phrase
                                eng_part = list(map(str.strip, eng_part.split('|')))  # Just split into separate english phrases

                            if '|' in rus_part:  # More than one Russian phrase
                                rus_part = list(map(str.strip, rus_part.split('|')))  # Split into separate russian phrases...
                                for rus_phrase in rus_part:
                                    phrase_mapping[rus_phrase] = eng_part  # ... and save separate items

                            else:  # Single Russian phrase
                                phrase_mapping[rus_part] = eng_part
        except Exception:
            print(f'Cannot open or parse {file_path} file')

        return phrase_mapping

    @staticmethod
    def read_json_from_file(file_path: str) -> dict:
        """Read JSON data from file"""
        repetitions: dict = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                repetitions = json.load(f)
        except Exception:
            print(f'Cannot open or parse {file_path} file')

        return repetitions

    @staticmethod
    def save_json_to_file(file_path: str, repetitions: dict):
        """Save JSON data to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(repetitions, ensure_ascii=False, indent=2))
        except Exception:
            print(f'Cannot save {file_path} file')
