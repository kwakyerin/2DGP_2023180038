from pathlib import Path

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


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sprite_sheet = load_image(str(SPRITE_PATH))
    running = True

    while running:
        for event in get_events():
            if event.type == SDL_QUIT or (
                event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
            ):
                running = False

        clear_canvas()
        sprite_sheet.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        update_canvas()

    close_canvas()


if __name__ == "__main__":
    main()