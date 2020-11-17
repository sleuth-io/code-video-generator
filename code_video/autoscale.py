from typing import Tuple

from attr import dataclass
from manim import config
from manim import DEFAULT_MOBJECT_TO_EDGE_BUFFER
from manim import DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
from manim import DOWN
from manim import LEFT
from manim import Mobject
from manim import np
from manim import ORIGIN
from manim import Polygon
from manim import RIGHT
from manim import UP
from wrapt import ObjectProxy


WIDTH_THIRD = (config["frame_x_radius"] * 2) / 3


@dataclass
class Bounds:
    ul: Tuple[float, float, float] = None
    ur: Tuple[float, float, float] = None
    dr: Tuple[float, float, float] = None
    dl: Tuple[float, float, float] = None

    @property
    def width(self):
        return abs(self.ul[0] - self.ur[0])

    @property
    def height(self):
        return abs(self.ur[1] - self.dr[1])

    def as_mobject(self) -> Polygon:
        return Polygon(self.ul, self.ur, self.dr, self.dl)


class AutoScaled(ObjectProxy):
    """
    Autoscales whatever it wraps on changes in placement including:
    * `next_to`
    * `to_edge`
    * `set_x`
    * `set_y`
    * `move_to`
    """

    def __init__(self, delegate: Mobject, rescale: bool = True):
        """
        Args:
            delegate: The object to scale
            rescale: Whether to rescale the object immediately or not
        """
        super().__init__(delegate)
        self._overall_scale_factor: float = 1
        self._bounds = Bounds()
        self.reset_bounds()
        if rescale:
            self.autoscale(ORIGIN)

    def scale(self, scale_factor, **kwargs):
        self._overall_scale_factor *= scale_factor
        self.__wrapped__.scale(scale_factor, **kwargs)
        return self

    def copy(self):
        result = self.__wrapped__.copy()
        wrapper = AutoScaled(result, False)
        wrapper._bounds = self._bounds
        wrapper._overall_scale_factor = self._overall_scale_factor
        return wrapper

    def next_to(self, mobject_or_point, direction=RIGHT, **kwargs):
        self.__wrapped__.next_to(mobject_or_point, direction, **kwargs)
        self._update_bounds_to_direction(direction * -1)
        self.autoscale(direction * -1)

        return self

    def move_to(self, point_or_mobject, aligned_edge=ORIGIN, coor_mask=np.array([1, 1, 1])):
        self.__wrapped__.move_to(point_or_mobject, aligned_edge, coor_mask)
        self._update_bounds_to_direction(aligned_edge)
        self.autoscale(aligned_edge)

        return self

    def set_x(self, x, direction=ORIGIN):
        self.__wrapped__.set_x(x, direction)
        self._update_bounds_to_direction(direction)
        self.autoscale(direction)

        return self

    def fill_between_x(self, x_left: float, x_right: float):
        """
        Autoscales between two X values
        """
        self._bounds.ur = np.array((x_right, self._bounds.ur[1], self._bounds.ur[2]))
        self._bounds.dr = np.array((x_right, self._bounds.dr[1], self._bounds.dr[2]))
        self.set_x(x_left, LEFT)
        self._update_bounds_to_direction(LEFT)
        self.autoscale(LEFT)

        return self

    def set_y(self, y, direction=ORIGIN):
        self.__wrapped__.set_y(y)
        self._update_bounds_to_direction(direction)
        self.autoscale(direction)

        return self

    def full_size(self):
        """
        Resets the scaling to full screen
        """
        self.reset_bounds()
        self.__wrapped__.center()
        self.autoscale(ORIGIN)
        return self

    def reset_bounds(self):
        x_rad = config["frame_x_radius"]
        y_rad = config["frame_y_radius"]
        buff = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

        self._bounds.ul = np.array((x_rad * -1 + buff, y_rad - buff, 0))
        self._bounds.ur = np.array((x_rad - buff, y_rad - buff, 0))
        self._bounds.dr = np.array((x_rad - buff, y_rad * -1 + buff, 0))
        self._bounds.dl = np.array((x_rad * -1 + buff, y_rad * -1 + buff, 0))
        return self

    def to_edge(self, edge=LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER):
        self.__wrapped__.to_edge(edge, buff)

        self._update_bounds_to_direction(edge)
        self.autoscale(edge)

        return self

    def autoscale(self, direction: np.array):
        """
        Manually autoscales in a given direction

        Args:
            direction: The direction to scale in
        """
        if not self.__wrapped__.get_width() or not self.__wrapped__.get_height():
            return
        x_scale = self._bounds.width / self.__wrapped__.get_width()
        y_scale = self._bounds.height / self.__wrapped__.get_height()
        self.scale(min(x_scale, y_scale), about_point=self._bounds.as_mobject().get_critical_point(direction))

    def _update_bounds_to_direction(self, direction: np.array):
        if direction[0] == -1:
            new_x = self.__wrapped__.get_x(LEFT)
            self._bounds.ul = np.array((new_x, self._bounds.ul[1], self._bounds.ul[2]))
            self._bounds.dl = np.array((new_x, self._bounds.dl[1], self._bounds.dl[2]))

        elif direction[0] == 1:
            new_x = self.__wrapped__.get_x(RIGHT)
            self._bounds.ur = np.array((new_x, self._bounds.ur[1], self._bounds.ur[2]))
            self._bounds.dr = np.array((new_x, self._bounds.dr[1], self._bounds.dr[2]))

        if direction[1] == -1:
            new_y = self.__wrapped__.get_y(DOWN)
            self._bounds.dr = np.array((self._bounds.dr[0], new_y, self._bounds.dr[2]))
            self._bounds.dl = np.array((self._bounds.dl[0], new_y, self._bounds.dl[2]))
        elif direction[1] == 1:
            new_y = self.__wrapped__.get_y(UP)
            self._bounds.ur = np.array((self._bounds.ur[0], new_y, self._bounds.ur[2]))
            self._bounds.ul = np.array((self._bounds.ul[0], new_y, self._bounds.ul[2]))
