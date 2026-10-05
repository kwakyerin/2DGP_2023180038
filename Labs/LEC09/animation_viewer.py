from pathlib import Path
from dataclasses import dataclass
import time

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    clear_canvas,
    close_canvas,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SPRITE_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
SPRITE_WIDTH = 399
SPRITE_HEIGHT = 525
FRAME_DURATION = 0.08
FRAME_SCALE = 5
REPEATS_PER_ANIMATION = 5
ANIMATION_GAP = 1.0


@dataclass(frozen=True)
class Animation:
    name: str
    top: int
    frame_width: int
    frame_height: int
    frame_stride: int
    frame_count: int


@dataclass
class PlaybackState:
    animation_index: int = 0
    frame_index: int = 0
    repetition_count: int = 0
    frame_elapsed: float = 0.0
    gap_elapsed: float = 0.0
    waiting_for_next: bool = False


ANIMATIONS = (
    Animation("동작 01", 36, 30, 44, 30, 10),
    Animation("동작 02", 77, 30, 42, 30, 13),
    Animation("동작 03", 120, 47, 44, 47, 6),
    Animation("동작 04", 165, 38, 42, 38, 8),
    Animation("동작 05", 204, 34, 32, 34, 6),
    Animation("동작 06", 236, 36, 39, 36, 6),
    Animation("동작 07", 281, 42, 38, 42, 6),
    Animation("동작 08", 325, 36, 46, 36, 8),
    Animation("동작 09", 376, 36, 42, 36, 8),
    Animation("동작 10", 424, 38, 44, 38, 4),
)


def advance_playback(state, delta_time):
    if state.waiting_for_next:
        state.gap_elapsed += delta_time
        if state.gap_elapsed >= ANIMATION_GAP:
            state.waiting_for_next = False
            state.animation_index = (state.animation_index + 1) % len(ANIMATIONS)
            state.frame_index = 0
            state.frame_elapsed = 0.0
        return

    state.frame_elapsed += delta_time
    animation = ANIMATIONS[state.animation_index]
    if state.frame_elapsed < FRAME_DURATION:
        return

    state.frame_elapsed %= FRAME_DURATION
    state.frame_index += 1
    if state.frame_index < animation.frame_count:
        return

    state.repetition_count += 1
    if state.repetition_count < REPEATS_PER_ANIMATION:
        state.frame_index = 0
        return

    state.repetition_count = 0
    state.waiting_for_next = True
    state.gap_elapsed = 0.0
    state.frame_index = animation.frame_count - 1


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        sprite_sheet = load_image(str(SPRITE_PATH))
        running = True
        state = PlaybackState()
        previous_time = time.monotonic()

        while running:
            current_time = time.monotonic()
            delta_time = current_time - previous_time
            previous_time = current_time
            advance_playback(state, delta_time)

            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False

            animation = ANIMATIONS[state.animation_index]
            frame_bottom = SPRITE_HEIGHT - animation.top - animation.frame_height
            clear_canvas()
            scale = min(
                FRAME_SCALE,
                WINDOW_WIDTH * 0.8 / animation.frame_width,
                WINDOW_HEIGHT * 0.8 / animation.frame_height,
            )
            sprite_sheet.clip_draw(
                state.frame_index * animation.frame_stride,
                frame_bottom,
                animation.frame_width,
                animation.frame_height,
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                round(animation.frame_width * scale),
                round(animation.frame_height * scale),
            )
            update_canvas()
    finally:
        close_canvas()


if __name__ == "__main__":
    main()