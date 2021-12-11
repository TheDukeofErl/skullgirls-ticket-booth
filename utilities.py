import os
import platform

from pathlib import Path

class ReplayDirManager(object):
    def __init__(self):
        self.path_valid = False
        self.replay_path = None
        self.replay_path_str = "NO_PATH"
        
    def path_detection(self):
        os_platform = platform.system()
        print("Detected platform as: " + os_platform)
        if os_platform == "Linux":
            self.replay_path = Path.home().joinpath('.local','share','Skullgirls','Replays')
        else:
            return self.path_valid

        dir_list = os.listdir(self.replay_path)
        if len(dir_list) == 1:
            self.replay_path = self.replay_path.joinpath(dir_list[0])
            self.replay_path_str = str(self.replay_path)
            self.path_valid = True
            print("Path detected as " + self.replay_path_str)
        else:
            self.path_valid = False
            self.replay_path = None
            self.replay_path_str = "TOO_MANY_DIRS"

        return self.path_valid

    def set_path(self, new_path):
        self.replay_path = Path(new_path)
        print("New path: " + new_path)
        if self.replay_path.exists() and self.replay_path.is_dir():
            self.replay_path_str = str(self.replay_path)
            self.path_valid = True
        else:
            self.path_valid = False
            self.replay_path = None
            self.replay_path_str = "NO_PATH"

        return self.path_valid

    def list_replays(self):
        print("Getting replays from : " + self.replay_path_str)
        if self.path_valid:
            replays = sorted(self.replay_path.iterdir())
            replays = [each.stem for each in replays]
            replays = list(dict.fromkeys(replays))
            return replays
