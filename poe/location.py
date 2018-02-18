class CharacterLocation:
    
    def __init__(self, points):
        self.points = points

    @property
    def extremes(self):
        min_x, max_x, min_y, max_y = None, None, None, None
        for x, y in self.points:
            min_x = min(x, min_x) if min_x else x
            max_x = max(x, max_x) if max_x else x
            min_y = min(y, min_y) if min_y else y
            max_y = max(y, max_y) if max_y else y
        return min_x, max_x, min_y, max_y        

def is_likely_duplicate(l1: CharacterLocation, l2: CharacterLocation):
    min_x1, max_x1, min_y1, max_y1 = l1.extremes
    min_x2, max_x2, min_y2, max_y2 = l2.extremes
    min_overlap = max(abs(min_x1 - min_x2), abs(min_y1 - min_y2)) <= 5 
    max_overlap = max(abs(max_x1 - max_x2), abs(max_y1 - max_y2)) <= 5 
    return min_overlap or max_overlap
