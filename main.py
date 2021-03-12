# This is a sample Python script.

# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+Shift+B to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    import dateutil.parser
    yourdate = dateutil.parser.parse('2007-03-04T23:59:59.999Z')
    print(yourdate.__class__)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
