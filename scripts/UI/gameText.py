def render_text(game, text, font, position, color=(255, 255, 255)):
    start_text = font.render(text, True, color)
    start_text_rect = start_text.get_rect(center=position)
    game.screen.blit(start_text, start_text_rect)