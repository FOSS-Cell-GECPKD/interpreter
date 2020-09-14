import sys
from scanner import Scanner


# TODO: Add readme
class Lox:

    def __init__(self):
        self.had_error = False

    # Core part
    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    # run file directly
    def runFile(self, path):
        # TODO: If the file doesn't exist
        # exit gracefully
        with open(path) as f:
            script = f.read()
        self.run(script)
        # exit when first error is encountered
        if self.had_error:
            # FIXME: confirm the exit code
            sys.exit(65)

    # REPL
    # stops  with ctrl+d or null entry
    def runPrompt(self,):
        while True:
            line = input("> ")
            if line == "":
                break
            self.run(line)
            # reset if any error happens
            # and continue using the REPL
            self.had_error = False

    # can be split into different module
    # currently following the jlox design
    def error(self, line, msg):
        self.report(line, "", msg)

    def report(self, line, where, msg):
        print(f"[line {line}] Error{where}: {msg}")


# TODO : move to different file if needed
# Entry point
if __name__ == '__main__':
    # FIXME: check if the argv is best practice
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
    elif len(sys.argv) == 2:
        lox.runFile(sys.argv[1])
    else:
        lox.runPrompt()
