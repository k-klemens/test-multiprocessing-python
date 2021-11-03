import concurrent.futures
import time
from random import randrange, sample


def create_index_entry_for(filename):
    position = 0
    index_entry = {}
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            for token in line.split():
                if token not in index_entry:
                    index_entry[token] = []
                index_entry[token].append(position)
                position = position + 1
    return index_entry


def create_random_dict_of_lists(sleep):
    random_dict = {}
    num_elements = randrange(10)
    for _ in range(0, num_elements):
        key = randrange(10)
        num_values = randrange(5) + 1
        values = sample(range(0, 5), k=num_values)
        if f'{key}' not in random_dict:
            random_dict[f'{key}'] = []
        random_dict[f'{key}'].extend(values)
    time.sleep(sleep)
    return random_dict


def merge_dict_of_lists(dol1, dol2):
    result = dict(dol1, **dol2)
    result.update((k, dol1[k] + dol2[k])
                  for k in set(dol1).intersection(dol2))
    return result


if __name__ == '__main__':
    sleep_times = [1, 2, 1, 2, 3, 2, 1, 2, 1, 2] #sum = 17

    t1 = time.perf_counter()
    resulting_dict = {}
    for sleep_time in sleep_times:
        dict_to_be_appended = create_random_dict_of_lists(sleep_time)
        resulting_dict = merge_dict_of_lists(dict_to_be_appended, resulting_dict)
    t2 = time.perf_counter()
    print(f'Sequential Processing Finished in {t2 - t1} seconds')

    t1 = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(create_random_dict_of_lists, sleep_times)
        resulting_dict = {}
        for result in results:
            resulting_dict = merge_dict_of_lists(result, resulting_dict)
    t2 = time.perf_counter()
    print(f'Parallel Processing Finished in {t2 - t1} seconds')
