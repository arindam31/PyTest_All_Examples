import time

def some_random_function():
    # This function serves as an example of some timetaking process
    # which we dont care. We just need it in out own function.
    print("I got called too")
    time.sleep(10)
    return {
        "stored": True,
        "location": "some_location"
    }

def my_new_function():
    data = some_random_function()
    new_path = f"{data['location']}/images"
    return new_path