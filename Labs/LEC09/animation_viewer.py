from dataclasses import dataclass
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
	movement_speed: float = 0.0


@dataclass
class PlaybackState:
	animation_index: int = 0
	frame_index: int = 0
	repetition_count: int = 0
	frame_elapsed: float = 0.0
	gap_elapsed: float = 0.0
	waiting_for_next: bool = False
	position_x: float = WINDOW_WIDTH / 2
	direction: int = 1


ANIMATIONS = (
	Animation("달리기 01", 36, 30, 44, 30, 10, 180.0),
	Animation("달리기 02", 77, 30, 42, 30, 13, 220.0),
	Animation("전진 동작", 120, 47, 44, 47, 6, 140.0),
	Animation("동작 04", 165, 38, 42, 38, 8),
	Animation("동작 05", 204, 34, 32, 34, 6),
	Animation("동작 06", 236, 36, 39, 36, 6),
	Animation("동작 07", 281, 42, 38, 42, 6),
	Animation("동작 08", 325, 36, 46, 36, 8),
	Animation("동작 09", 376, 36, 42, 36, 8),
	Animation("동작 10", 424, 38, 44, 38, 4),
)


def frame_scale(animation: Animation) -> float:
	return min(
		FRAME_SCALE,
		WINDOW_WIDTH * 0.8 / animation.frame_width,
		WINDOW_HEIGHT * 0.8 / animation.frame_height,
	)


def advance_position(
	state: PlaybackState,
	animation: Animation,
	delta_time: float,
) -> None:
	if animation.movement_speed == 0 or delta_time <= 0:
		return

	half_width = animation.frame_width * frame_scale(animation) / 2
	left_edge = half_width
	right_edge = WINDOW_WIDTH - half_width
	next_position = (
		state.position_x
		+ animation.movement_speed * state.direction * delta_time
	)

	if next_position >= right_edge:
		state.position_x = right_edge
		state.direction = -1
	elif next_position <= left_edge:
		state.position_x = left_edge
		state.direction = 1
	else:
		state.position_x = next_position


def advance_playback(state: PlaybackState, delta_time: float) -> None:
	if state.waiting_for_next:
		state.gap_elapsed += delta_time
		if state.gap_elapsed >= ANIMATION_GAP:
			state.waiting_for_next = False
			state.animation_index = (state.animation_index + 1) % len(ANIMATIONS)
			state.frame_index = 0
			state.frame_elapsed = 0.0
		return

	animation = ANIMATIONS[state.animation_index]
	advance_position(state, animation, delta_time)
	state.frame_elapsed += delta_time

	while state.frame_elapsed + 1e-9 >= FRAME_DURATION:
		state.frame_elapsed = max(0.0, state.frame_elapsed - FRAME_DURATION)
		state.frame_index += 1
		if state.frame_index < animation.frame_count:
			continue

		state.repetition_count += 1
		if state.repetition_count < REPEATS_PER_ANIMATION:
			state.frame_index = 0
			continue

		state.repetition_count = 0
		state.waiting_for_next = True
		state.gap_elapsed = 0.0
		state.frame_index = animation.frame_count - 1
		return


def draw_animation_frame(
	sprite_sheet,
	animation: Animation,
	frame_index: int,
	position_x: float,
	direction: int,
) -> None:
	frame_bottom = sprite_sheet.h - animation.top - animation.frame_height
	scale = frame_scale(animation)
	sprite_sheet.clip_composite_draw(
		frame_index * animation.frame_stride,
		frame_bottom,
		animation.frame_width,
		animation.frame_height,
		0,
		"h" if animation.movement_speed and direction < 0 else "",
		position_x,
		WINDOW_HEIGHT // 2,
		round(animation.frame_width * scale),
		round(animation.frame_height * scale),
	)


def validate_animations(
	animations=ANIMATIONS,
	sheet_width=399,
	sheet_height=525,
) -> None:
	for animation in animations:
		last_frame_right = (
			(animation.frame_count - 1) * animation.frame_stride
			+ animation.frame_width
		)
		if (
			animation.frame_count < 1
			or animation.frame_width < 1
			or animation.frame_height < 1
			or animation.frame_stride < animation.frame_width
			or animation.top < 0
			or last_frame_right > sheet_width
			or animation.top + animation.frame_height > sheet_height
		):
			raise ValueError(f"잘못된 스프라이트 프레임 설정: {animation.name}")


def main() -> None:
	if not SPRITE_PATH.is_file():
		raise FileNotFoundError(f"스프라이트 파일을 찾을 수 없습니다: {SPRITE_PATH}")

	open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
	try:
		sprite_sheet = load_image(str(SPRITE_PATH))
		validate_animations(sheet_width=sprite_sheet.w, sheet_height=sprite_sheet.h)
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

			if not running:
				break

			animation = ANIMATIONS[state.animation_index]
			clear_canvas()
			draw_animation_frame(
				sprite_sheet,
				animation,
				state.frame_index,
				state.position_x,
				state.direction,
			)
			update_canvas()
			time.sleep(0.001)
	finally:
		close_canvas()


if __name__ == "__main__":
	main()
