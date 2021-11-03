import concurrent.futures
import time


def merge_dict_of_lists(dol1, dol2):
    result = dict(dol1, **dol2)
    result.update((k, dol1[k] + dol2[k])
                  for k in set(dol1).intersection(dol2))
    return result


def create_index_entry_for(filename, sleep_time):
    position = 0
    index_entry = {}
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            for token in line.split():
                if token not in index_entry:
                    index_entry[token] = [(filename, [])]
                token_list = index_entry[token]
                token_list[0][1].append(position)
                position = position + 1
    time.sleep(sleep_time)
    return index_entry


if __name__ == '__main__':
    sleep_times = [10, 3, 8]  # total time sequential 21 seconds

    # Sequential Processing
    t1 = time.perf_counter()
    resulting_index = {}
    for i, sleep_time in enumerate(sleep_times):
        current_index = create_index_entry_for(f'simple-dummy-files/test{i}.txt', sleep_time)
        resulting_index = merge_dict_of_lists(current_index, resulting_index)
    print(resulting_index)
    t2 = time.perf_counter()
    sequential_time_needed = t2 - t1

    # Parallel Processing
    t1 = time.perf_counter()
    resulting_index = {}
    file_names = [f'simple-dummy-files/test{i}.txt' for i in range(0, 3)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        all_indexes = executor.map(create_index_entry_for, file_names, sleep_times)
        for index in all_indexes:
            resulting_index = merge_dict_of_lists(index, resulting_index)
    print(resulting_index)
    t2 = time.perf_counter()
    parallel_time_needed = t2 - t1

    print('')
    print(f'Sequential Processing finished in {sequential_time_needed} seconds')
    print(f'Parallel Processing finished in {parallel_time_needed} seconds')
