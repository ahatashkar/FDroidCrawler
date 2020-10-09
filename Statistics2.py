import os

total = 0
count_java = 0
count_kt = 0
count_dart = 0
count_ts = 0
count_js = 0

check_flag = False


def analyse(dir):
    global count_java, count_kt, count_dart, count_ts, count_js, check_flag

    os.chdir(dir)
    for each in os.listdir(dir):
        if check_flag:
            break

        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyse(current)

        elif os.path.isfile(current):
            if '.java' in current:
                count_java = count_java + 1
                check_flag = True
                break

            elif '.kt' in current:
                count_kt = count_kt + 1
                check_flag = True
                break

            elif '.ts' in current:
                count_ts = count_ts + 1
                check_flag = True
                break

            elif '.js' in current:
                count_js = count_js + 1
                check_flag = True
                break

            elif '.dart' in current:
                count_dart = count_dart + 1
                check_flag = True
                break

            else:
                continue


root_crawler = os.getcwd()
for directory in os.listdir(root_crawler):
    if 'Project' in directory:
        root_project = os.path.join(root_crawler, directory)
        os.chdir(root_project)

        for dir in os.listdir(root_project):
            if os.path.isdir(dir) and 'Unzip' in dir:
                root_unzip = os.path.join(root_project, dir)
                os.chdir(root_unzip)

                for project in os.listdir(root_unzip):
                    current_dir = os.path.join(root_unzip, project)
                    check_flag = False
                    total = total + 1
                    analyse(current_dir)

print("total: " + str(total))
print("java: " + str(count_java))
print("kt: " + str(count_kt))
print("type script: " + str(count_ts))
print("java script: " + str(count_js))
print("flutter: " + str(count_dart))
