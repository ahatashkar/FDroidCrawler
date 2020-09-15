import os

count = 0
has_test = 0


def analyze(dir):
    global count
    for each in os.listdir(dir):
        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyze(current)

        elif os.path.isfile(current):
            if '.java' in current or '.kt' in current:
                datafile = open(current)
                lines = datafile.readlines()
                for line in lines:
                    if 'import org.junit.Test' in line:
                        # print(current)
                        count = count + 1


root = os.getcwd() + '/Projects/Unzip'
total = os.listdir(root).__len__()
for directory in os.listdir(root):
    os.chdir(root)
    current_dir = os.path.join(root, directory)
    if os.path.isdir(current_dir):
        os.chdir(current_dir)
        count = 0
        analyze('.')
        if count > 0:
            has_test = has_test + 1
        print(directory + ' : ' + str(count))

print('----------------------------')
print('total projects: ' + str(total))
print('projects have test: ' + str(has_test))
print('percentage: ' + str((has_test/total)*100))
