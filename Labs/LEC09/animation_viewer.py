from dataclasses import dataclass
from pathlib import Path
import time
from typing import Tuple

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
class SpriteFrame:
	left: int
	top: int
	width: int
	height: int


@dataclass(frozen=True)
class Animation:
	name: str
	frames: Tuple[SpriteFrame, ...]
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
	Animation("달리기 01", (
		SpriteFrame(1, 39, 29, 39),
		SpriteFrame(31, 40, 26, 38),
		SpriteFrame(58, 39, 28, 39),
		SpriteFrame(86, 40, 30, 38),
		SpriteFrame(118, 40, 30, 38),
		SpriteFrame(150, 40, 30, 38),
		SpriteFrame(182, 40, 29, 38),
		SpriteFrame(211, 39, 29, 38),
		SpriteFrame(240, 39, 29, 38),
		SpriteFrame(270, 45, 24, 32),
		SpriteFrame(302, 51, 29, 26),
	), 180.0),
	Animation("달리기 02", (
		SpriteFrame(8, 80, 26, 37),
		SpriteFrame(37, 80, 27, 37),
		SpriteFrame(65, 80, 31, 38),
		SpriteFrame(97, 80, 37, 37),
		SpriteFrame(135, 80, 32, 35),
		SpriteFrame(170, 79, 32, 38),
		SpriteFrame(206, 79, 26, 38),
		SpriteFrame(238, 80, 24, 37),
		SpriteFrame(263, 80, 30, 37),
		SpriteFrame(295, 80, 36, 37),
		SpriteFrame(334, 80, 32, 36),
		SpriteFrame(370, 79, 29, 38),
	), 220.0),
	Animation("전진 동작", (
		SpriteFrame(1, 124, 33, 40),
		SpriteFrame(39, 124, 35, 39),
		SpriteFrame(89, 125, 35, 38),
		SpriteFrame(130, 122, 34, 41),
		SpriteFrame(181, 122, 34, 41),
		SpriteFrame(228, 122, 33, 40),
	), 140.0),
	Animation("동작 04", (
		SpriteFrame(1, 169, 29, 30),
		SpriteFrame(35, 168, 29, 30),
		SpriteFrame(67, 169, 30, 29),
		SpriteFrame(98, 169, 31, 29),
		SpriteFrame(131, 168, 29, 30),
		SpriteFrame(162, 168, 29, 31),
		SpriteFrame(193, 170, 30, 29),
		SpriteFrame(230, 170, 31, 29),
		SpriteFrame(268, 170, 30, 30),
	)),
	Animation("동작 05", (
		SpriteFrame(1, 206, 30, 27),
		SpriteFrame(36, 206, 29, 27),
		SpriteFrame(70, 206, 29, 27),
		SpriteFrame(105, 206, 29, 27),
		SpriteFrame(139, 206, 29, 27),
		SpriteFrame(174, 206, 29, 27),
	)),
	Animation("동작 06", (
		SpriteFrame(1, 239, 29, 35),
		SpriteFrame(36, 239, 30, 35),
		SpriteFrame(74, 239, 31, 35),
		SpriteFrame(111, 238, 31, 36),
		SpriteFrame(149, 239, 30, 35),
		SpriteFrame(186, 238, 31, 36),
	)),
	Animation("동작 07", (
		SpriteFrame(1, 283, 29, 35),
		SpriteFrame(36, 283, 30, 35),
		SpriteFrame(72, 286, 39, 31),
		SpriteFrame(123, 285, 39, 32),
		SpriteFrame(172, 286, 39, 31),
		SpriteFrame(218, 285, 38, 32),
	)),
	Animation("동작 08", (
		SpriteFrame(1, 327, 24, 44),
		SpriteFrame(31, 327, 29, 44),
		SpriteFrame(65, 327, 20, 44),
		SpriteFrame(90, 327, 25, 43),
		SpriteFrame(119, 327, 25, 43),
		SpriteFrame(149, 327, 20, 44),
		SpriteFrame(184, 341, 40, 28),
		SpriteFrame(232, 341, 39, 27),
	)),
	Animation("동작 09", (
		SpriteFrame(1, 379, 27, 38),
		SpriteFrame(31, 379, 31, 36),
		SpriteFrame(64, 379, 31, 36),
		SpriteFrame(99, 378, 33, 37),
		SpriteFrame(136, 379, 32, 36),
		SpriteFrame(176, 379, 33, 36),
		SpriteFrame(217, 379, 33, 36),
		SpriteFrame(254, 378, 33, 36),
	)),
	Animation("동작 10", (
		SpriteFrame(6, 429, 34, 40),
		SpriteFrame(49, 427, 34, 42),
		SpriteFrame(96, 427, 23, 39),
		SpriteFrame(125, 427, 23, 39),
	)),
)


def frame_scale(animation: Animation) -> float:
	frame_width = max(frame.width for frame in animation.frames)
	frame_height = max(frame.height for frame in animation.frames)
	return min(
		FRAME_SCALE,
		WINDOW_WIDTH * 0.8 / frame_width,
		WINDOW_HEIGHT * 0.8 / frame_height,
	)


def advance_position(
	state: PlaybackState,
	animation: Animation,
	delta_time: float,
) -> None:
	if animation.movement_speed == 0 or delta_time <= 0:
		return

	frame_width = max(frame.width for frame in animation.frames)
	half_width = frame_width * frame_scale(animation) / 2
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
		if state.frame_index < len(animation.frames):
			continue

		state.repetition_count += 1
		if state.repetition_count < REPEATS_PER_ANIMATION:
			state.frame_index = 0
			continue

		state.repetition_count = 0
		state.waiting_for_next = True
		state.gap_elapsed = 0.0
		state.frame_index = len(animation.frames) - 1
		return


def draw_animation_frame(
	sprite_sheet,
	animation: Animation,
	frame_index: int,
	position_x: float,
	direction: int,
) -> None:
	frame = animation.frames[frame_index]
	frame_bottom = sprite_sheet.h - frame.top - frame.height
	scale = frame_scale(animation)
	sprite_sheet.clip_composite_draw(
		frame.left,
		frame_bottom,
		frame.width,
		frame.height,
		0,
		"h" if animation.movement_speed and direction < 0 else "",
		position_x,
		WINDOW_HEIGHT // 2,
		round(frame.width * scale),
		round(frame.height * scale),
	)


def validate_animations(
	animations=ANIMATIONS,
	sheet_width=399,
	sheet_height=525,
) -> None:
	for animation in animations:
		if not animation.frames:
			raise ValueError(f"프레임이 없는 애니메이션: {animation.name}")
		for frame in animation.frames:
			if (
				frame.left < 0
				or frame.top < 0
				or frame.width < 1
				or frame.height < 1
				or frame.left + frame.width > sheet_width
				or frame.top + frame.height > sheet_height
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
