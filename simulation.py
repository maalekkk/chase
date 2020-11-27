import csv
import wolf
import sheep
import json
from parse_args import cls_logger, func_logger


@func_logger
def save_to_json_file(positions_data, path):
    with open(path, mode='w') as json_file:
        json.dump(positions_data, json_file, indent=5)


@func_logger
def save_to_csv_file(alive_sheep_data, path):
    with open(path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['round_no', 'alive_sheep'])
        writer.writeheader()
        for row in alive_sheep_data:
            writer.writerow({'round_no': row[0], 'alive_sheep': row[1]})


@cls_logger(func_logger)
class Simulation:
    def __init__(self, sheep_number=15, init_pos_limit=10.0, wolf_move_dist=1.0, sheep_move_dist=0.5):
        self.wolf = wolf.Wolf(wolf_move_dist)
        self.sheep = [sheep.Sheep(init_pos_limit, sheep_move_dist) for i in range(sheep_number)]

    def __repr__(self):
        return f"Simulation()"

    def moving_animals(self):
        for single_sheep in self.sheep:
            single_sheep.move()
        dead_sheep = self.wolf.move(self.sheep)
        return dead_sheep

    def simulate(self, round_number=50, json_file_path="alive.csv", csv_file_path="pos.json", wait=False):
        starters_sheep = self.sheep.copy()
        print('Round number', '{0: <15}'.format('Wolf position'), '{0: <8}'.format('Number of live sheep'),
              'Dead sheep number')
        positions_data, alive_sheep_data = [], []
        for i in range(round_number):
            if len(self.sheep) <= 0:
                break
            dead_sheep = self.moving_animals()
            if dead_sheep is not None:
                num_of_dead_sheep = starters_sheep.index(dead_sheep) + 1
                self.sheep.remove(dead_sheep)
            else:
                num_of_dead_sheep = '-'
            print('{0: <12}'.format(str(i + 1)), '{0: <7}'.format(str("{:.3f}".format(self.wolf.x))),
                  '{0: <7}'.format(str("{:.3f}".format(self.wolf.y))), '{0: <20}'.format(len(self.sheep)),
                  num_of_dead_sheep)
            positions_data.append({
                "round_no": str(i + 1),
                "wolf_pos": self.wolf.coords,
                "sheep_pos": [single_sheep.coords for single_sheep in self.sheep]})
            alive_sheep_data.append([i + 1, len(self.sheep)])
            if wait and i < round_number - 1:
                input('Press enter to go to the next round.')
        save_to_json_file(positions_data, json_file_path)
        save_to_csv_file(alive_sheep_data, csv_file_path)
