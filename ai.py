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
    last_pipes = [None] * len(birds)

    while game.run and len(birds) > 0:
        pipe = game.pipes[0]  # første pipe på banen

        for i, bird in enumerate(birds):
            pipe_top_y = MAP_HEIGHT - pipe.height - pipe.gap
            pipe_bottom_y = MAP_HEIGHT - pipe.height
            pipe_top = abs(bird.y - pipe_top_y)
            pipe_bottom = abs(bird.y - pipe_bottom_y)
            bird_y = bird.y
            inputs = (bird_y, pipe_top, pipe_bottom)

            output = nets[i].activate(inputs)[0]
            if output > 0.5:
                bird.jump()

        game.update()
        game.draw()
        


        # Fjern døde fugle og opdater fitness
        for i in reversed(range(len(birds))):
            bird = birds[i]
            if bird.out_of_map() or pipe.collides_with_bird(bird):
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
                last_pipes.pop(i)  # fjern samme indeks her
            else:
                ge[i].fitness += 0.1
                if last_pipes[i] != pipe and bird.x > pipe.x + pipe.width:
                    ge[i].fitness += 5
                    last_pipes[i] = pipe  # type: ignore # opdater kun, hvis ikke fjernet


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(winner, config)
    game = Game(ai_mode=True)
    game.birds = [Bird(150, MAP_HEIGHT // 2)]
    bird = game.birds[0]

    while game.run:
        pipe = game.pipes[0]

        pipe_top_y = MAP_HEIGHT - pipe.height - pipe.gap
        pipe_bottom_y = MAP_HEIGHT - pipe.height
        pipe_top = abs(bird.y - pipe_top_y)
        pipe_bottom = abs(bird.y - pipe_bottom_y)
        bird_y = bird.y

        inputs = (bird_y, pipe_top, pipe_bottom)
        output = net.activate(inputs)[0]

        if output > 0.5:
            bird.jump()

        game.update()
        game.draw()

        # Du kan stoppe hvis fuglen dør (valgfrit):
        #if bird.out_of_map() or pipe.collides_with_bird(bird):
        #    break





def get_latest_checkpoint(dir,file_start_with):
    file_names = []
    newest_file_no = 0

    for file in os.listdir(dir):
        if(file.startswith(file_start_with)):
            file_names.append(file)
    
    if len(file_names) == 0:
        return None

    for file_name in file_names:
        arr = file_name.split('-')
        no = int(arr[-1])
        if no > newest_file_no:
            newest_file_no = int(no)
    
    return dir + '/' + file_start_with + str(newest_file_no)


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2))

    winner = p.run(eval_genomes, 2)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)