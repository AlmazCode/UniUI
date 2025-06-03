class Time:

    Instance = None

    def __init__(self) -> None:

        if Time.Instance is None:
            Time.Instance = self
        else:
            raise Exception("Time: the time object has already been created")

        self.__delta_time: float = None
    
    @property
    def delta_time(self) -> float:
        return self.__delta_time
    
    @staticmethod
    def _update_delta_time(value: float) -> None:
        Time.Instance.__delta_time = value