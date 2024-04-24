import abc


class DrawEngine(abc.ABC):
    @abc.abstractmethod
    def circle_draw(self, screen):
        pass

    @abc.abstractmethod
    def rect_draw(self, screen):
        pass

    @abc.abstractmethod
    def line_draw(self, screen):
        pass


