if userInput[pygame.K_UP] and not self.dino_jump:
            self.ACCELARATION = ((
                (game_speed**2) * (self.JUMP_DISTANCE**2))/2/self.JUMP_HEIGHT)**(1/3)
            self.y_vel = game_speed * self.JUMP_DISTANCE/self.ACCELARATION
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not(self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False