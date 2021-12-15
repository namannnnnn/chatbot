import wikipedia
import os


class TextExtractor:

    __pageTitle: str
    __pageId: str

    def __init__(self, pageTitle, pageId):
        self.__pageTitle = pageTitle
        self.__pageId = pageId

    def extract(self):
        fileName = "/Users/dhavalparmar/PycharmProjects/pythonProject1/text" + self.__pageTitle + ".txt"
        if not os.path.isfile(fileName):
            page = wikipedia.page(title=self.__pageTitle, pageid=self.__pageId)
            f = open(fileName, "w")
            f.write(page.content)
            f.close()

    def getText(self):
        f = open("/Users/dhavalparmar/PycharmProjects/pythonProject1/" + self.__pageTitle + ".txt", "r")
        return f.read()


from text_extractor import TextExtractor


class TextExtractorPipe:

    __textExtractors: [TextExtractor]

    def __init__(self):
        self.__textExtractors = []

    def addTextExtractor(self, textExtractor: TextExtractor):
        self.__textExtractors.append(textExtractor)

    def extract(self) -> str:
        result = ''
        for textExtractor in self.__textExtractors:
            result = result + textExtractor.getText()
        return result
