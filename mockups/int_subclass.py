class CrazyInt(int):
    def __add__(self, other):
        return 17

my_int = int.__new__(CrazyInt, 1)
print(my_int)
print(2 + my_int)
