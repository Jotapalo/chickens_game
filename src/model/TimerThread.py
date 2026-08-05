import threading
import time

class TimerThread(threading.Thread):
    def __init__(self, duration, callback, daemon: bool) -> None:
        super().__init__(daemon=daemon)
        self.duration = duration
        self.callback = callback
        self._pause_event = threading.Event()
        self._stop_event = threading.Event()
        self.remaining_time = duration

    def run(self) -> None:
        start_time = time.time()
        while self.remaining_time > 0:
            if self._stop_event.is_set():
                break
            if not self._pause_event.is_set():
                elapsed = time.time() - start_time
                self.remaining_time -= elapsed
                start_time = time.time()
                time.sleep(0.1)  # Pequeña pausa para reducir el consumo de CPU
            else:
                start_time = time.time()  # Resetear tiempo al pausar
        if self.remaining_time <= 0:
            self.callback()

    def pause(self) -> None:
        self._pause_event.set()

    def resume(self) -> None:
        self._pause_event.clear()

    def stop(self) -> None:
        self._stop_event.set()

    def extend(self, seconds: float) -> None:
        """Extiende el tiempo restante del temporizador.

        Si el power-up ya está activo y se recoge otro del mismo tipo,
        se suman los segundos al tiempo que quedaba en vez de reiniciarlo.
        """
        self.remaining_time += seconds
