def seconds_to_ftime(seconds):
    '''seconds to formatting time'''
    m = str(seconds // 60).rjust(2, "0")
    s = str(seconds % 60).rjust(2, "0")
    ftime = f'{m}:{s}'
    return ftime
