import os

count = 0


def analyze(dir):
    global count
    for each in os.listdir(dir):
        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyze(current)

        elif os.path.isfile(current):
            if '.java' in current:
                datafile = open(current)
                lines = datafile.readlines()
                for line in lines:
                    if 'import org.junit.Test' in line:
                        # print(current)
                        count = count + 1


root = os.getcwd() + '/Projects/Unzip'
for directory in os.listdir(root):
    os.chdir(root)
    current_dir = os.path.join(root, directory)
    if os.path.isdir(current_dir):
        os.chdir(current_dir)
        count = 0
        analyze('.')
        print(directory + ' : ' + str(count))
