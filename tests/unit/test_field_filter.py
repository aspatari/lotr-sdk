from lotr_sdk.schemas.base import FieldFilter


def test_field_filter_initialization():
    """Test that FieldFilter can be initialized with different operators."""
    # Test match operator
    filter_match = FieldFilter(match="value")
    assert filter_match.match == "value"

    # Test not_match operator
    filter_not_match = FieldFilter(not_match="value")
    assert filter_not_match.not_match == "value"

    # Test include operator
    filter_include = FieldFilter(include=["value1", "value2"])
    assert filter_include.include == ["value1", "value2"]

    # Test exclude operator
    filter_exclude = FieldFilter(exclude=["value1", "value2"])
    assert filter_exclude.exclude == ["value1", "value2"]

    # Test exists operator
    filter_exists = FieldFilter(exists=True)
    assert filter_exists.exists is True

    # Test regex operator
    filter_regex = FieldFilter(regex="pattern")
    assert filter_regex.regex == "pattern"

    # Test comparison operators
    filter_gt = FieldFilter(gt=10)
    assert filter_gt.gt == 10

    filter_gte = FieldFilter(gte=10)
    assert filter_gte.gte == 10

    filter_lt = FieldFilter(lt=10)
    assert filter_lt.lt == 10

    filter_lte = FieldFilter(lte=10)
    assert filter_lte.lte == 10


def test_field_filter_to_dict():
    """Test that FieldFilter converts to dictionary correctly."""
    # Test match operator
    filter_match = FieldFilter(match="value")
    assert filter_match.to_dict("field") == {"field": "value"}

    # Test not_match operator
    filter_not_match = FieldFilter(not_match="value")
    assert filter_not_match.to_dict("field") == {"field!": "value"}

    # Test include operator
    filter_include = FieldFilter(include=["value1", "value2"])
    assert filter_include.to_dict("field") == {"field": "value1,value2"}

    # Test exclude operator
    filter_exclude = FieldFilter(exclude=["value1", "value2"])
    assert filter_exclude.to_dict("field") == {"field!": "value1,value2"}

    # Test exists operator
    filter_exists_true = FieldFilter(exists=True)
    assert filter_exists_true.to_dict("field") == {"field": ""}

    filter_exists_false = FieldFilter(exists=False)
    assert filter_exists_false.to_dict("field") == {"!field": ""}

    # Test regex operator
    filter_regex = FieldFilter(regex="pattern")
    assert filter_regex.to_dict("field") == {"field": "pattern"}

    # Test comparison operators
    filter_gt = FieldFilter(gt=10)
    assert filter_gt.to_dict("field") == {"field>": 10}

    filter_gte = FieldFilter(gte=10)
    assert filter_gte.to_dict("field") == {"field>=": 10}

    filter_lt = FieldFilter(lt=10)
    assert filter_lt.to_dict("field") == {"field<": 10}

    filter_lte = FieldFilter(lte=10)
    assert filter_lte.to_dict("field") == {"field<=": 10}
