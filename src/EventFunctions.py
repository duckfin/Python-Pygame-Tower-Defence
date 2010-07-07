
def leftSelectedTower(event,selected):
    for text,rect,cb in selected.buttonlist:
        if rect.collidepoint(event.dict['pos']):
            cb()
