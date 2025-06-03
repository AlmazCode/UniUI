class Event:
    def __init__(self, listeners: list = None):
        self._listeners = [] if listeners is None else listeners

    def add_listener(self, callback):
        if callback not in self._listeners:
            self._listeners.append(callback)

    def remove_listener(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def invoke(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)