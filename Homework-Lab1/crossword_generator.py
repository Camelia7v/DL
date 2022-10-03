from typing import List
from clues_generator import get_words_and_clues


class Orientation:
    across = "Across"
    down = "Down"


class ClueProp:
    row = 0
    col = 1
    num = 2
    dir = 3
    ans = 4
    data_index = 5


class CrossWord:
    def __init__(self, cross_word_text: str) -> None:
        self.cross_word_text = cross_word_text

    def __str__(self) -> str:
        return f"<Row>{self.cross_word_text.upper()}</Row>\n"


class Clue:
    def __init__(self,
                 row: int,
                 col: int,
                 num: int,
                 orientation: Orientation,
                 ans: str,
                 clue_text: str) -> None:
        self.row = row
        self.col = col
        self.num = num
        self.ans = ans
        self.clue_text = clue_text
        self.orientation = orientation

    def __str__(self) -> str:
        return f"<Clue Row=\"{self.row}\" " \
               f"Col=\"{self.col}\" " \
               f"Num=\"{self.num}\" " \
               f"Dir=\"{self.orientation.__str__()}\" " \
               f"Ans=\"{self.ans}\">" \
               f"![CDATA[{self.clue_text}]]</Clue>\n"


class CrossWordsGenerator:
    def __init__(self, raw_cross_words: List[str]) -> None:
        self.raw_cross_words = raw_cross_words

        self.keyword = raw_cross_words[0]
        self.used_words_proprieties_across = []
        self.used_words_proprieties_down = []
        self.used_words = []
        self.cross_words_matrix_width = self.get_cross_words_matrix_width()
        self.cross_words_matrix_height = len(raw_cross_words[0])

        self.keyword_start_column = self.cross_words_matrix_width // 2

        self.cross_words_puzzle_dimension = (self.cross_words_matrix_height, self.cross_words_matrix_width)
        self.cross_words_matrix = self.generate_cross_words_matrix()
        # for line in self.cross_words_matrix:
        #     print(line)
        self.cross_words_list = self.generate_cross_words()

    def generate_cross_words(self) -> List[CrossWord]:
        local_cross_words_list = []
        for line in self.cross_words_matrix:
            word = ""
            for character in line:
                word += character
            cross_word = CrossWord(cross_word_text=word)
            local_cross_words_list.append(cross_word)
        return local_cross_words_list

    def get_cross_words(self) -> List[CrossWord]:
        return self.cross_words_list

    def get_cross_words_matrix_width(self) -> int:
        for i in range(1, len(self.raw_cross_words)):
            for character in self.raw_cross_words[i]:
                if character in self.keyword:
                    return 2 * len(self.raw_cross_words[i]) + 1

    def get_cross_words_puzzle_dimension(self) -> (int, int):
        return self.cross_words_puzzle_dimension

    def generate_cross_words_matrix(self) -> List[List[str]]:
        local_cross_words_matrix = [['~' for _ in range(self.cross_words_matrix_width)] for _ in
                                    range(self.cross_words_matrix_height)]
        self.put_keyword_in_matrix(local_cross_words_matrix)
        words_list_copy = list.copy(self.raw_cross_words)
        for index, character in enumerate(self.keyword):
            if index % 2 == 0:
                for word in words_list_copy[1:]:
                    find_result = word.find(character)
                    if find_result != -1:
                        self.used_words.append(word)
                        words_list_copy.remove(word)
                        word_start = self.keyword_start_column - find_result
                        word_end = self.keyword_start_column + (len(word) - find_result)
                        self.put_word_in_matrix(local_cross_words_matrix=local_cross_words_matrix,
                                                start=word_start,
                                                end=word_end,
                                                word=word,
                                                orientation=Orientation.across,
                                                line=index)
                        break
        self.delete_padding(local_cross_words_matrix)
        self.set_proprieties(local_cross_words_matrix)
        return local_cross_words_matrix

    def put_keyword_in_matrix(self, local_cross_words_matrix):
        self.used_words.append(self.keyword)
        keyword_start = 0
        keyword_end = 0 + len(self.raw_cross_words[0])
        self.put_word_in_matrix(local_cross_words_matrix,
                                keyword_start,
                                keyword_end,
                                self.raw_cross_words[0],
                                Orientation.down,
                                column=self.keyword_start_column)

    def delete_padding(self, local_cross_words_matrix):
        min_left = self.cross_words_matrix_width
        max_right = 0
        for line in local_cross_words_matrix:
            index = 0
            while line[index] == '~':
                index += 1
            if index < min_left:
                min_left = index
            while index != len(line) - 1 or line[index] != '~':
                index += 1
            if index > max_right:
                max_right = index

        for i in range(len(local_cross_words_matrix)):
            local_cross_words_matrix[i] = local_cross_words_matrix[i][min_left:max_right - 1]

        self.set_cross_words_matrix_width(len(local_cross_words_matrix[0]))
        self.set_cross_words_matrix_height(len(local_cross_words_matrix))
        self.set_cross_words_puzzle_dimension((self.cross_words_matrix_height, self.cross_words_matrix_width))
        self.set_keyword_start_position(self.keyword_start_column - min_left)

    def set_proprieties(self, local_cross_words_matrix):
        local_words = []
        num = 1
        line_index = 1
        if local_cross_words_matrix[1][self.keyword_start_column] != '~':
            self.add_used_word_proprieties_down(line=1,
                                                column=self.keyword_start_column + 1,
                                                num=2,
                                                ans=self.keyword,
                                                index_in_words_list=self.raw_cross_words.index(self.keyword))
        else:
            self.add_used_word_proprieties_down(line=1,
                                                column=self.keyword_start_column + 1,
                                                num=1,
                                                ans=self.keyword,
                                                index_in_words_list=self.raw_cross_words.index(self.keyword))

        for index, line in enumerate(local_cross_words_matrix):
            local_word = ""
            if index % 2 == 0:
                for character in line:
                    local_word += character
                local_words.append(local_word)

        for item in local_words:
            if len(item.replace("~", "")) == 1:
                self.used_words.append(item.replace("~", ""))

        print(self.keyword)
        print(self.used_words)
        print(local_words)
        for index, local_word in enumerate(local_words):
            if local_cross_words_matrix[1][self.keyword_start_column] != '~' and num == 2:
                num = 3

            self.add_used_word_proprieties_across(line=line_index,
                                                  column=local_word.find(self.used_words[index + 1]) + 1,
                                                  num=num,
                                                  ans=self.used_words[index + 1],
                                                  index_in_words_list=self.raw_cross_words.index(
                                                      self.used_words[index + 1]) if len(
                                                      self.used_words[index + 1]) != 1 else -1)
            num += 1
            line_index += 2

    def add_used_word_proprieties_across(self, line, column, num, ans, index_in_words_list):
        self.used_words_proprieties_across.append(
            [line, column, num, Orientation.across.__str__(), ans, index_in_words_list])

    def add_used_word_proprieties_down(self, line, column, num, ans, index_in_words_list):
        self.used_words_proprieties_down.append(
            [line, column, num, Orientation.down.__str__(), ans, index_in_words_list])

    @staticmethod
    def put_word_in_matrix(local_cross_words_matrix, start: int, end: int, word: str, orientation: str,
                           column=0, line=0) -> None:
        consume = 0
        if orientation == Orientation.across:
            for index in range(start, end):
                local_cross_words_matrix[line][index] = word[consume].upper()
                consume += 1

        if orientation == Orientation.down:
            for index in range(start, end):
                local_cross_words_matrix[index][column] = word[consume].upper()
                consume += 1

    def set_cross_words_matrix_width(self, value):
        self.cross_words_matrix_width = value

    def set_cross_words_matrix_height(self, value):
        self.cross_words_matrix_height = value

    def set_cross_words_puzzle_dimension(self, dimension):
        self.cross_words_puzzle_dimension = dimension

    def set_keyword_start_position(self, value):
        self.keyword_start_column = value


