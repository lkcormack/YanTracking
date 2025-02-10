# scraps


    # Show first word
    label.draw()
    word_stim.draw()
    win.flip()
    core.wait(2)  # Show for 2 seconds

    # Fade out first word
    for opacity in range(100, -1, -5):
        label.opacity = opacity/100
        word_stim.opacity = opacity/100
        label.draw()
        word_stim.draw()
        win.flip()
        core.wait(0.016)

    # Brief pause with blank screen
    win.flip()
    core.wait(0.3)

    # Reset opacity for second word
    label.opacity = 1.0
    word_stim.opacity = 1.0
