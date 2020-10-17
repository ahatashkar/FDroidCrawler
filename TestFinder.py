import os
import sys

import matplotlib.pyplot as plt
import json

has_junit = 0
has_espresso = 0
has_robolectric = 0

count_junit = 0
count_espresso = 0
count_robolectric = 0

total_count_junit = 0
total_count_espresso = 0
total_count_robolectric = 0

total_test = 0
total_junit = 0
total_espresso = 0
total_robolectric = 0

only_junit = 0
only_espresso = 0
only_robolectric = 0

junit_espresso = 0
junit_robolectric = 0
espresso_robolectric = 0

lines_code = 0
lines_test = 0

plot_junit = {}
plot_espresso = {}
plot_robolectric = {}

release_list = {}
release_list_test = {}
release_list_junit = {}
release_list_espresso = {}
release_list_robolectric = {}
release_list_lines = {}


def analyse(dir):
    global has_junit, has_espresso, count_espresso, count_junit, lines_test, lines_code, has_robolectric, count_robolectric

    for each in os.listdir(dir):
        current = os.path.join(dir, each)
        if os.path.isdir(current):
            analyse(current)

        elif os.path.isfile(current):
            if '.java' in current or '.kt' in current:
                datafile = open(current, encoding='latin-1')
                lines = datafile.readlines()

                lines_count = 0
                # x = os.popen('cloc '+current+' --json')
                # xx = x.read()
                # d = json.loads(xx)
                # lines_count = d['SUM']['code']

                temp_lines = []
                for line in lines:
                    if line.startswith("\n") or \
                            line.lstrip().startswith('//') or \
                            line.lstrip().startswith("/*") or \
                            line.lstrip().startswith("*") or \
                            line.lstrip().startswith("*/"):
                        continue
                    else:
                        temp_lines.append(line)
                lines_count = temp_lines.__len__()

                has_test_flag = False
                for line in lines:
                    if 'org.junit.Test' in line:
                        has_test_flag = True
                        lines_test = lines_test + lines_count
                        junit_flag = True

                        for temp_line in lines:
                            if 'androidx.test.espresso' in temp_line \
                                    or 'android.support.test.espresso' in temp_line:
                                has_espresso = 1
                                junit_flag = False

                                for temp in lines:
                                    if '@Test' in temp:
                                        count_espresso = count_espresso + 1

                                break

                            elif 'org.robolectric.Robolectric' in temp_line:
                                has_robolectric = 1
                                junit_flag = False

                                for temp in lines:
                                    if '@Test' in temp:
                                        count_robolectric = count_robolectric + 1

                                break

                        if junit_flag:
                            has_junit = 1

                            for temp in lines:
                                if '@Test' in temp:
                                    count_junit = count_junit + 1

                if not has_test_flag:
                    lines_code = lines_code + lines_count


root = os.getcwd() + '/Projects/Unzip'
output_path = os.getcwd() + '/Projects/Output'
# total = os.listdir(root).__len__()
total = 0
print("Project,release_date,has_junit,has_espresso,has_robolectric,count_junit,count_espresso,count_robolectric,lines_code,"
      "lines_test")