class CluesGenerator:
    def __init__(self, raw_clues: List[str], cross_words_generator: CrossWordsGenerator) -> None:
        self.raw_clues = raw_clues
        self.cross_words_generator = cross_words_generator
        self.clues_list = self.generate_clues()

    def generate_clues(self) -> List[Clue]:
        local_clues_list = []
        local_clues_across_list = self.cross_words_generator.used_words_proprieties_across
        local_clues_down_list = self.cross_words_generator.used_words_proprieties_down

        for across_clue in local_clues_across_list:
            if len(across_clue[ClueProp.ans]) != 1:
                clue = Clue(row=across_clue[ClueProp.row],
                            col=across_clue[ClueProp.col],
                            num=across_clue[ClueProp.num],
                            orientation=across_clue[ClueProp.dir],
                            ans=across_clue[ClueProp.ans],
                            clue_text=self.raw_clues[across_clue[ClueProp.data_index]])
                local_clues_list.append(clue)

        for across_clue in local_clues_down_list:
            clue = Clue(row=across_clue[ClueProp.row],
                        col=across_clue[ClueProp.col],
                        num=across_clue[ClueProp.num],
                        orientation=across_clue[ClueProp.dir],
                        ans=across_clue[ClueProp.ans],
                        clue_text=self.raw_clues[across_clue[ClueProp.data_index]])
            local_clues_list.append(clue)

        return local_clues_list

    def get_clues(self) -> List[Clue]:
        return self.clues_list


