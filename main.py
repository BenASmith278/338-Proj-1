import re

log_string = ""
times = []
text = []
ops = []
first_ind = 0

def dissect_string():
    with open ('log.txt') as file:
        data = file.read().strip()

        while len(data) > 500:
            match = re.search(r" {3} ?[0-9]+\.[0-9]+]", data)
            times.append(match.group()[:-1].strip())                            # add times string to list
            first_ind = match.span()                                            # get indices of match
            
            next = data[first_ind[1]:]                                          # repeat for next match
            next_match = re.search(r" {3} ?[0-9]+\.[0-9]+]", next)
            next_ind = next_match.span()
            text.append(data[first_ind[1]+1:(next_ind[0]+first_ind[1]-2)])      # get text from between matches

            data = next

    return data

def get_nums(sting):
    return(re.search(r" {3} ?[0-9]+\.[0-9]+]", sting))                          # match the timestamp of bootlog

dissect_string()

for x in range(len(times)):
    ops.append([times[x], text[x]])                                             # make [[time, text], ...]

print(ops[25])
