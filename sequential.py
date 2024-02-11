from random import randint, randrange
import requests
import time
import hashlib


def serial_number_generate(map, width, height):
    serial_nums = [[0 for _ in range(width)] for _ in range(height)]
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


def rover_path_draw(rover, n_map, map_width, map_height, serial_numbers):
    directions = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    response = requests.get("https://coe892.reev.dev/lab1/rover/" + str(rover))
    command = response.json()['data']['moves']
    m_map = [['0' for _ in range(map_width)] for _ in range(map_height)]
    m_map[0][0] = "*"
    x_pos, y_pos, cur_dir = 0, 0, 2

    with open("path_" + str(rover) + ".txt", "w") as fp:
        for move in command:
            if move == 'M':
                if n_map[y_pos][x_pos] == '1':
                    m_map[y_pos][x_pos] = 'Explode'
                    break
                x_pos = x_pos + directions[cur_dir][0] if 0 <= x_pos + directions[cur_dir][0] < map_width else x_pos
                y_pos = y_pos + directions[cur_dir][1] if 0 <= y_pos + directions[cur_dir][1] < map_height else y_pos
                m_map[y_pos][x_pos] = '*'

            elif move == 'L':
                cur_dir = (cur_dir + 3) % 4

            elif move == 'R':
                cur_dir = (cur_dir + 1) % 4

            elif move == 'D':
                if n_map[y_pos][x_pos] == '1':
                    t1 = time.time()
                    n_map[y_pos][x_pos] = '0'
                    mine_detect_serial = serial_numbers[y_pos][x_pos]
                    hash_value = 'test'
                    while hash_value[0] != '0':
                        pin = randint(999, 9999)
                        mine_detect_serial = str(pin) + str(mine_detect_serial)
                        mine_detect_serial = mine_detect_serial.encode()
                        hash_value = hashlib.sha256(mine_detect_serial).hexdigest()
                    m_map[y_pos][x_pos] = 'Disarm'
                    t2 = time.time()
                    print("Time to disarm for rover " + str(rover) + f': {t2-t1} seconds')

        tw1 = time.time()
        for row in m_map:
            fp.write(' '.join(str(i) for i in row) + '\n')
        tw2 = time.time()
        print("Time to write path for rover " + str(rover) + f': {tw2-tw1} seconds')


if __name__ == '__main__':
    start_time = time.time()
    with open('map.txt') as file:
        map_data = [line.split() for line in file]

    width = int(map_data[0][1])
    height = int(map_data[0][0])
    map_data = map_data[1:]
    serial_numbers = serial_number_generate(map_data, width, height)

    for rover_num in range(1, 11):
        rover_path_draw(rover_num, map_data, width, height, serial_numbers)

    print(f'Total Processing Time is {time.time() - start_time} seconds')