class CrossWordsPuzzleGenerator:
    def __init__(self,
                 domain,
                 words_list: List[str],
                 clues_list: List[str]
                 ) -> None:
        self.domain = domain
        self.cross_words_generator = CrossWordsGenerator(raw_cross_words=words_list)
        self.clues_generator = CluesGenerator(raw_clues=clues_list, cross_words_generator=self.cross_words_generator)
        self.dimension = self.cross_words_generator.get_cross_words_puzzle_dimension()

        self.cross_words_list = self.cross_words_generator.get_cross_words()
        self.clues_list = self.clues_generator.get_clues()
        self.cross_words_puzzle_file_path = f"Puzzles/{domain}_cross_words_file.xpf"
        self.cross_words_puzzle_resolved_file_path = f"Puzzles/{domain}_cross_words_file(resolved).xpf"

    def create_solved_cross_words_file(self) -> None:
        self.write_header_in_file()
        self.write_grid()
        self.write_clues()
        self.write_footer()

    def create_cross_words_file(self) -> None:
        new_list = self.cross_words_generator.used_words.copy()
        new_list = new_list[1:] + [new_list[0]]
        lengths = []
        for item in new_list:
            lengths.append(len(item))

        r_file = open(self.cross_words_puzzle_resolved_file_path, "r")
        w_file = open(self.cross_words_puzzle_file_path, "w")
        text = r_file.readlines()

        for i in range(len(text)):
            if text[i] == "<Grid>\n":
                i += 1
                find_tag = text[i].find("<Row>")
                while find_tag != -1:
                    replaceable_word = text[i].replace("<Row>", "").replace("</Row>", "")
                    used_word_for_replace = ""

                    for i_p in range(len(replaceable_word)):
                        if replaceable_word[i_p] != "~":
                            used_word_for_replace += " "
                        else:
                            used_word_for_replace += "~"
                    used_word_for_replace = used_word_for_replace[0:-1]

                    text[i] = f"<Row>{used_word_for_replace}</Row>\n"
                    i += 1
                    find_tag = text[i].find("<Row>")

            if text[i] == "<Clues>\n":
                i += 1
                find_tag = text[i].find("<Clue")
                pos = 0
                while find_tag != -1:
                    find_ans = text[i].find("Ans=")
                    used_word_for_replace = text[i][0:find_ans + 5] + " " * lengths[pos] + text[i][
                                                                                           find_ans + 5 + lengths[pos]:]
                    text[i] = used_word_for_replace
                    i += 1
                    pos += 1
                    find_tag = text[i].find("<Clue")
        print(text)
        w_file.writelines(text)
        r_file.close()
        w_file.close()

    def write_header_in_file(self) -> None:
        file = open(self.cross_words_puzzle_resolved_file_path, "w")
        file.write("<?xml version='1.0' encoding='utf-8'?>\n")
        file.write("<Puzzles Version=\"1.0\">\n")
        file.write("<Puzzle>\n")
        file.write("<Size>\n")
        file.write(f"<Rows>{self.dimension[0]}</Rows>\n")
        file.write(f"<Cols>{self.dimension[1]}</Cols>\n")
        file.write("</Size>\n")
        file.close()

    def write_grid(self) -> None:
        file = open(self.cross_words_puzzle_resolved_file_path, "a")
        file.write("<Grid>\n")
        for word in self.cross_words_list:
            file.write(word.__str__())
        file.write("</Grid>\n")

    def write_clues(self) -> None:
        file = open(self.cross_words_puzzle_resolved_file_path, "a")
        file.write("<Clues>\n")
        for clue in self.clues_list:
            file.write(clue.__str__())
        file.write("</Clues>\n")

    def write_footer(self) -> None:
        file = open(self.cross_words_puzzle_resolved_file_path, "a")
        file.write("</Puzzle>\n")
        file.write("</Puzzles>\n")


if __name__ == '__main__':
    local_domain = input("Type a domain: ")
    words, clues = get_words_and_clues(local_domain)

    cross_words_puzzle_generator = CrossWordsPuzzleGenerator(local_domain, words, clues)
    cross_words_puzzle_generator.create_solved_cross_words_file()
    cross_words_puzzle_generator.create_cross_words_file()
