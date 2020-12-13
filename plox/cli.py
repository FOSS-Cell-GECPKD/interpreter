import sys
from plox.lox import Lox

# TODO : move to different file if needed
# Entry point
def main():
    # FIXME: check if the argv is best practice
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
    elif len(sys.argv) == 2:
        lox.runFile(sys.argv[1])
    else:
        lox.runPrompt()
