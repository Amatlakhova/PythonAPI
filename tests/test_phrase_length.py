class TestPhraseLength:
    def test_phrase_length(self):
        text = input("Please enter text less than 15 symbols: ")
        print("You entered: " + text)

        expected_length = 15
        actual_length = len(text)

        assert actual_length <= expected_length, f"Length of entered text is > 15 symbols. Actual length is {actual_length}"
