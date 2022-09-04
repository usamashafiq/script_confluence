from atlassian import Confluence
import csv
import pwinput

username = input("Enter the account username : ")
password = pwinput.pwinput()
# make connection with confluence account to get the data
confluence = Confluence(
    url='https://confluence.catena-x.net',
    username=username,
    password=password)

print("connected")
print("Making a files plesae wait.........")

with open('space-key.txt') as f:
    lines = f.readlines()

new_lst = [x[:-1] for x in lines]
final_user_name = []

# get the all data relate to spaces
status_space = confluence.get_all_spaces()

# get the all data relate to groups
status_groups = confluence.get_all_groups()

# get the all data relate to members
status_members = confluence.get_group_members()

# remove the unnecessary things
new_dict = dict((item['name'], item) for item in status_space['results'])
final = new_dict.keys()
final_data = list(final)

# get the names of group from list of dict
groups = [d['name'] for d in status_groups if 'name' in d]

# get the names of members from list of dict
members = [d['displayName'] for d in status_members if 'displayName' in d]

for i in new_lst:
    try:
        # get the all data relate to spaces
        status_space_per = confluence.get_space_permissions(i)
        # print(status_space)

        my_list = list(status_space_per[0].values())
        group_per = [d['userName'] for d in my_list[1] if "userName" in d]

        for val in group_per:
            if val != None:
                final_user_name.append(val)
    except:
        print(".......")


# make a cvs file for write the data
def csv_file(name, list_name):
    file = open(name + ".csv", 'w+', newline='')
    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(list_name)


# list into a list of lists to write in csv file in good way
def extractDigits(lst):
    res = []
    for el in lst:
        sub = el.split(', ')
        res.append(sub)

    return res


# pass the space name of list to get the list of list and save in check varibale
write_list_of_list_space = extractDigits(final_data)
# pass the groups name of list to get the list of list
write_list_of_list_group = extractDigits(groups)
# pass the members name of list to get the list of list
# write_list_of_list_members = extractDigits(members)

write_list_of_list_permision = extractDigits(final_user_name)

# make a csv files
csv_file("read_space", write_list_of_list_space)
csv_file("read_spaces_groups", write_list_of_list_group)
csv_file("read_space_Users", write_list_of_list_permision)

print("All files successful created ")
