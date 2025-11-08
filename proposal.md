# Flames of the Lost

## Repository
[https://github.com/M-Knutson/Flames-of-the-Lost]

## Description
Flames of the Lost is a simple platformer game. It's relevant to PFDA as it's an interactive form of media using Python. 

## Features
- As a platforming game, Flames of the Lost will feature a playable character.
	-  I will create a player class to store the character information and methods and then use a pygame surface to actually display the character.
- The character will be able to move around the level based on user input.
	- Player movement will be implemented through the pygame.key.get_pressed() method and function. 
- The character will be governed by "gravity" and will able to land on platforms.
	- To create pseudogravity, the character will have a constant y_velocity acting upon it. Using one of pygame's several .collide methods, the character's y_velocity will be set to 0 when in contact with a platform. 
- There will be an end goal/finish line that triggers a "Thanks for playing" message.
    - I should be able to use a collision detection method and an if statement to simulate a game end message. 

## Challenges
- I'll need to do more research into how to create "gravity" and govern character movement.
- I need to learn how to create a death state which restarts the level if the character falls off the map.
- I have to research how to create an end messge screen and how to trigger it. 
- I'll need to learn how to import images and animations into my program as I, ideally, want to create custom art for it. 

## Outcomes
Ideal Outcome:
- Ideally, Flames of the Lost will be a playable game with a challenging but fun level design. I hope for the game to have visuals and possibly even background music. The player movement should feel smooth and intuitive. The player should be able to fall and die which should restart the level, and there should be an end screen to signify the end of the game. 

Minimal Viable Outcome:
- Minimally, Flames of the Lost should still be interactive with player movement and a very simple level design. The game should restart in case of the player falling off of the platforms.

## Milestones

- Week 1
  1. Create base game init, loop, and quit
  2. Create character class
  3. Simple character movment

- Week 2
  1. Create platform class and design level
  2. Implement "gravity" and character interactions with platforms
  3. Game restart upon death

- Week N (Final)
  1. End screen/goal
  2. Import visuals/music (if I've had time to create custom visuals)