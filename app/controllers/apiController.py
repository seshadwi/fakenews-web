from ..library import NewsCatcher

def indentify():
    return {
        'test' : "test"
    }


def syncNews():
    data = NewsCatcher.catchNews("SALAH")
    # TODO : SAVE TO DB AFTER DONE REQUEST
    return {
        "data": data
    }