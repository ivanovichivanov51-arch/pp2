import pygame

def flood_fill(surface, x, y, new_color):
    # Ағымдағы түсті алу
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    # Рекурсия орнына кезек (queue) қолданамыз (Python-да рекурсия шегі аз)
    pixels_to_fill = [(x, y)]
    width, height = surface.get_size()

    while pixels_to_fill:
        cx, cy = pixels_to_fill.pop()
        if surface.get_at((cx, cy)) != target_color:
            continue
        
        surface.set_at((cx, cy), new_color)
        
        # Көрші пиксельдерді тексеру
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny)) == target_color:
                    pixels_to_fill.append((nx, ny))