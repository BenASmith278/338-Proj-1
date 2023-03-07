import re

log_string = ""
times = []
text = []
ops = []

def dissect_string(filepath):
    with open (filepath) as file:
        data = file.read().strip()

        while find_next_match(data, find_numbers(data).span()[1]):              # while there is a next
            match = find_numbers(data)                  
            times.append(float(match.group()[:-1].strip()))                     # add times string to list
            first_ind = match.span()                                            # get indices of match
            
            next = data[first_ind[1]:]                                          # repeat for next match
            next_match = find_numbers(next)
            next_ind = next_match.span()
            text.append(data[first_ind[1]+1:(next_ind[0]+first_ind[1]-2)])      # get text from between matches

            data = next
        
        last_match = find_numbers(data)                                         # add last operation
        times.append(float(last_match.group()[:-1].strip()))
        text.append(data[last_match.span()[1]:])

    return data                   

def find_next_match(string, index):                                             # find next match starting at index
    next = string[index:]
    next_match = find_numbers(next)

    return next_match

def find_numbers(string):
    return re.search(r" {3} ?[0-9]+\.[0-9]+]", string)                          # match the timestamp of bootlog

def sort_func(e):
    return e['elapsed']                                                         # sort by elapsed

def get_times(filepath):
    dissect_string(filepath)
    out = open("output.txt", "w")

    for x in range(len(times)):                                                 # make [{time: time, text: text, elapsed: elapsed}, ...]
        ops.append({"time": times[x],
                    "text": text[x],
                    "elapsed": 0})
    
    for x in range(len(ops) - 1):                                               # add elapsed time
        elapsed = times[x] - times[x - 1]
        if elapsed < 0:
            elapsed = 0
        ops[x]["elapsed"] = elapsed
    
    ops[len(ops) - 1]['elapsed'] = times[len(ops) - 1] - times[len(ops) - 2]    # last op
    ops.sort(key=sort_func, reverse=True)

    for op in ops:
        out.write("OPERATION: " + op["text"] +
                  "\n TIME: " + str(op["elapsed"]) + 
                  "\n\n")
    
    return

get_times("log.txt")
