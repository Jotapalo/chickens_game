import pygame as py
from src.model.Enum import Enum


class SoundService:
    """Servicio centralizado de audio (música y efectos de sonido).

    Se accede a sus métodos directamente desde la clase (métodos de clase),
    sin necesidad de instanciarlo ni de pasar una instancia como argumento.

    Uso:
        SoundService.play_music_background()
        SoundService.play_shoot_sound()
        SoundService.play_power_up_sound()
    """

    # Los efectos se cargan de forma perezosa (lazy) la primera vez que se
    # usan, para no requerir que pygame.mixer esté inicializado en el momento
    # del import del módulo.
    _shoot_sound = None
    _power_up_sound = None
    _boom_sound = None
    _music_loaded = False

    @classmethod
    def _init_mixer(cls) -> None:
        """Asegura que pygame.mixer esté inicializado antes de cargar audio."""
        if not py.mixer.get_init():
            py.mixer.init()

    @classmethod
    def _load_shoot(cls):
        """Carga (una sola vez) el sonido de disparo."""
        if cls._shoot_sound is None:
            cls._init_mixer()
            cls._shoot_sound = py.mixer.Sound(Enum.resourcePath.SHOOT_SOUND)
            cls._shoot_sound.set_volume(0.4)
        return cls._shoot_sound

    @classmethod
    def _load_power_up(cls):
        """Carga (una sola vez) el sonido de power-up."""
        if cls._power_up_sound is None:
            cls._init_mixer()
            cls._power_up_sound = py.mixer.Sound(Enum.resourcePath.POWER_UP_SOUND)
            cls._power_up_sound.set_volume(0.6)
        return cls._power_up_sound

    @classmethod
    def _load_boom(cls):
        """Carga (una sola vez) el sonido de boom."""
        if cls._boom_sound is None:
            cls._init_mixer()
            cls._boom_sound = py.mixer.Sound(Enum.resourcePath.BOOM_SOUND)
            cls._boom_sound.set_volume(0.45)
        return cls._boom_sound

    @classmethod
    def play_boom_sound(cls):
        """Reproduce el sonido boom cuando se elimina un enemigo"""
        cls._load_boom().play(0)

    @classmethod
    def play_shoot_sound(cls) -> None:
        """Reproduce el sonido de disparo (efecto corto, se puede solapar)."""
        cls._load_shoot().play(0)

    @classmethod
    def play_power_up_sound(cls) -> None:
        """Reproduce el sonido de recoger un power-up."""
        cls._load_power_up().play(0)

    @classmethod
    def play_music_background(cls) -> None:
        """Reproduce la música de fondo en bucle infinito (.mp3 vía mixer.music)."""
        cls._init_mixer()
        if not cls._music_loaded:
            py.mixer.music.load(Enum.resourcePath.LEVEL_BACKGROUND_SOUND)
            py.mixer.music.set_volume(0.3)
            cls._music_loaded = True
        py.mixer.music.play(-1)

    @classmethod
    def stop_music_background(cls) -> None:
        """Detiene la música de fondo."""
        py.mixer.music.stop()

    @classmethod
    def pause_music_background(cls) -> None:
        """Pausa la música de fondo."""
        py.mixer.music.pause()

    @classmethod
    def resume_music_background(cls) -> None:
        """Reanuda la música de fondo pausada."""
        py.mixer.music.unpause()

