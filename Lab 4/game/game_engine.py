
"""
GameEngine: manages fishing gameplay.

Task 1: Correct catch detection.
Task 2: Multiple fish types, speeds, and points.
Task 3: Player-controlled casting.
Task 4: 30-second timer, final score, and restart.
"""

import pygame

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game.renderer import (
    WIDTH,
    SURFACE_Y,
    MAX_DEPTH_Y,
    draw_scene,
    draw_text,
    draw_banner,
)


class GameEngine:
    ROUND_DURATION = 30

    def __init__(self):
        self.reset()

    def reset(self):
        """Initialize or restart a round."""
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5
        )

        self.fish_list = [
            Fish(
                x=100, y=180, speed=2,
                width=30, height=16,
                point_value=10, color=(80, 180, 220)
            ),
            Fish(
                x=400, y=280, speed=-3,
                width=42, height=22,
                point_value=20, color=(255, 140, 50)
            ),
            Fish(
                x=250, y=380, speed=4,
                width=54, height=28,
                point_value=50, color=(255, 215, 0)
            ),
        ]

        self.hooked_fish = None
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.ROUND_DURATION
        self.game_over = False

    def start_cast(self):
        """Start a cast only while the round is active."""
        if not self.game_over:
            self.hook.start_cast()

    def update(self):
        """Update gameplay and enforce the time limit."""
        if self.game_over:
            return

        elapsed_seconds = (
            pygame.time.get_ticks() - self.start_time
        ) / 1000

        self.time_left = max(
            0,
            self.ROUND_DURATION - int(elapsed_seconds)
        )

        if elapsed_seconds >= self.ROUND_DURATION:
            self.time_left = 0
            self.game_over = True

            # Freeze the hook and end any unfinished catch.
            self.hooked_fish = None
            self.hook.state = IDLE
            self.hook.y = self.hook.surface_y
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None

        elif self.hook.state != IDLE:
            caught = check_catch(self.hook, self.fish_list)

            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        """Draw the game and its status."""
        draw_list = list(self.fish_list)

        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        draw_scene(surface, self.hook, draw_list)

        draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )
        draw_text(
            surface, font, f"Time: {self.time_left}s", (10, 40)
        )

        if self.game_over:
            draw_banner(
                surface, font,
                f"TIME UP! Final Score: {self.score}"
            )
            draw_text(
                surface, font, "Press R to Restart",
                (WIDTH // 2 - 110, surface.get_height() // 2 + 35),
                (255, 255, 255)
            )
