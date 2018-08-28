#!/usr/bin/env python2.7
#-------------------------------------------------------------------------
# HEADER_START -----------------------------------------------------------
"""


"""
#----------------------------------------------------------------------------#
#---------------------------------------------------------------- PACKAGES --#

# Built-in
from argparse import ArgumentParser, HelpFormatter
from random import randint


#----------------------------------------------------------------------------#
#------------------------------------------------------------- GLOBAL VARS --#


#----------------------------------------------------------------------------#
#--------------------------------------------------------------- FUNCTIONS --#

def get_parser():
    arg_parser = ArgumentParser(formatter_class=FormatHelp,
                                description='')
    arg_parser.add_argument('-d', '--dice', 
                            type=int, default = 5,
                            help='# of Dice to roll.')
    arg_parser.add_argument('-diff', '--difficulty', 
                            type=int, default = 3,
                            help='Difficulty Number')
    arg_parser.add_argument('-i', '--iterations', 
                            type=int,
                            help='Only use if you want to iterate multiple times for stats')
    arg_parser.add_argument('-s', '--special', 
                            action='store_true',
                            help='Iterates 10 Mil times on multiple pool and difficulties')
    

    return vars(arg_parser.parse_args())

def get_roll():
    return randint(1,6)

def get_glory(rInt):
    if rInt == 1:
        return 'Complication'
    elif rInt == 6:
        return 'Glory!'
    else:
        return None
    
def get_icons(rInt):
    if rInt == 6:
        return 2
    elif 3 < rInt:
        return 1
    else:
        return None

def roll_dice(dice):
    wrath = None
    glory = None
    icons = []
    for x in range(dice):
        roll = get_roll()
        icon = get_icons(roll)
        if icon:
            icons.append(icon)
        if wrath:
            continue
        glory = get_glory(roll)
        wrath = True
    return glory, icons

def get_shifts(dice_array, diff_num):
    icon_array = [x for x in dice_array]
    while diff_num > 0:
        if icon_array:
            icon = icon_array.pop(icon_array.index(min(icon_array)))
            diff_num -= icon
        else:
            return 'Failed'
    return len([x for x in icon_array if x == 2])

def iterate_test(num_it, dice, diff, special=False):
    glory_count = 0
    wrath_count = 0
    sux = 0
    shift_num = 0
    shift_count = 0
    for x in range(1, num_it):
        glory, icons = roll_dice(dice)
        shifts = get_shifts(icons, diff)
        if glory == 'Complication':
            wrath_count +=1
        if glory == 'Glory!':
            glory_count += 1
        if shifts != 'Failed':
            sux += 1
            if shifts > 0:
                shift_num += shifts
                shift_count += 1
    if special:
        print_string = '{0}, {1}, {2}, {3}, {4}'.format(num_it, 
                                                        dice, diff, 
                                                        round(sux/(num_it*1.00), 4)*100, 
                                                        round(shift_count/(num_it*1.00), 4)*100)
        if shift_count:
            shift_string = '{0}'.format(round(shift_num/(shift_count*1.0), 2))
            print_string = ','.join([print_string, shift_string])
        print print_string
    else:
        print 'There were {0} iterations of {1} dice at DN {2}'.format(num_it, dice, diff)
        print 'There were {0} successes. That is {1}%'.format(sux, round(sux/(num_it*1.00), 4)*100)
        #print 'Glory occured {0} times. {1}%'.format(glory_count, round(glory_count/(num_it*1.00), 4)*100)
        #print 'Wrath occured {0} times. {1}%'.format(wrath_count, round(wrath_count/(num_it*1.00), 4)*100)
        print 'Shifts occured {0} times. {1}%'.format(shift_count, round(shift_count/(num_it*1.00), 4)*100)
        if shift_count:
            print 'Avg Shifts = {0}'.format(round(shift_num/(shift_count*1.0), 2))


def return_result(dice, wrath, icons, diff, shifts):
    fail_string = 'The roll was failed. {0} Icons at DN {1}.'.format(icons, diff)
    sux_str_one = 'Rolled {0} dice at DN {1}.\n'.format(dice, diff)
    sux_str_two = 'There were {0} Icons, and {1} shifts.'.format(icons, shifts)
    if wrath:
        wrath_str = 'Wrath is {0}'.format(wrath)
        fail_string = ' '.join([fail_string, wrath_str])
        sux_str_two = ' '.join([sux_str_two, wrath_str])
    if shifts == 'Failed':
        print fail_string
    else:
        print sux_str_one
        print sux_str_two

def full_roll(dice, diff):
    glory, icons = roll_dice(dice)
    shifts = get_shifts(icons, diff)
    return_result(dice, glory, sum(icons), diff, shifts)

def main():
    parser = get_parser()
    dice = parser.get('dice', 5)
    diff = parser.get('difficulty', 3)
    iters = parser.get('iterations')
    special = parser.get('special')
    
    if special:
        iters = 10000000
        for x in range(1, 16):
            for y in range(1, 11):
                iterate_test(iters, x, y, True)
    elif iters:
        iterate_test(iters, dice, diff, False)
    else:
        full_roll(dice, diff)
    
#----------------------------------------------------------------------------#
#----------------------------------------------------------------- CLASSES --#

class FormatHelp(HelpFormatter):

    """
    Custom formatter for the command help output.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialization.
        """
        kwargs['max_help_position'] = 100
        kwargs['width'] = 200
        super(FormatHelp, self).__init__(*args, **kwargs)

    def format_help(self):
        self._action_max_length += 2
        return super(FormatHelp, self).format_help()

if __name__ == '__main__':
    main()
