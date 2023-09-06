        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
                planets[-1].rotate_force(0.1)