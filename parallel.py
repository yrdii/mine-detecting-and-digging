import threading
from random import randint, randrange
import hashlib
from time import perf_counter
import requests

lock = threading.Lock()


def serial_number_generate(map, width, height):
    serial_nums = [[0 for i in range(Width)] for j in range(Height)]
    row_num = 0
    for row in map:
        col_num = 0
        for val in row:
            if val == '1':
                mine_detect_serial = randrange(1000000, 1000000000)
                serial_nums[row_num][col_num] = mine_detect_serial
            col_num += 1
        row_num += 1

    with open("mineDetect.txt", "w") as fp:
        for row in serial_nums:
            fp.write(' '.join(str(i) for i in row) + '\n')
    return serial_nums


def rover_path_draw(rover, n_map, map_width, map_height):
    lock.acquire()
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    x_pos, y_pos, cur_dir = 0, 0, 2

    response = requests.get("https://coe892.reev.dev/lab1/rover/" + str(rover))
    command = response.json()['data']['moves']
    m_map = [['0' for i in range(map_width)] for j in range(map_height)]
    m_map[0][0] = "*"

    with open("path2_" + str(rover) + ".txt", "w") as fp:
        for i, move in enumerate(command):
            if move == 'M':
                if n_map[y_pos][x_pos] == '1':
                    m_map[y_pos][x_pos] = 'Explode'
                    break
                x_pos = x_pos + directions[cur_dir][0] if 0 <= x_pos + directions[cur_dir][0] < map_width else x_pos
                y_pos = y_pos + directions[cur_dir][1] if 0 <= y_pos + directions[cur_dir][1] < map_height else y_pos
                m_map[y_pos][x_pos] = '*'

            if move == 'L':
                cur_dir = (cur_dir + 3) % 4

            if move == 'R':
                cur_dir = (cur_dir + 1) % 4

            if move == 'D':
                if n_map[y_pos][x_pos] == '1':
                    t1 = perf_counter()
                    n_map[y_pos][x_pos] = '0'
                    mine_detect_serial = serialNumbers[y_pos][x_pos]
                    hash_value = 'test'
                    while hash_value[0] != '0':
                        pin = randint(999, 9999)
                        mine_detect_serial = str(pin) + '' + str(mine_detect_serial)
                        mine_detect_serial = mine_detect_serial.encode()
                        hash_value = hashlib.sha256(mine_detect_serial).hexdigest()
                    m_map[y_pos][x_pos] = 'Disarm'
                    t2 = perf_counter()
                    print("Time to disarm for rover " + str(rover) + f': {t2-t1} seconds')

        tw1 = perf_counter()
        for row in m_map:
            fp.write(' '.join([str(i) for i in row]) + '\n')
        tw2 = perf_counter()
        print("Time to write path for rover " + str(rover) + f': {tw2-tw1} seconds')
        lock.release()


if __name__ == '__main__':
    start_time = perf_counter()
    map = []
    with open('map.txt') as file:
        map = [line.split() for line in file]

    Width = int(map[0][1])
    Height = int(map[0][0])
    map = map[1:]
    serialNumbers = serial_number_generate(map, Width, Height)

    threads = []
    for rover_num in range(1, 11):
        x = threading.Thread(target=rover_path_draw, args=(rover_num, map, Width, Height))
        x.start()
        threads.append(x)

    for x in threads:
        x.join()

    end_time = perf_counter()

    print(f'Total Processing Time is {end_time - start_time} seconds')
