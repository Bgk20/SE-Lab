
"""
Hook: the player's fishing hook.

The player starts a cast manually.
The hook cannot be interrupted while casting or retracting.
"""

import pygame

IDLE = "idle"
CASTING = "casting"
RETRACTING = "retracting"


class Hook:
    def __init__(
        self,
        x,
        surface_y,
        max_depth_y,
        speed=4,
        width=14,
        height=14
    ):
        self.x = x
        self.surface_y = surface_y
        self.max_depth_y = max_depth_y
        self.y = surface_y
        self.speed = speed
        self.width = width
        self.height = height
        self.state = IDLE

    def start_cast(self):
        """Start casting only when the hook is idle."""
        if self.state != IDLE:
            return False

        self.y = self.surface_y
        self.state = CASTING
        return True

    def update(self):
        """Move the hook down and then back up."""
        if self.state == CASTING:
            self.y += self.speed

            if self.y >= self.max_depth_y:
                self.y = self.max_depth_y
                self.state = RETRACTING

        elif self.state == RETRACTING:
            self.y -= self.speed

            if self.y <= self.surface_y:
                self.y = self.surface_y
                self.state = IDLE

    def catch_fish(self):
        """Retract immediately after catching a fish."""
        if self.state == CASTING:
            self.state = RETRACTING

    def get_rect(self):
        """Return the hook's collision rectangle."""
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height
        )
