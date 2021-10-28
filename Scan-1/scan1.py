import os
from typing import Tuple, Union


class StatementBlockScanner:

    def __init__(self, testFile, outputFile):
        self.file = open(testFile, "r")
        self.output = open(outputFile, "a")
        self.wordBuffer = []
        self.bufferPos = 0
        self.code = []
        self.EOF = False
        self.refinedCode = ""
        self.statementsNBlocks = []
        pass

    # get file word-by-word

    def fileReader(self):
        if self.EOF:
            return ""

        if self.bufferPos >= len(self.wordBuffer):
            line = self.file.readline()
            self.wordBuffer = line.strip().split()
            self.bufferPos = 0

            while len(line) > 0 and len(self.wordBuffer) == 0:
                line = self.file.readline()
                self.wordBuffer = line.strip().split()

            if len(line) == 0:
                self.EOF = True
                return ""

        word = self.wordBuffer[self.bufferPos]
        self.bufferPos += 1
        return word

    # flush line buffer (to be used if single line comment found)

    def flushBuffer(self):
        self.bufferPos = 0
        self.wordBuffer = self.file.readline().strip().split()

    # skip multiline comment and save back any left-over
    # example:    /* sdfsf */x = 5
    #             */x will not be fully discarded, x will be saved

    def skipMultilineComment(self):
        word = self.fileReader()
        commentEndPos = word.find("*/")
        while commentEndPos == -1 and not self.EOF:
            word = self.fileReader()
            commentEndPos = word.find("*/")
        self.bufferPos -= 1
        self.wordBuffer[self.bufferPos] = word[commentEndPos+2:]

    # scan the file, remove comments and store the code

    def scan(self):
        word = self.fileReader()
        while self.EOF == False:

            singleLineComment = word.find("//")
            if singleLineComment != -1:
                word = word[0:singleLineComment]
                self.flushBuffer()  # clear the proceeding words in the line

            multilineComment = word.find("/*")
            if multilineComment != -1:
                word = word[0:multilineComment]
                self.skipMultilineComment()

            self.code.append(word)
            word = self.fileReader()

        self.refinedCode = (" ").join(self.code)
        pass

    def breakToBlocks(self, code):

        # check if given var is minimum but not eq to -1
        # also ignores other vars if they are -1
        def checkMinNotEqNeg1(varComp, var1, var2) -> bool:
            if varComp == -1:
                return False
            if var1 != -1 and var2 != -1:
                return varComp < var1 and varComp < var2
            if var1 != -1:
                return varComp < var1
            if var2 != -1:
                return varComp < var2

            return True  # here varComp is not -1 but other are

        linesNBlocks = []
        while len(code) > 0:
            semiColon = code.find(";")
            blockOpen = code.find("{")
            blockClos = code.find("}")

            if checkMinNotEqNeg1(semiColon, blockOpen, blockClos):
                line = str(code[0:semiColon+1]).strip()
                linesNBlocks.append({
                    "line": line,
                    "block": []
                })  # include semicolon
                code = code[semiColon+1:]
            elif checkMinNotEqNeg1(blockOpen, semiColon, blockClos):
                line = str(code[0:blockOpen]).strip()
                linesNBlocks.append({
                    "line": line,
                    "block": []
                })  # do not include open bracket
                code = code[blockOpen+1:]
                (linesNBlocks[len(linesNBlocks)-1]["block"],
                 code) = self.breakToBlocks(code)
            elif checkMinNotEqNeg1(blockClos, semiColon, blockOpen):
                line = str(code[0:blockClos]).strip()
                if len(line) > 0:
                    linesNBlocks.append({
                        "line": line,
                        "block": []
                    })  # include semicolon
                code = code[blockClos+1:]
                return [linesNBlocks, code]
            else:
                # EOF
                return [linesNBlocks, code]
        return [linesNBlocks, code]

    def classify(self):
        [self.statementsNBlocks, retCode] = self.breakToBlocks(
            self.refinedCode)

    # print into test-output file

    def print(self):
        self.output.seek(0)
        self.output.truncate()
        self.output.write(str(self.statementsNBlocks).replace("\"", "\\\""))


def main():
    testFile = os.path.dirname(os.path.realpath(__file__)) + "\\test1.java"
    outputFile = os.path.dirname(os.path.realpath(__file__)) + "\\output.json"
    scanner = StatementBlockScanner(testFile, outputFile)
    scanner.scan()
    scanner.classify()
    scanner.print()


main()
