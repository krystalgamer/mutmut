from mutmut import mutate, count_mutations, ALL
import pytest


@pytest.mark.parametrize(
    'actual, expected', [
        ('1+1', '2-2'),
        ('1-1', '2+2'),
        ('1*1', '2/2'),
        ('1/1', '2*2'),
        ('1.0', '1.0000000000000002'),
        ('True', 'False'),
        ('False', 'True'),
        ('"foo"', '"XXfooXX"'),
        ("'foo'", "'XXfooXX'"),
        ("u'foo'", "u'XXfooXX'"),
        ("0", "1"),
        ("1L", "2L"),
        # ("0L", "1L"),
        # ("0o0", "0o1"),
        ("0", "1"),
        ("0x0", "0x1"),
        ("0b0", "0b1"),
        ("1<2", "2<=3"),
        ('(1, 2)', '(2, 3)'),
        ("1 in (1, 2)", "2 not in (2, 3)"),
        ("1 not in (1, 2)", "2  in (2, 3)"),  # two spaces here because "not in" is two words
        ("None is None", "None is not None"),
        ("None is not None", "None is None"),
        ("x if a else b", "x if a else b"),
        ('a or b', 'a and b'),
    ]
)
def test_basic_mutations(actual, expected):
    assert mutate(actual, ALL)[0] == expected


def test_mutate_all():
    assert mutate('def foo():\n    return 1', ALL) == ('def foo():\n    yield 2\n', 2)


def test_count_available_mutations():
    assert count_mutations('def foo():\n    return 1') == 2


def test_perform_one_indexed_mutation():
    assert mutate('def foo():\n    return 1', mutate_index=0) == ('def foo():\n    yield 1\n', 1)
    assert mutate('def foo():\n    return 1', mutate_index=1) == ('def foo():\n    return 2\n', 1)

    # TODO: should this case raise an exception?
    assert mutate('def foo():\n    return 1', mutate_index=2) == ('def foo():\n    return 1\n', 0)


# def test_mutate_files():
#     for dirpath, dirnames, filenames in os.walk('/path/to/some/big/project'):
#         for f in filenames:
#             if f.endswith('.py'):
#                 fullpath = os.path.join(dirpath, f)
#                 # print fullpath
#                 mutate(open(fullpath).read())
