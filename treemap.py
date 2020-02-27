import os
import os.path
import sys
import math
import pygame
import sort_tree
from tkinter import filedialog
from directory import File, Folder


def build_tree(f, d):
    '''(Folder, str) -> int
    Build a disk usage tree of directory d, recursively,
    based on directory d's Folder class, f.
    Return the total size of the directory d.'''

    try:
        for filename in os.listdir(d):
            path = os.path.join(d, filename)
            size = os.path.getsize(path)
            if os.path.isdir(path):
                folder = Folder(path, size)
                f.files.append(folder)
                f.size += build_tree(folder, path)
            else:
                f.size += size
                f.files.append(File(path, size))
    except:
        # Just skip if access is denied
        pass
    return f.size


def draw_tree(f, screen, pos_file, x, y, w, h):
    '''(Folder/File, pygame.display, list, float, float, \
    float, float) -> None
    Draw the treemap using the tiling algorithm, recursively.'''

    if isinstance(f, Folder):
        b_x, b_y, b_w, b_h = x, y, w, h
        if f.size > 0:
            for item in f.files:
                ratio = float(item.size) / f.size
                if b_w > b_h:
                    # If directory f's rectangle is wider than it is high,
                    # draw every Files in directory f from left to right.
                    w = ratio * b_w
                    draw_tree(item, screen, pos_file, x, y, w, h)
                    x += w
                else:
                    # Otherwise, draw every Files in directory f
                    # from top to bottom.
                    h = ratio * b_h
                    draw_tree(item, screen, pos_file, x, y, w, h)
                    y += h
            # Finally, draw the white border line
            pygame.draw.rect(screen, (255, 255, 255), \
                             (b_x, b_y, b_w, b_h), 1)
    else:
        # If f is a File then simply draw its rectangle
        pygame.draw.rect(screen, f.color, (x, y, w, h))
        # pos_file is used for enhancement, to detect which File
        # is being hovered over
        pos = [x, y, x + w, y + h, f.name]
        pos_file.append(pos)

def calc_size(size):
    '''int -> string
    Convert size to KB, MB or GB accordingly'''

    sizes = ['B', 'KB', 'MB', 'GB']
    i = math.floor(math.log(size) / math.log(1024))
    
    return 'Total size: %d %s' % ((size / math.pow(1024, i)), sizes[i])

def build_treemap(d, screen_size):
    '''(str, tuple) -> None
    Main function to fully build and display the treemap using pygame.'''

    f = Folder(d, os.path.getsize(d))
    total_size = build_tree(f, d)
    sort_tree.sort_tree(f)
    s = d

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    font = pygame.font.Font(None, 20)

    pos_file = []

    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        elif event.type == pygame.MOUSEMOTION:
            # Continually update the text at the bottom of the window
            # to show the path for the file the mouse is currently
            # hovering over.
            (x, y) = pygame.mouse.get_pos()
            for pos in pos_file:
                if pos[0] < x and pos[2] > x:
                    if pos[1] < y and pos[3] > y:
                        s = pos[4]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Enhancement. Please read enhancement.txt.
            if event.button == 1:
                (x, y) = pygame.mouse.get_pos()
                for pos in pos_file:
                    if pos[0] < x and pos[2] > x:
                        if pos[1] < y and pos[3] > y:
                            if os.path.dirname(pos[4]) != d:
                                build_treemap(os.path.dirname(pos[4]), \
                                              screen_size)
                                running = False
                                pygame.quit()
                                break
            elif event.button == 3:
                if d != old_d:
                    build_treemap(os.path.dirname(d), screen_size)
                    running = False
                    pygame.quit()
                    break
        # 'break' after 'pygame.quit()', and the 'if running' statement
        # are to prevent pygame error: display Surface quit,
        if running:
            screen.fill((190, 190, 190))
            height = screen_size[1] - (2.0 * font.get_linesize())
            draw_tree(f, screen, pos_file, 0.0, font.get_linesize(),\
                      screen_size[0], height)
            text_surface = font.render('Path: ' + s, 1, (0, 0, 0))
            text_pos = (5, screen_size[1] - font.get_linesize())

            size_text_surface = font.render(calc_size(total_size), 1, (0, 0, 0))
            size_text_pos = (5, 0)
            screen.blit(text_surface, text_pos)
            screen.blit(size_text_surface, size_text_pos)
            pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    d = filedialog.askdirectory(title="Choose a directory ...", initialdir='.')
    if not d:
        sys.exit('No directory selected')
    old_d = d
    while True:
        try:
            w = int(input('Enter the width of the screen: '))
            h = int(input('Enter the height of the screen: '))
            if w > 0 and h > 0:
                break
            else:
                raise Exception
        except Exception:
            print('Width and height must be a number greater than 0')
            break
    build_treemap(d, (w, h))
