import pygame, os
from bullet import Bullet
pygame.init()


max_acceleration_in_seconds = 0.5
GRAVITY = 0.5
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x_pos, y_pos, scale, speed):
        super().__init__()

        self.is_alive = True
        self.is_airborne = True

        self.char_type = char_type
        self.speed = speed
        self.current_speed = 0
        self.accel_step = self.speed / (60 * max_acceleration_in_seconds)



        self.flip = False
        self.direction = 1

        self.velocity_y = 0
        self.jump = False

        self.moving_right = False
        self.moving_left = False
        self.shoot = False


        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

      
        #load all images for the players
        animation_types = ["Idle", "Run", "Jump", "Death"]

        for animation in animation_types:
            #reset
            temp = []

            # count number of files in a folder
            num_of_frames = len(os.listdir(f"./assets/img/{char_type}/{animation}/"))

            for i in range(num_of_frames):
                original_img = pygame.image.load(
                    f"./assets/img/{self.char_type}/{animation}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    original_img,
                    (
                        original_img.get_width() * scale,
                        original_img.get_height() * scale,
                    )
                )
                temp.append(img)
            self.animation_list.append(temp)
            


        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x_pos, y_pos))



    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        # ✅ CORRECT: action + frame
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def move(self):
        target_speed = 0
        dx = 0
        dy = 0

        if self.moving_right:
            target_speed = self.speed
            self.flip = False
            self.direction = 1

        if self.moving_left:
            target_speed = -self.speed
            self.flip = True
            self.direction = -1

        if self.jump and not self.is_airborne:
            self.velocity_y = -10
            self.jump = False
            self.is_airborne = True

        if self.current_speed < target_speed:
            self.current_speed += self.accel_step
            if self.current_speed > target_speed:
                self.current_speed = target_speed
        elif self.current_speed > target_speed:
            self.current_speed -= self.accel_step
            if self.current_speed < target_speed:
                self.current_speed = target_speed

        #apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y = 10

        dx = self.current_speed
        dy += self.velocity_y

        #check collision with a fake floor

        if self.rect.bottom + dy > 500:
            dy = 500 - self.rect.bottom
            self.is_airborne = False

        self.rect.x += int(dx)
        self.rect.y += int(dy)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def shoot_a_bullet(self, screen_width):
        bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction), self.rect.centery, self.direction, screen_width)
            
        self.shoot = False
        return bullet
