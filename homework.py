class InfoMessage:
    """(RU) Информационное сообщение о тренировке.
       (EN) Informational message about the training."""

    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type: str = training_type
        self.duration: int = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """(RU) Базовый класс тренировки."""

    M_IN_KM: float = 1000.0
    LEN_STEP: float = 0.65
    VMIN: int = 60

    def __init__(self, action, duration, weight):
        self.action: int = action
        self.duration: int = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """(RU) Получить дистанцию в км.
           (EN) Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """(RU) Получить среднюю скорость движения.
           (EN) Get the average speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """(RU) Получить количество затраченных калорий.
           (EN) Get the number of calories consumed."""
        pass

    def show_training_info(self):
        """(RU) Вернуть информационное сообщение о выполненной тренировке.
           (EN) Return an informational message about the completed workout."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """(RU)Тренировка: бег.
       (EN) Training: running."""
    CONS_CAL1 = 18
    CONS_CAL2 = 20

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CONS_CAL1 * self.get_mean_speed() - self.CONS_CAL2)
                * self.weight / self.M_IN_KM * (self.duration * self.VMIN))


class SportsWalking(Training):
    """(RU) Тренировка: спортивная ходьба.
       (EN) Training: sports walking."""
    CAL3 = 0.035
    CAL4 = 0.029

    def __init__(self, action: int, duration: int, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CAL3 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.CAL4 * self.weight) * (self.duration * self.VMIN))


class Swimming(Training):
    """(RU) Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        const_k = 1.1
        return (self.get_mean_speed() + const_k) * 2 * (self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """(RU) Прочитать данные полученные от датчиков.
       (EN) Read the data received from the sensors."""
    read1: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    return read1[workout_type](*data)


def main(training: Training) -> str:
    """(RU) Главная функция.
       (EN) The main function."""
    info = InfoMessage.get_message(training.show_training_info())
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        if training is None:
            print('Неожиданный тип тренировки')
        else:
            main(training)