import os

from colorama import Fore

from data_level import DataOperations as dop


class UiOperations:
    @staticmethod
    def user_session(phrase: str, repetition: dict) -> (float, str):
        """Console user interface"""
        user_input: str = input(f'Enter phrase \"{phrase}\" in English: {os.linesep}')
        distance, best_translation = dop.find_max_string_similarity(user_input, repetition['translations'])
        diff = dop.find_user_mistakes(user_input, best_translation)

        if distance >= dop.level_excellent:  # Phrases are identical
            print(f'{Fore.GREEN}Correct!{os.linesep}')
        elif distance >= dop.level_good:  # The phrases are very similar, maybe a typo
            print(f'{Fore.RESET}Almost correct. Right answer is: ', end='')
            UiOperations._print_colored_diff(diff, best_translation)
            print(os.linesep)
        elif distance >= dop.level_mediocre:  # Phrases have a lot in common
            print(f'{Fore.RESET}Not bad. Right answer is: ', end='')
            UiOperations._print_colored_diff(diff, best_translation)
            print(os.linesep)
        else:
            print(f'{Fore.RED}Wrong. ', end='')
            print(
                f'{Fore.RESET}Right answer is: {Fore.GREEN}{best_translation}{os.linesep}'
            )

        print(Fore.RESET, end='')

        return distance, best_translation

    @staticmethod
    def _print_colored_diff(correction, reference) -> None:
        """Visualisation of user errors"""
        for i, ch in enumerate(reference):
            if correction[i]:
                print(Fore.GREEN + ch, end='')
            elif ch == ' ':
                if i >= 1 and i + 1 < len(reference):  # Emphasise the space between correct but sticky characters
                    if correction[i - 1] and correction[i + 1]:
                        print(f'{Fore.RED}_', end='')
                    else:
                        print(f'{Fore.RED} ', end='')

            else:
                print(Fore.RED + ch, end='')  # Just a letter
