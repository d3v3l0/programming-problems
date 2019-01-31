import graphs.pathfinding.heuristic_search as heuristic_search
import graphs.pathfinding.util as util
import graphs.pathfinding.drawing as drawing

from curses import wrapper

MAZES_DIR = 'graphs/pathfinding/maze_files'
MAZE_FILE = 'cave.txt'

def main(screen):
    drawing.initialize_curses(screen)
    maze = util.parse_maze(MAZES_DIR + '/' + MAZE_FILE)
    modified_maze = heuristic_search.a_star_search(maze)
    drawing.curses_render(modified_maze)


if __name__ == '__main__':
  wrapper(main)
