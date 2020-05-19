import re
import operator
import sys
import csv

def process_logfile(logfile):
    error_msgs = {}
    user_stats = {}
    pattern1 = r"ticky: ERROR ([\w ]*) "
    pattern2 = r"ticky: INFO ([\w ]*) "
    
    with open(logfile, 'r') as f:
        for line in f:
            if "ticky" not in line:
                continue
            if re.search(pattern1, line) is not None:
                result = re.findall(pattern1, line)
                error = result[0]
                if error not in error_msgs.keys():
                    error_msgs[error] = 1
                else:
                    error_msgs[error] += 1
                result = re.findall(r"\([\w\.]*\)", line)
                user_name = result[0][1:-1]
                if user_name not in user_stats.keys():
                    L = [0] * 2
                    user_stats[user_name] = L
                    L[1] = 1
                else:
                    (user_stats[user_name])[1] += 1
                    
            elif re.search(pattern2, line) is not None:
                result = re.findall(r"\([\w\.]*\)", line)
                user_name = result[0][1:-1]
                if user_name not in user_stats.keys():
                    L = [0] * 2
                    user_stats[user_name] = L
                    L[0] = 1
                else:
                    (user_stats[user_name])[0] += 1
           
        f.close()
    return error_msgs, user_stats

def write_to_csv(error_msgs, user_stats):
    with open('error_message.csv', 'w') as f:
        writer = csv.writer(f)
        col_names = [("Error", "Count")]
        writer.writerows((col_names + sorted(error_msgs.items(), key = operator.itemgetter(1), reverse=True)))
        f.close()
        
    with open('user_statistics.csv', 'w') as f:
        list_of_user_stats2 = []
        list_of_user_stats = sorted(user_stats.items(), key = operator.itemgetter(0))
        writer = csv.writer(f)
        col_names = [("Username", "INFO", "ERROR")]
        for elem in list_of_user_stats:
            tu = elem[0], elem[1][0], elem[1][1]
            list_of_user_stats2.append(tu)
        writer.writerows((col_names + list_of_user_stats2))
        f.close()

if __name__ == '__main__':
    logfile = sys.argv[1]
    error_msgs, user_stats = process_logfile(logfile)
    write_to_csv(error_msgs, user_stats)
    
            