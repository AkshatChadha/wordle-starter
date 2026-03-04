"""
One-time script to generate valid_guesses.txt and valid_answers.txt.

Inputs required (place in backend/ directory, not committed to repo):
  - words_all.txt: full English dictionary from https://github.com/dwyl/english-words/blob/master/words_alpha.txt
  - words_5_answers.txt: NYT Wordle answer list from https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b

Run from the backend/ directory:
  python scripts/generate_word_lists.py

Outputs (committed to repo):
  - valid_guesses.txt: all valid 5-8 letter English words
  - valid_answers.txt: NYT curated 5-letter answers (to avoid plurals) + 6-8 letter words from full dictionary (this may include plurals)
"""

# Load full dictionary, filter to 5-8 letters
with open("words_all.txt") as f:
    all_words = [w.strip().lower() for w in f if w.strip().isalpha()]

valid_guesses = [w for w in all_words if 5 <= len(w) <= 8]

# Load NYT 5-letter answers
with open("words_5_answers.txt") as f:
    nyt_5 = [w.strip().lower() for w in f if len(w.strip()) == 5 and w.strip().isalpha()]

# 6-8 letter answers come from the full dictionary
long_answers = [w for w in all_words if 6 <= len(w) <= 8]

valid_answers = nyt_5 + long_answers

# Write outputs
with open("valid_guesses.txt", "w") as f:
    f.write("\n".join(valid_guesses))

with open("valid_answers.txt", "w") as f:
    f.write("\n".join(valid_answers))

print(f"valid_guesses.txt: {len(valid_guesses)} words")
print(f"valid_answers.txt: {len(valid_answers)} words ({len(nyt_5)} five-letter NYT + {len(long_answers)} six-to-eight letter)")