from pathlib import Path


def format_replay(replay_json):
    import json
    return json.dumps(replay_json, indent=4)


def print_replay(replay_json):
    import json
    print(format_replay(replay_json))


class ReplayReader(object):
    def __init__(self, path=None):
        self._replay_path = path

    def set_path_from_string(self, path_str):
        self.set_path(Path(path_str))

    def set_path(self, path):
        self._replay_path = path

    def read_replay(self, replay_name):
        print("processing " + replay_name + ".ini")
        process_fighter = False
        player_one_name = ""
        player_two_name = ""
        raw_replay = self._replay_path.joinpath(replay_name + ".ini")
        raw_replay.open('r')

        # need to find the player names first... will have to revisit this later to find a better way
        for row in raw_replay.read_text().splitlines():
            key, value = row.split(' ', maxsplit=1)
            if key == "P1Name":
                player_one_name = value
            elif key == "P2Name":
                player_two_name = value

        replay_dict = {"World": "", "NumRounds": 0, "MatchLength": 0,
                       "Players": {player_one_name: {}, player_two_name: {}},
                       "path_ini": str(self._replay_path) + "/" + replay_name + ".ini",
                       "path_rnd": str(self._replay_path) + "/" + replay_name + ".rnd"}

        current_player = ""
        current_fighter = ""
        # go through this again...
        for row in raw_replay.read_text().splitlines():
            key, value = row.split(maxsplit=1)
            if key == "World":
                replay_dict["World"] = value
            elif key == "NumRounds":
                replay_dict["NumRounds"] = value
            elif key == "MatchLength":
                replay_dict["MatchLength"] = value
            elif key == "Player":
                if value == "1":
                    current_player = player_one_name
                elif value == "2":
                    current_player = player_two_name
            elif key == "Fighter":
                current_fighter = value
                replay_dict["Players"][current_player].update({value: {"Fighter": value}})
            elif key == "Color":
                replay_dict["Players"][current_player][current_fighter].update({"Color": value})

        return replay_dict

    def process_directory(self):
        replay_name_list = sorted(self._replay_path.iterdir())
        replay_name_list = [each.stem for each in replay_name_list]
        replay_name_list = list(dict.fromkeys(replay_name_list))

        replays_dict = {}
        for replay in replay_name_list:
            replays_dict.update({replay: self.read_replay(replay)})

        return replays_dict


# testing
if __name__ == "__main__":
    # hardcoded path for testing
    test_path = Path('.').joinpath('sample_replays')

    replay_reader = ReplayReader()
    replay_reader.set_path(test_path)

    import json

    print("TESTING INDIVIDUAL REPLAY")
    test = replay_reader.read_replay("round_0001")
    print_replay(test)
    print("TESTING DIRECTORY OF REPLAYS")
    test = replay_reader.process_directory()
    print_replay(test)
