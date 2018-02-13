import unittest

def is_isogram(string):
    """Determine if a word or phrase is an isogram."""
    for i in xrange(0,len(string)):
        if string[i].isalpha() and string.lower().find(string[i].lower(),i+1) > 0:
            return False
            
    return True
    
class TestIsogram(unittest.TestCase):

    def test_empty_string(self):
        self.assertTrue(is_isogram(""))

    def test_isogram_with_only_lower_case_characters(self):
        self.assertTrue(is_isogram("isogram"))

    def test_word_with_one_duplicated_character(self):
        self.assertFalse(is_isogram("eleven"))

    def test_longest_reported_english_isogram(self):
        self.assertTrue(is_isogram("subdermatoglyphic"))

    def test_word_with_duplicated_character_in_mixed_case(self):
        self.assertFalse(is_isogram("Alphabet"))

    def test_hypothetical_isogrammic_word_with_hyphen(self):
        self.assertTrue(is_isogram("thumbscrew-japingly"))

    def test_isogram_with_duplicated_non_letter_character(self):
        self.assertTrue(is_isogram("Hjelmqvist-Gryb-Zock-Pfund-Wax"))

    def test_made_up_name_that_is_an_isogram(self):
        self.assertTrue(is_isogram("Emily Jung Schwartzkopf"))

    def test_duplicated_character_in_the_middle(self):
        self.assertFalse(is_isogram("accentor"))


if __name__ == '__main__':

    print is_isogram("lumberjacks")
    print is_isogram("background")
    print is_isogram("downstream")

    unittest.main()
    
