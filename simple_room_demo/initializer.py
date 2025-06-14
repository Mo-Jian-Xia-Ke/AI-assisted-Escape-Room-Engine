from engine import main_engine

def main():
    item_config = "simple_room_demo/item_config.json"
    puzzle_config = "simple_room_demo/puzzle_config.json"
    end_item = 'door'
    end_item_state = -1
    action_type = "hybrid"
    main_engine.start_game(item_config_path=item_config, puzzle_config_path=puzzle_config, end_item_name=end_item, end_item_state_num=end_item_state, action_interpreter_type=action_type)

if __name__ == "__main__":
    main()