# import pygame

# class InputSystem():
#     def __init__(self):
#         self.events = []
#         self.pressed_keys = []
#         self.actions = {
#             'move_left': False,
#             'move_right': False,
#             'jump': False,
#             'attack': False,
#             'dash': False,
#             'skip': False,
#             'pull_skill': False,
#         }
    
#     def get_actions(self):
#         yield self.actions

#     def update_actions(self, events):
#         self.events = events
#         for event in self.events:
#             if event.type == pygame.KEYDOWN:
#                 # left_move
#                 if event.key == pygame.K_a or event.key == pygame.K_LEFT:
#                     self.actions['move_left'] = True
#                 else:
#                     self.actions['move_left'] = False
#                 # right_move
#                 if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
#                     self.actions['move_right'] = True
#                 else:
#                     self.actions['move_right'] = False
#                 # jump
#                 if event.key == pygame.K_SPACE:
#                     self.actions['jump'] = True
#                 else:
#                     self.actions['jump'] = False
#                 # attack
#                 if event.key == pygame.K_j or event.key == pygame.MOUSEBUTTONDOWN:
#                     self.actions['attack'] = True
#                 else:
#                     self.actions['attack'] = False
#                 # dash
#                 if event.key == pygame.K_k or event.key == pygame.K_LSHIFT or event.key == pygame.K_LCTRL:
#                     self.actions['dash'] = True
#                 else:
#                     self.actions['dash'] = False
#                 # skip
#                 if event.key == pygame.K_p:
#                     self.actions['skip'] = True
#                 else:
#                     self.actions['skip'] = False
#                 # pull_skill
#                 if event.key == pygame.K_q:
#                     self.actions['pull_skill'] = True
#                 else:
#                     self.actions['pull_skill'] = False