for directory in os.listdir(root):
    os.chdir(root)

    datafile = open(output_path+'/info.json', encoding='latin-1')
    lines = datafile.readlines()
    app_name = directory.replace('-', '').replace('master', '').lower()
    release_date = ""
    for line in lines:
        try:

            temp_line = line.lower().split(',')[0].split('/')[-1].replace('-', '').replace(' ', '')
            if app_name in temp_line or temp_line in app_name:
                release_date = line.split(',')[1].split(':')[1].replace('"', '').replace('}', '').replace('\n', '')
                release_date = release_date.split('-')[0]
                break
        except:
            continue

    current_dir = os.path.join(root, directory)

    if os.path.isdir(current_dir):
        os.chdir(current_dir)

        has_junit = 0
        has_espresso = 0
        has_robolectric = 0
        count_espresso = 0
        count_junit = 0
        count_robolectric = 0
        lines_code = 0
        lines_test = 0

        analyse('.')
        if lines_code == 0:
            continue

        total = total + 1

        if has_junit > 0 or has_espresso > 0 or has_robolectric > 0:
            total_test = total_test + 1

        if has_junit > 0:
            total_junit = total_junit + 1
        if has_espresso > 0:
            total_espresso = total_espresso + 1
        if has_robolectric > 0:
            total_robolectric = total_robolectric + 1

        if has_junit > 0 and has_espresso == 0 and has_robolectric == 0:
            only_junit = only_junit + 1
        if has_junit == 0 and has_espresso > 0 and has_robolectric == 0:
            only_espresso = only_espresso + 1
        if has_junit == 0 and has_espresso == 0 and has_robolectric > 0:
            only_robolectric = only_robolectric + 1

        if has_junit > 0 and has_espresso > 0 and has_robolectric == 0:
            junit_espresso = junit_espresso + 1
        if has_junit > 0 and has_espresso == 0 and has_robolectric > 0:
            junit_robolectric = junit_robolectric + 1
        if has_junit == 0 and has_espresso > 0 and has_robolectric > 0:
            espresso_robolectric = espresso_robolectric + 1

        total_count_junit = total_count_junit + count_junit
        total_count_espresso = total_count_espresso + count_espresso
        total_count_robolectric = total_count_robolectric + count_robolectric

        if release_date != "":
            if has_junit > 0 or has_espresso > 0 or has_robolectric > 0:
                if release_list_test.get(release_date) is not None:
                    release_list_test[release_date] = release_list_test[release_date] + 1
                else:
                    release_list_test[release_date] = 1

            if release_list.get(release_date) is not None:
                release_list[release_date] = release_list[release_date] + 1
            else:
                release_list[release_date] = 1

            if has_junit > 0:
                if release_list_junit.get(release_date) is not None:
                    release_list_junit[release_date] = release_list_junit[release_date] + 1
                else:
                    release_list_junit[release_date] = 1

            if has_espresso > 0:
                if release_list_espresso.get(release_date) is not None:
                    release_list_espresso[release_date] = release_list_espresso[release_date] + 1
                else:
                    release_list_espresso[release_date] = 1

            if has_robolectric > 0:
                if release_list_robolectric.get(release_date) is not None:
                    release_list_robolectric[release_date] = release_list_robolectric[release_date] + 1
                else:
                    release_list_robolectric[release_date] = 1

            if plot_junit.get(release_date) is not None:
                plot_junit[release_date] = plot_junit[release_date] + count_junit
            else:
                plot_junit[release_date] = count_junit

            if plot_espresso.get(release_date) is not None:
                plot_espresso[release_date] = plot_espresso[release_date] + count_espresso
            else:
                plot_espresso[release_date] = count_espresso

            if plot_robolectric.get(release_date) is not None:
                plot_robolectric[release_date] = plot_robolectric[release_date] + count_robolectric
            else:
                plot_robolectric[release_date] = count_robolectric

            test_ratio = lines_test / lines_code
            if release_list_lines.get(release_date) is not None:
                release_list_lines[release_date] = release_list_lines[release_date] + test_ratio
            else:
                release_list_lines[release_date] = test_ratio

        print(directory + ',' +
              release_date + ',' +
              str(has_junit) + ',' +
              str(has_espresso) + ',' +
              str(has_robolectric) + ',' +
              str(count_junit) + ',' +
              str(count_espresso) + ',' +
              str(count_robolectric) + ',' +
              str(lines_code) + ',' +
              str(lines_test))

print('----------------------------')
print('total projects:,' + str(total))
print('total test:,' + str(total_test))
print('total junit:,' + str(total_junit))
print('total espresso:,' + str(total_espresso))
print('total robolectric:,' + str(total_robolectric))
print('only junit:,' + str(only_junit))
print('only espresso:,' + str(only_espresso))
print('only robolectric:,' + str(only_robolectric))
print('junit & espresso:,' + str(junit_espresso))
print('junit & robolectric:,' + str(junit_robolectric))
print('espresso & robolectric:,' + str(espresso_robolectric))
print('total count junit:,' + str(total_count_junit))
print('total count espresso:,' + str(total_count_espresso))
print('total count robolectric:,' + str(total_count_robolectric))
print('----------------------------')
print('year,projects,has test,has junit,has espresso,has robolectric,test line ratio,has test ratio')
release_list = sorted(release_list.items(), key=lambda t: t[0])

for item in release_list:
    year = item[0]
    projects = item[1]

    if release_list_test.get(year) is None:
        has_test = 0
    else:
        has_test = release_list_test.get(year)

    if release_list_junit.get(year) is None:
        has_junit = 0
    else:
        has_junit = release_list_junit.get(year)

    if release_list_espresso.get(year) is None:
        has_espresso = 0
    else:
        has_espresso = release_list_espresso.get(year)

    if release_list_robolectric.get(year) is None:
        has_robolectric = 0
    else:
        has_robolectric = release_list_robolectric.get(year)

    if release_list_lines.get(year) is None:
        line_ratio = 0
    elif int(projects) > 0:
        line_ratio = release_list_lines.get(year) / float(projects)

    print(year + ',' +
          str(projects) + ',' +
          str(has_test) + ',' +
          str(has_junit) + ',' +
          str(has_espresso) + ',' +
          str(has_robolectric) + ',' +
          str(line_ratio) + ',' +
          str(has_test/projects))

category_name = ''
if sys.argv.__len__() > 1:
    arg = sys.argv[1]
    category_name = arg.split('/')[-2]

plot_junit = sorted(plot_junit.items(), key=lambda t: t[0])

x, y = zip(*plot_junit)
plt.plot(x, y, label='junit')

plot_espresso = sorted(plot_espresso.items(), key=lambda t: t[0])
x, y = zip(*plot_espresso)
plt.plot(x, y, label='espresso')

plot_robolectric = sorted(plot_robolectric.items(), key=lambda t: t[0])
x, y = zip(*plot_robolectric)
plt.plot(x, y, label='robolectric')
plt.legend(loc='best')
plt.ylabel('Test cases')
plt.xlabel('Years')
plt.title(category_name)
plt.savefig(output_path+"/plot_"+category_name+".jpg")
