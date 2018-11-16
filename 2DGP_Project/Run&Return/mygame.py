import game_framework
import pico2d
import start_state
import stage_run
import stage_return
import stage_editor
import title_state
# fill here

pico2d.open_canvas()
game_framework.run(stage_return)
pico2d.close_canvas()