from pathlib import Path

import moderngl_window as mglw
from pyrr import Matrix44
import moderngl

import moderngl_tmx as tmx


class TileTest(mglw.WindowConfig):
    """
    Simple test rendering a tilemap.

    Controls:
        Mouse drag : Move the tilemap around
        mouse wheel: Change the zoom / projection
    """
    gl_version = 3, 3
    title = "Tile Test"
    resource_dir = (Path(__file__) / '../resources').absolute()
    aspect_ratio = None
    window_size = 1280, 720
    samples = 16

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.level = tmx.load_level(self.resource_dir / 'examples/arcade_example' / 'map_with_ladders.tmx',
                                    ctx=self.ctx)
        self.zoom_level = 5.0  # For zooming the projection
        self.position = 0, 0  # For moving the map around with mouse
        self.resize(*self.wnd.buffer_size)

    def render(self, time: float, frame_time: float) -> None:
        self.ctx.clear()
        self.ctx.enable(moderngl.BLEND)

        # self.level.render_layer(layer_id=1, projection=self.proj, pos=self.position)
        # self.level.render_layer(layer_id=0, projection=self.proj, pos=self.position)
        self.level.render_all(projection=self.proj, pos=self.position)

    def mouse_drag_event(self, x, y, dx, dy):
        """Move the map around"""
        self.position = ((self.position[0] + dx / (1 / self.zoom_level)),
                         (self.position[1] - dy / (1 / self.zoom_level)))

    def mouse_scroll_event(self, x, y):
        """Basic projection scaling"""
        if y > 0:
            self.zoom_level *= 1.05
        elif y < 0:
            self.zoom_level *= 0.95

        self.zoom_level = min(max(self.zoom_level, 0.1), 10.0)
        self.resize(*self.wnd.buffer_size)

    def resize(self, width, height):
        """Recalculate projection"""
        self.proj = Matrix44.orthogonal_projection(
            0, width * self.zoom_level,
            0, height * self.zoom_level,
            -1.0, 1.0,
            dtype='f4'
        )


if __name__ == '__main__':
    # noinspection PyTypeChecker
    mglw.run_window_config(TileTest)
