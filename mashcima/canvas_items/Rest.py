from mashcima.canvas_items.CanvasItem import CanvasItem
from typing import Optional


class Rest(CanvasItem):
    def __init__(
            self,
            duration_dots: Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        # duration dots
        assert duration_dots in [None, "*", "**"]
        self.duration_dots = duration_dots
        assert duration_dots is None  # TODO: duration dots not yet implemented for rests
