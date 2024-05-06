from sql_app.schemas import ToDo


def test_create_todo_with_valid_data():
    todo_data = {
        "id": 1,
        "title": "Test Todo",
        "description": "This is a test todo",
        "is_done": False
    }
    todo = ToDo(**todo_data)
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo"
    assert todo.is_done == False


def test_todo_initialization():
    todo = ToDo(id=1, title="Test Todo",
                description="Test Description", is_done=False)
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.is_done == False


def test_todo_attributes():
    todo = ToDo(id=1, title="Test Todo",
                description="Test Description", is_done=False)
    assert isinstance(todo.id, int)
    assert isinstance(todo.title, str)
    assert isinstance(todo.description, str)
    assert isinstance(todo.is_done, bool)


def test_config_class_attribute():
    assert ToDo.Config.from_attributes == True


def test_todo_attribute_data_types():
    todo = ToDo(id=1, title="Test Todo",
                description="Test Description", is_done=False)
    assert isinstance(todo.id, int)
    assert isinstance(todo.title, str)
    assert isinstance(todo.description, str)
    assert isinstance(todo.is_done, bool)
