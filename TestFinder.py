import os

has_junit = 0
has_espresso = 0

count_junit = 0
count_espresso = 0

total_test = 0
total_junit = 0
total_espresso = 0

lines_code = 0
lines_test = 0


def analyze(dir):
    global has_junit, has_espresso, count_espresso, count_junit, lines_test, lines_code

    for each in os.listdir(dir):
        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyze(current)

        elif os.path.isfile(current):
            if '.java' in current or '.kt' in current:
                datafile = open(current)
                lines = datafile.readlines()

                temp_lines = []
                for line in lines:
                    if line.lstrip().startswith("package") or \
                            line.startswith("\n") or \
                            line.lstrip().startswith("import") or \
                            line.lstrip().startswith('//') or \
                            line.lstrip().startswith("/*") or \
                            line.lstrip().startswith("*") or \
                            line.lstrip().startswith("*/"):
                        continue
                    else:
                        temp_lines.append(line)

                has_test_flag = False
                for line in lines:
                    if 'org.junit.Test' in line:
                        has_test_flag = True
                        lines_test = lines_test + temp_lines.__len__()
                        espresso_flag = False

                        for temp_line in lines:
                            if 'androidx.test.espresso' in temp_line \
                                    or 'android.support.test.espresso' in temp_line:
                                has_espresso = 1
                                espresso_flag = True

                                for temp in lines:
                                    if '@Test' in temp:
                                        count_espresso = count_espresso + 1

                                break

                        if not espresso_flag:
                            has_junit = 1

                            for temp in lines:
                                if '@Test' in temp:
                                    count_junit = count_junit + 1

                if not has_test_flag:
                    lines_code = lines_code + temp_lines.__len__()


root = os.getcwd() + '/Projects/Unzip'
total = os.listdir(root).__len__()
print("Project;has_junit;has_espresso;count_junit;count_espresso;lines_code;lines_test")
for directory in os.listdir(root):
    os.chdir(root)
    current_dir = os.path.join(root, directory)
    if os.path.isdir(current_dir):
        os.chdir(current_dir)

        has_junit = 0
        has_espresso = 0
        count_espresso = 0
        count_junit = 0
        lines_code = 0
        lines_test = 0

        analyze('.')
        if has_junit > 0 or has_espresso > 0:
            total_test = total_test + 1
        if has_junit > 0:
            total_junit = total_junit + 1
        if has_espresso > 0:
            total_espresso = total_espresso + 1

        print(directory + ' ; ' +
              str(has_junit) + ' ; ' +
              str(has_espresso) + ' ; ' +
              str(count_junit) + ' ; ' +
              str(count_espresso) + ' ; ' +
              str(lines_code) + ' ; ' +
              str(lines_test))

print('----------------------------')
print('total projects: ' + str(total))
print('total test: ' + str(total_test))
print('total junit: ' + str(total_junit))
print('total espresso: ' + str(total_espresso))
