

def trigger(a=0,b=1):
    yield 0
    yield 1

def viewMainOn():
    viewMain=False
    temp= next(trigger())
    if  temp == 0:
        viewMain=True
    else:
        viewMain=False
    return viewMain