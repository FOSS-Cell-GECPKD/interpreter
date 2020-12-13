import sys
from os.path import basename
from plox.scanner import Scanner


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
        # If the file doesn't exist
        # exit gracefully
        try:
            with open(path) as f:
                script = f.read()
        except IOError:
            print(f"Can't open {basename(path)} : No such file exists")
            sys.exit()
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
