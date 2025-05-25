import neat
import pickle
import os
from bird import Bird
from game import Game
from settings import MAP_HEIGHT,MAP_WIDTH

def eval_genomes(genomes, config):
    nets = []
    birds = []
    ge = []

    game = Game(ai_mode=True)

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        bird = Bird(150, MAP_HEIGHT // 2)

        nets.append(net)
        birds.append(bird)
        ge.append(genome)

    game.birds = birds

    while game.run and len(birds) > 0:
        pipe = game.pipes[0]  # første pipe på banen

        for i, bird in enumerate(birds):
            # Input: normaliseret fugleposition og pipe
            pipe_mid_y = (MAP_HEIGHT - pipe.height - pipe.gap / 2) / MAP_HEIGHT
            pipe_x = pipe.x / MAP_WIDTH
            bird_y = bird.y / MAP_HEIGHT
            inputs = [bird_y, pipe_x, pipe_mid_y]

            output = nets[i].activate(inputs)[0]
            if output > 0.5:
                bird.jump()

        game.update()
        game.draw()

        # Fjern døde fugle og opdater fitness
        for i in reversed(range(len(birds))):
            bird = birds[i]
            if bird.out_of_map():
                ge[i].fitness -= 1
                del birds[i]
                del nets[i]
                del ge[i]
            else:
                for pipe in game.pipes:
                    if pipe.collides_with_bird(bird):
                        ge[i].fitness -= 1
                        del birds[i]
                        del nets[i]
                        del ge[i]
                        break
                else:
                    ge[i].fitness += 0.1  # beløn overlevelse

def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(winner, config)
    game = Game(True)
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
    
    if len(file_names) == 0:
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

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

