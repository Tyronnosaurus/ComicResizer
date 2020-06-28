
def cleanPath(path):
    #In Windows, Alt+RightClick on a file lets the user "Copy as path". This string contains two quotemarks,
    # which we remove automatically so that the user doesn't have to do it manually
    if (path[0] == '"'):
        path = path[1:]

    if (path[-1] == '"'):
        path = path[:-1]

    return (path)