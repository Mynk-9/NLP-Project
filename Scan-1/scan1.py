import os


class StatementBlockScanner:

    def __init__(self, testFile, outputFile):
        self.file = open(testFile, "r")
        self.output = open(outputFile, "a")
        self.wordBuffer = []
        self.bufferPos = 0
        self.code = []
        self.EOF = False
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

    # flush line buffer (to be used if single line comment founf)

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

    # scan the file and store the code

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

        pass

    # print into test-output file

    def print(self):
        self.output.seek(0)
        self.output.truncate()
        for word in self.code:
            self.output.write(word + " ")


def main():
    testFile = os.path.dirname(os.path.realpath(__file__)) + "\\test1.java"
    outputFile = os.path.dirname(os.path.realpath(__file__)) + "\\output.java"
    scanner = StatementBlockScanner(testFile, outputFile)
    scanner.scan()
    scanner.print()


main()
