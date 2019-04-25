import pytest

import Main

def test_example():
    Main.args = 'C:/Users\Test\PycharmProjects/UWIDS/vid3.MOV'

    assert(Main.vidValid())
