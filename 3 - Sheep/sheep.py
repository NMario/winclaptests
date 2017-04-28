#!/usr/bin/python3


def get_last_number(number):
    """
    Returns the last number Bealtrix will name before falling asleep
    """

    # Bealtrix never fall asleep.
    if number == 0:
        return 'INSOMNIA'

    # Find the last number
    digits = set(str(number))
    i = 1
    while True:
        last_number = number * (i+1)
        digits |= set(str(last_number))
        i += 1

        if len(digits) == 10:
            return last_number


if __name__ == '__main__':
    with open('c-input.in') as tests_file:
        tests = tests_file.readlines()

        # The number of test cases
        number_of_tests = int(tests[0])

        # Check Tests limits
        if number_of_tests < 1 or number_of_tests > 100:
            raise ValueError('Test limits error (T = {0})'.format(number_of_tests))

        # Check Bealtrix strategy for each test value
        for case in range(1, number_of_tests + 1):

            # The number Bleatrix has chosen
            number = int(tests[case])

            # Check Dataset limits
            if number < 0 or number > 200:
                raise ValueError('Dataset limits error (N: {0})'.format(number))

            # Get the last number she will name before falling asleep.
            result = get_last_number(number)

            print('Case #{0}: {1}'.format(case, result))
