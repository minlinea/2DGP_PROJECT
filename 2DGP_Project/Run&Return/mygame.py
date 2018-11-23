import game_framework
import pico2d
import start_state
import stage_run
import stage_return
import stage_editor
import title_state
import pause_state

pico2d.open_canvas()
game_framework.run(title_state)
pico2d.close_canvas()