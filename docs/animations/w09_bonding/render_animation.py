from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from render_teaching_animation import render

if __name__ == '__main__':
    render(Path(__file__).resolve().parent)
