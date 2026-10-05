from pathlib import Path
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
FRAME_WIDTH = 30
FRAME_DURATION = 0.08
FRAME_SCALE = 5
ANIMATION_ROWS = ((36, 44, 10),)


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_sheet = load_image(str(SPRITE_PATH))
    running = True
    frame_index = 0
    frame_elapsed = 0.0
    previous_time = time.monotonic()

    while running:
        current_time = time.monotonic()
        frame_elapsed += current_time - previous_time
        previous_time = current_time

        for event in get_events():
            if event.type == SDL_QUIT or (
                event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
            ):
                running = False

        if frame_elapsed >= FRAME_DURATION:
            frame_index = (frame_index + 1) % ANIMATION_ROWS[0][2]
            frame_elapsed %= FRAME_DURATION

        row_top, frame_height, _ = ANIMATION_ROWS[0]
        frame_bottom = SPRITE_HEIGHT - row_top - frame_height
        clear_canvas()
        sprite_sheet.clip_draw(
            frame_index * FRAME_WIDTH,
            frame_bottom,
            FRAME_WIDTH,
            frame_height,
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            FRAME_WIDTH * FRAME_SCALE,
            frame_height * FRAME_SCALE,
        )
        update_canvas()

    close_canvas()


if __name__ == "__main__":
    main()