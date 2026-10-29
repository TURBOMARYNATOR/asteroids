import sys

import pygame

from asteroid import *
from asteroidfield import *
from constants import *
from logger import log_event, log_state
from player import Player
from shot import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0.0

    asteroid_score = 0
    font = pygame.font.Font(None, 32)
    text = font.render(f"Score: {asteroid_score}", True, "White")

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_SHOOT_COOLDOWN_SECONDS)

    asteroid_field = AsteroidField()

    while True:
        log_state()
        screen.fill("black")
        screen.blit(text, (640, 50))

        for d in drawable:
            d.draw(screen)

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for missle in shots:
                if asteroid.collides_with(missle):
                    log_event("asteroid_shot")
                    missle.kill()
                    asteroid.split()
                    asteroid_score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
