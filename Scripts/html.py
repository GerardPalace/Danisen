import sys
import io

c = ["fox", "falco", "marth", "sheik", "jigglypuff", "peach", "ice_climbers", "falcon", "pikachu", "samus", "dr_mario", "yoshi", "luigi", "ganondorf", "mario", "young_link", "donkey_kong", "link", "mr_game_and_watch", "roy", "mewtwo", "zelda", "ness", "bowser", "pichu", "kirby"]
for v in c:
    open("../" + v + ".html", "w", encoding='utf-8')
