import pygame
import random
import sys

pygame.init()  # Initialize pygame

# Get screen size and set up display
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Match Game")

# Colors
WHITE=(255,255,255)
GRAY=(200,200,200)
BLACK=(30,30,30)
RED=(220,70,70)
GREEN=(70,200,120)
BLUE=(70,120,220)
BG=(240,240,240)

# Fonts
font_size=min(WIDTH//4,HEIGHT//5)
font=pygame.font.SysFont(None,font_size)
small_font=pygame.font.SysFont(None,HEIGHT//25)

# Game board setup
ROWS,COLS=2,4
CARD_WIDTH=WIDTH//7
CARD_HEIGHT=HEIGHT//4
GAP=20

# Center the grid
START_X=(WIDTH-(COLS*CARD_WIDTH+(COLS-1)*GAP))//2
START_Y=(HEIGHT-(ROWS*CARD_HEIGHT+(ROWS-1)*GAP))//2

# Buttons
button_width=WIDTH//8
button_height=HEIGHT//15
exit_button=pygame.Rect(WIDTH-button_width-20,20,button_width,button_height)
restart_button=pygame.Rect(20,20,button_width,button_height)

clock=pygame.time.Clock()

# Reset game state
def reset_game():
    global values,revealed,selected,mismatch_time,card_colors,start_time,final_time,moves,win_ready,win_delay
    # Create pairs of values and shuffle
    values=list(range(1,(ROWS*COLS//2)+1))*2
    random.shuffle(values)
    revealed=[False]*(ROWS*COLS)  # Track revealed cards
    selected=[]                   # Currently selected cards
    mismatch_time=0               # Timer for wrong pairs
    card_colors=["hidden"]*(ROWS*COLS)
    start_time=pygame.time.get_ticks()
    final_time=None
    moves=0
    win_ready=False               # Flag for win screen
    win_delay=None                # Delay before showing win screen

reset_game()

running=True
while running:
    screen.fill(BG)

    # Timer
    if final_time is None:
        elapsed=(pygame.time.get_ticks()-start_time)//1000
    else:
        elapsed=final_time

    # Event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.MOUSEBUTTONDOWN:
            if exit_button.collidepoint(event.pos):
                running=False
            elif restart_button.collidepoint(event.pos):
                reset_game()
            elif not mismatch_time and final_time is None:
                x,y=event.pos
                # Check if click is inside grid
                if START_X<x<START_X+COLS*(CARD_WIDTH+GAP) and START_Y<y<START_Y+ROWS*(CARD_HEIGHT+GAP):
                    col=(x-START_X)//(CARD_WIDTH+GAP)
                    row=(y-START_Y)//(CARD_HEIGHT+GAP)
                    idx=row*COLS+col
                    # Select card if not already revealed
                    if idx<len(values) and not revealed[idx] and idx not in selected:
                        selected.append(idx)
                    # If two cards selected, check match
                    if len(selected)==2:
                        moves+=1
                        i1,i2=selected
                        if values[i1]==values[i2]:
                            revealed[i1]=revealed[i2]=True
                            card_colors[i1]=card_colors[i2]="match"
                            selected=[]
                            # If all revealed, trigger win
                            if all(revealed):
                                win_ready=True
                                win_delay=pygame.time.get_ticks()
                        else:
                            card_colors[i1]=card_colors[i2]="wrong"
                            mismatch_time=pygame.time.get_ticks()

    # Reset wrong pair after short delay
    if mismatch_time and pygame.time.get_ticks()-mismatch_time>800:
        for i in selected:
            card_colors[i]="hidden"
        selected=[]
        mismatch_time=0

    # Escape key exits
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running=False

    # Draw cards
    for i in range(len(values)):
        row=i//COLS
        col=i%COLS
        rect=pygame.Rect(
            START_X+col*(CARD_WIDTH+GAP),
            START_Y+row*(CARD_HEIGHT+GAP),
            CARD_WIDTH,
            CARD_HEIGHT
        )
        # Card colors based on state
        if card_colors[i]=="match":
            color=GREEN
        elif card_colors[i]=="wrong":
            color=RED
        elif i in selected:
            color=GRAY
        else:
            color=BLACK
        pygame.draw.rect(screen,color,rect,border_radius=18)
        pygame.draw.rect(screen,WHITE,rect,3,border_radius=18)
        # Show value if revealed or selected
        if revealed[i] or i in selected:
            text=font.render(str(values[i]),True,WHITE)
            screen.blit(text,text.get_rect(center=rect.center))

    # Timer + moves display
    minutes=elapsed//60
    seconds=elapsed%60
    timer_text=small_font.render(f"Time: {minutes:02}:{seconds:02}",True,BLACK)
    screen.blit(timer_text,(WIDTH//2-60,20))
    move_text=small_font.render(f"Moves: {moves}",True,BLACK)
    screen.blit(move_text,(WIDTH//2-60,50))

    # Win screen with 200ms delay
    if win_ready and pygame.time.get_ticks() - win_delay > 200:
        if final_time is None:
            final_time=elapsed

        # Overlay background
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BG)
        screen.blit(overlay, (0, 0))

        # Win text
        win_text=font.render("YOU WIN!",True,GREEN)
        screen.blit(win_text,win_text.get_rect(center=(WIDTH//2,HEIGHT//2)))
        score_text=small_font.render(f"Completed in {moves} moves",True,BLACK)
        screen.blit(score_text,score_text.get_rect(center=(WIDTH//2,HEIGHT//2+120)))

        # Redraw buttons on top
        pygame.draw.rect(screen,RED,exit_button,border_radius=10)
        screen.blit(small_font.render("Exit",True,WHITE),
                    small_font.render("Exit",True,WHITE).get_rect(center=exit_button.center))
        pygame.draw.rect(screen,BLUE,restart_button,border_radius=10)
        screen.blit(small_font.render("Restart",True,WHITE),
                    small_font.render("Restart",True,WHITE).get_rect(center=restart_button.center))
    else:
        # Normal buttons during gameplay
        pygame.draw.rect(screen,RED,exit_button,border_radius=10)
        screen.blit(small_font.render("Exit",True,WHITE),
                    small_font.render("Exit",True,WHITE).get_rect(center=exit_button.center))
        pygame.draw.rect(screen,BLUE,restart_button,border_radius=10)
        screen.blit(small_font.render("Restart",True,WHITE),
                    small_font.render("Restart",True,WHITE).get_rect(center=restart_button.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
