
def save_game(game_name):
    from bot_firestore_game import Game
    import json
    games_generator = Game.query([        
        ('name', '==', game_name)
    ]).get()
    for g in games_generator:
        output_file_path = './tmp/{}.json'.format(g.id)
        game_dict = g.to_dict()
        with open(output_file_path, 'w') as f_out:
            json.dump(game_dict, f_out, indent=3, ensure_ascii=False)
        print("Saved {}".format(output_file_path))

if __name__ == '__main__':
    save_game('PLAGIOWOODROSE2')
    