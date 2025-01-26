import math
from datetime import datetime


class RequestController:
    def __init__(self, rate_limit: int | float) -> None:
        self.request_per_cycle, self.cycle_seconds = self._rate_normalizer(rate_limit)
        self._last_request_time = None
        self._request_counter = 0

    @staticmethod
    def _rate_normalizer(rate_limit: int | float) -> tuple[int, int]:
        cycle_seconds = 1

        if rate_limit < 1:
            while rate_limit < 1:
                rate_limit *= 10
                cycle_seconds *= 10
            rate_limit = int(rate_limit)
        else:
            rate_limit = int(rate_limit)

        return rate_limit, cycle_seconds

    def reset_counter(self) -> None:
        self._request_counter = 0

    def increment_counter(self) -> None:
        self._last_request_time = datetime.now()
        self._request_counter += 1

    def get_suspend_time(self) -> int:
        if not self.is_locked or self.is_new_cycle:
            return 0

        if (seconds_since_last_request := self.seconds_since_last_request) > self.cycle_seconds:
            return 0

        return math.ceil(self.cycle_seconds - seconds_since_last_request)

    def request_is_allowed(self) -> bool:
        if self.is_locked:
            return False

        self.increment_counter()
        return True

    @property
    def is_locked(self) -> bool:
        if self.is_new_cycle:
            self.reset_counter()
            return False

        return self._request_counter >= self.request_per_cycle

    @property
    def is_new_cycle(self) -> bool:
        if self._last_request_time is None:
            return True

        if self.seconds_since_last_request > self.cycle_seconds:
            return True

        return False

    @property
    def seconds_since_last_request(self) -> int | float:
        if self._last_request_time is None:
            return self.cycle_seconds

        return (datetime.now() - self._last_request_time).total_seconds()

    def __str__(self) -> str:
        return f"{self.request_per_cycle} requests in {self.cycle_seconds} seconds"

    def __repr__(self) -> str:
        return f"RequestController(request_per_cycle={self.request_per_cycle}, cycle_seconds={self.cycle_seconds})"
