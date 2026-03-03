# Особенности тестирования

- Объект тестирования - web-приложение. Большинство операций связаны с вводом и выводом. Поэтому используется `pytest_asyncio` для ускорения выполнения тестов;
- Для каждого теста создаются отдельные тестовые данные, чтобы избежать гонки за ресурс;
- В тестах проверяется схема json из ответа через `Model.model_validate(json_obj)` из Pydantic.

При выполнении теста логи пишутся в файл, в папке `logs` (игнорируется git'ом). Пример:

```text
2026-03-03 14:35:01 | INFO | conftest.py::users_url | Using url: http://127.0.0.1:8000/api/v1/users/
2026-03-03 14:35:02 | INFO | conftest.py::delete_test_users | Deleting users with IDs: [68, 69]
2026-03-03 14:35:02 | INFO | conftest.py::add_test_users | Added user: 
{
    "name": null,
    "surname": null,
    "comment": null,
    "username": "TestUserRequiredFields_20260303-143502.281",
    "role": "user"
}
2026-03-03 14:35:02 | INFO | conftest.py::add_test_users | Added user: 
{
    "name": "TestUserName",
    "surname": "TestUserSurname",
    "comment": "User for testing",
    "username": "TestUserAllFields_20260303-143502.281",
    "role": "user"
}
2026-03-03 14:35:02 | INFO | test_users.py::test_users_get | Got users:
[
    {
        "name": null,
        "surname": null,
        "comment": null,
        "id": 1,
        "username": "cgntv",
        "role": "user"
    },
    {
        "name": "Stan",
        "surname": "Brown",
        "comment": "Testing",
        "id": 25,
        "username": "Stan",
        "role": "user"
    },
...
```