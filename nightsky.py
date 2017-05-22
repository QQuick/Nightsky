import webgl_wrapper as ww

canvas = None

def run (parentId):
    global canvas
    canvas = ww.Canvas (parentId)
