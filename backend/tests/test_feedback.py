import pytest
from game import _get_feedback


def test_all_correct():
    assert _get_feedback("crane", "crane") == ["green", "green", "green", "green", "green"]

def test_all_wrong():
    assert _get_feedback("crane", "stomp") == ["gray", "gray", "gray", "gray", "gray"]

def test_all_yellow():
    assert _get_feedback("abcde", "edbca") == ["yellow", "yellow", "yellow", "yellow", "yellow"]




def test_partial_match():
    assert _get_feedback("crane", "crimp") == ["green", "green", "gray", "gray", "gray"]

def test_wrong_position():
    assert _get_feedback("crane", "rcane") == ["yellow", "yellow", "green", "green", "green"]


# Duplicate letters in guess
def test_duplicate_letter_one_yellow_one_gray():
    # answer has one 'r', guess has two — only first should be yellow
    assert _get_feedback("river", "crane") == ["yellow", "gray", "gray", "yellow", "gray"]

def test_duplicate_letter_one_green_one_gray():
    # answer is "crane", guess is "crare" — first r is green, second r should be gray
    assert _get_feedback("crare", "crane") == ["green", "green", "green", "gray", "green"]

def test_duplicate_letter_one_green_one_yellow():
    assert _get_feedback("abcab", "abcba") == ["green", "green", "green", "yellow", "yellow"]

def test_duplicate_letter_both_green():
    assert _get_feedback("aabbb", "aaccc") == ["green", "green", "gray", "gray", "gray"]

def test_duplicate_letter_both_yellow():
    assert _get_feedback("aabbb", "cccaa") == ["yellow", "yellow", "gray", "gray", "gray"]

def test_duplicate_letter_both_gray():
    assert _get_feedback("aabbb", "cccdd") == ["gray", "gray", "gray", "gray", "gray"]


# Duplicate letters in answer
def test_duplicate_letter_in_answer_one_in_guess_yelow():
    # answer has two s's, guess has one — should be yellow
    assert _get_feedback("siren", "dress") == ["yellow", "gray", "yellow", "yellow", "gray"]

def test_duplicate_letter_in_answer_one_in_guess_green():
    # answer has two s's, guess has one — should be yellow
    assert _get_feedback("abcde", "aacde") == ["green", "gray", "green", "green", "green"]

def test_duplicate_letter_in_answer_both_matched():
    assert _get_feedback("speed", "speed") == ["green", "green", "green", "green", "green"]


# Word length variants
def test_six_letter_word():
    assert _get_feedback("planet", "planet") == ["green", "green", "green", "green", "green", "green"]

def test_seven_letter_word():
    assert _get_feedback("abackus", "abacuss") == ["green", "green", "green", "green", "gray", "yellow", "green"]

def test_eight_letter_word_all_gray():
    assert _get_feedback("abcdefgh", "stuvwxyz") == ["gray","gray","gray","gray","gray","gray","gray","gray"]


