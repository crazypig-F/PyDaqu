def o(p):
    def outer(func):
        def inner(*args, **kwargs):
            print(p)
            func()

        return inner

    return outer


@o("hello")
def f():
    print(1)


f()
