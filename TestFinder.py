import os

junit_count = 0
espresso_count = 0

total_test = 0
total_junit = 0
total_espresso = 0



def analyze(dir):
    global junit_count
    global espresso_count

    for each in os.listdir(dir):
        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyze(current)

        elif os.path.isfile(current):
            if '.java' in current or '.kt' in current:
                datafile = open(current)
                lines = datafile.readlines()
                for line in lines:
                    if 'import static androidx.test.espresso' in line:
                        # print(current)
                        # junit_count = junit_count + 1
                        espresso_count = 1

                    if 'import org.junit.Test' in line:
                        junit_count = 1


root = os.getcwd() + '/Projects/Unzip'
total = os.listdir(root).__len__()
for directory in os.listdir(root):
    os.chdir(root)
    current_dir = os.path.join(root, directory)
    if os.path.isdir(current_dir):
        os.chdir(current_dir)
        junit_count = 0
        espresso_count = 0
        analyze('.')
        if junit_count > 0 or espresso_count > 0:
            total_test = total_test + 1
        if junit_count > 0:
            total_junit = total_junit + 1
        if espresso_count > 0:
            total_espresso = total_espresso + 1

        print(directory + ' : ' + str(junit_count) + ' , ' + str(espresso_count))

print('----------------------------')
print('total projects: ' + str(total))
print('total test: ' + str(total_test))
print('total junit: ' + str(total_junit))
print('total espresso: ' + str(total_espresso))
print('percentage: ' + str((total_test/total)*100))
