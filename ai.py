import neat
import pickle
import os
from game import Game
from settings import MAP_HEIGHT,MAP_WIDTH

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()

        genome.fitness = 0

        while game.run:
            bird = game.bird

            # Input til NEAT: fuglens y-position normaliseret
            pipe_mid_y = (MAP_HEIGHT - game.pipe.height - game.pipe.gap / 2) / MAP_HEIGHT
            pipe_x = game.pipe.x / MAP_WIDTH
            bird_y = bird.y / MAP_HEIGHT
            inputs = [bird_y,pipe_x,pipe_mid_y]

            output = net.activate(inputs)[0]
            if output > 0.5:
                bird.jump()

            game.update()
            game.draw()

            genome.fitness += 0.1  # beløn længere overlevelse

            if bird.out_of_map() or game.pipe.collides_with_bird(bird):
                break

def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(winner, config)
    game = Game()
    bird = game.bird

    while game.run:
        pipe_mid_y = (MAP_HEIGHT - game.pipe.height - game.pipe.gap / 2) / MAP_HEIGHT
        pipe_x = game.pipe.x / MAP_WIDTH
        bird_y = bird.y / MAP_HEIGHT

        output = net.activate([bird_y, pipe_x, pipe_mid_y])[0]
        if output > 0.5:
            bird.jump()

        game.update()
        game.draw()

        if bird.out_of_map() or game.pipe.collides_with_bird(bird):
            break



def get_latest_checkpoint(file_start_with):
    file_names = []
    newest_file_no = 0
    
    for file in os.listdir():
        if(file.startswith(file_start_with)):
            file_names.append(file)
    
    if file_names.count == 0:
        return None

    for file_name in file_names:
        arr = file_name.split('-')
        no = int(arr[-1])
        if no > newest_file_no:
            newest_file_no = int(no)
    
    return file_start_with + str(newest_file_no)


def run_neat(config):
    checkpoint_file = get_latest_checkpoint('neat-checkpoint-')
    if checkpoint_file:
        p = neat.Checkpointer.restore_checkpoint(checkpoint_file)
    else:
        p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 10)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

