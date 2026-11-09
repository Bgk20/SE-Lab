
import pygame
from game.hook import Hook
from game.fish import Fish
from game.catch import check_catch

pygame.init()

hook = Hook(x=350, surface_y=80, max_depth_y=460)
hook.y = 200

# Case 1: Fish is far from the hook
fish_far = Fish(x=100, y=200, speed=0)
result_far = check_catch(hook, [fish_far])
assert result_far is None, "A distant fish should not be caught!"

# Case 2: Fish overlaps the hook
fish_near = Fish(x=350, y=200, speed=0)
result_near = check_catch(hook, [fish_near])
assert result_near is fish_near, "An overlapping fish should be caught!"

print("Task 1 tests passed!")

pygame.quit()
