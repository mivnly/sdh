from app.schemas.users import UserCreate, UserRead

uc = UserCreate(name="William", surname="Snow", username="Wsnow", comment="Test")

uc_invalid = UserCreate(name="William", surname="Snow", username="Invalid", comment="Wrong")

ur = UserRead(id=1, name="William", surname="Snow", username="Wsnow", comment="Test")


def test_compare_with_diff_models():
    """
    This assertion method allows avoid writing multiple separate `assert` statements.
    Due to `Pydantic` we can do:

        assert uc.model_dump() == ur.model_dump(exclude={"id"})

    instead of:

        assert uc.name == ur.name
        assert uc.surname == ur.surname
        assert uc.username == ur.username
        assert uc.comment == ur.comment

    In this case when the assertion fails, pytest gives
    a clear and informative diff. For example:
    ```
    def test_compare_with_diff_models():
            assert uc.model_dump() == ur.model_dump(exclude={"id"})
    >       assert uc_invalid.model_dump() == ur.model_dump(exclude={"id"})
    E       AssertionError: assert {'comment': '...: 'Snow', ...} == {'comment': '...: 'Snow', ...}
    E
    E         Omitting 3 identical items, use -vv to show
    E         Differing items:
    E         {'username': 'Invalid'} != {'username': 'Wsnow'}
    E         {'comment': 'Wrong'} != {'comment': 'Test'}
    E         Use -v to get more diff

    test_expirements.py:28: AssertionError
    ```

    """

    assert uc.model_dump() == ur.model_dump(exclude={"id"})
    assert uc_invalid.model_dump() == ur.model_dump(exclude={"id"})
