class A:
    def __init__(self, x) -> None:
        self.x = x
    
    def __ge__(self, other):
        return "Giuditta"
    
print (A(1) >= A(2))
print (A(lambda: 1) >= A(lambda: 2))