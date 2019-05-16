#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import sys

import colorama
import jinja2


class Config(object):
    max_attempts = 12
    allow_dupes = True
    code_length = 4

    vertical_borders = '|'
    horizontal_borders = '='
    horizontal_separator = '-'
    whitespace = ' '

    pin_char = 'O'
    code_char = 'X'

    debug = False

    colors = {
        'r': colorama.Fore.LIGHTRED_EX,
        'g': colorama.Fore.LIGHTGREEN_EX,
        'b': colorama.Fore.LIGHTBLUE_EX,
        'c': colorama.Fore.LIGHTCYAN_EX,
        'y': colorama.Fore.LIGHTYELLOW_EX,
        'w': colorama.Fore.LIGHTWHITE_EX,
        'p': colorama.Fore.LIGHTMAGENTA_EX,
    }

    human_readable_colors = {
        'r': 'Red',
        'g': 'Green',
        'b': 'Blue',
        'c': 'Cyan',
        'y': 'Yellow',
        'w': 'White',
        'p': 'Purple',
    }


class Board(object):
    def __init__(self, board_template, legend_template):
        self._board_template = board_template
        self._legend_template = legend_template

        self._attempts = []
        self._scores = []
        self._next_prompt = None

        self._code = self.generate_code()

    def say(self, message):
        if self._next_prompt is None:
            self._next_prompt = ''

        self._next_prompt = '{0}{1}\n'.format(self._next_prompt, message)

    def register_guess(self):
        next_guess = raw_input('{0}> '.format(self._next_prompt or ''))
        self._next_prompt = None

        if next_guess == 'debug':
            Config.debug = not Config.debug
            return

        if len(next_guess) != Config.code_length:
            self.say('Try a correct combination length.')
            return

        for char in next_guess:
            if char not in Config.colors:
                self.say('Nope, sorry. Not a good one.')
                return

        guess = [char for char in next_guess]

        right_colors = 0
        right_positions = 0

        accounted_colors = {col: 0 for col in self._code}

        # exact matches
        for pos, col in enumerate(guess):
            if col == self._code[pos]:
                if Config.debug:
                    self.say('Exact match! {0}->{1} is just like the code.'.format(pos + 1,
                                                                                   self.render_guess([col])))

                right_colors += 1
                right_positions += 1
                accounted_colors[col] += 1

        # just color matches
        for col, accounted_times in accounted_colors.iteritems():
            appearances_in_guess = guess.count(col)
            appearances_in_code = self._code.count(col)

            if Config.debug:
                self.say('Color {0} appears {1} times in code and {2} times in the guess. We already got {3} exact positions for it.'.format(
                    self.render_guess([col]), appearances_in_code, appearances_in_guess, accounted_times
                ))

            if accounted_times < appearances_in_code and appearances_in_guess > accounted_times:
                additional_color_matches = appearances_in_code - accounted_times

                if Config.debug:
                    self.say('Color match. {0} appears {1} unaccounted-for time(s) in the code.'.format(
                        self.render_guess([col]),
                        additional_color_matches
                    ))

                right_colors += additional_color_matches

        self._attempts.append(guess)
        self._scores.append((right_colors, right_positions))

    def render(self):
        rendered_guesses = map(self.render_guess, self._attempts)
        rendered_code = self.render_guess(
            self._code) if Config.debug else self.render_code()

        code_width = (Config.code_length * 2) - 1
        board_width = (Config.code_length * 2) + 22

        won = len(
            self._attempts) > 0 and self._scores[-1][1] == Config.code_length

        template_data = {
            'won': won,
            'widths': {
                'code': code_width,
                'board': board_width
            },
            'guesses': rendered_guesses,
            'scores': self._scores,
            'code': rendered_code,
            'turn': len(self._attempts) + 1,
            'ws': Config.whitespace,
            'hb': Config.horizontal_borders,
            'vb': Config.vertical_borders,
            'hs': Config.horizontal_separator,
            'max_attempts': Config.max_attempts,
        }

        os.system('cls' if os.name == 'nt' else 'clear')
        print self._board_template.render(**template_data)

        if not won:
            print self._legend_template.render(colors=Config.colors,
                                            human_readable_colors=Config.human_readable_colors,
                                            reset=colorama.Fore.RESET)

        if won:
            self.win()
        elif len(self._attempts) == Config.max_attempts:
            self.lose()

    def render_guess(self, guess):
        return Config.whitespace.join(['{0}{1}{2}'.format(Config.colors[char],
                                                          Config.pin_char,
                                                          colorama.Fore.RESET)
                                       for char in guess])

    def render_code(self):
        return Config.whitespace.join([Config.code_char for char in self._code])

    def generate_code(self):
        if Config.allow_dupes:
            return [random.choice(Config.colors.keys()) for _ in xrange(Config.code_length)]

        return random.sample(Config.colors.keys(), Config.code_length)

    def win(self):
        print 'Nice job! Took you long enough.'
        sys.exit(0)

    def lose(self):
        print 'You lose!'
        sys.exit(1)


def main():
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'),
                                   trim_blocks=True,
                                   lstrip_blocks=True)

    board_template = jinja_env.get_template('board.tpl')
    legend_template = jinja_env.get_template('legend.tpl')

    board = Board(board_template, legend_template)

    while True:
        board.render()
        board.register_guess()


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        try:
            print '\nOkay, bye!'
            sys.exit(130)
        except:
            pass
