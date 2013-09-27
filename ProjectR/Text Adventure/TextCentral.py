# Unpleasant Text Adventure
# by Walt Rinehart 9/9/2013

# importz
import data
import textwrap
import time

#ENGINE!
# python C:\Python27\Q2API\xml\mk_class.py "C:\Users\wrinehart\PycharmProjects\ProjectR\Text Adventure\data.xml"
areas = {}
inv = []
hung = 0
def main():
    with open('data.xml') as fin:
        data_file = fin.read()

    success_flag, game_map = data.obj_wrapper(data_file)

    print "\n","\n",game_map.intro[0].value

    actions = {"inspect" : inspect,
               "interact" : interact,
               "eat" : eat, "inventory" : inventory, "hunger" : hunger}
    last_area = None
    current_area = game_map.area[0]
    global areas
    global inv
    areas = create_map(game_map)
    zones = {}
    for flag in areas:
        zones[flag] = 0

    while True:
        if current_area != last_area and zones[current_area.attrs['name']] == 0:
                print textwrap.fill(current_area.description[0].value)
                zones[current_area.attrs['name']] = 1
        elif current_area != last_area and zones[current_area.attrs['name']] == 1:
                print textwrap.fill(current_area.revisit[0].value)
        last_area = current_area
        timer = time.time()
        command = raw_input(">")
        print '\n'
        if time.time() - timer > int(current_area.attrs['time']):
            print textwrap.fill(current_area.timeup[0].value)
            play_again(current_area)
        else:
            command = command.lower()
            command1 = command.split()
            if command1[0] == 'inventory':
                inventory(inv)
            elif command1[0] == 'hunger':
                hunger(hung)
            else:
                words = command.split()
                if len(words) == 2:
                    cmd = words[0]
                    subject = words[1]
                    if cmd not in actions:
                        print "Invalid command, you silly wally."
                    else:
                        func = actions[cmd]
                        current_area = func(subject, current_area)
                        if current_area == False:

                            break
                else:
                    print "Invalid command, you silly wally."

def create_map(game_map):
    dict = {}
    for area in game_map.area:
        name = area.attrs['name']
        dict[name] = area
    return dict

def inventory(inv):
    for item in inv:
        item = item.upper()
        print item

def hunger(hung):
    if hung == 0:
        print "You are absolutely starving."
    elif hung == 1:
        print "You are still pretty damn hungry."
    elif hung == 2:
        print "You require more minerals."
    elif hung == 3:
        print "Your stomach is still rumbling."
    elif hung == 4:
        print "You could really use some more food."
    elif hung == 5:
        print "You are still hungry."
    elif hung == 6:
        print "You need more food."
    elif hung == 7:
        print "Food must go in your mouth."
    elif hung == 8:
        print "Need more grub."
    elif hung == 9:
        print "You are less hungry, but still could use more food."
    elif hung == 10:
        print "You are completely full!"

def inspect(subject, area):
    if subject:
        for ext in area.exit:
            if subject in ext.attrs['name'].split(','):
                print ext.inspect[0].value, '\n'
                return area
        for obj in area.object:
            if subject in obj.attrs['name'].split(','):
                print obj.inspect[0].value, '\n'
                return area
        print "This does not look unusual."
        return area
    else:
        print textwrap.fill(area.description[0].value)
        return area


def interact(subject, area):
    global inv
    if subject:
        for ext in area.exit:
            if subject in ext.attrs['name'].split(','):
                print textwrap.fill(ext.interact[0].value), '\n'
                area_name = ext.attrs["link"]
                new_area = areas.get(area_name)
                if new_area:
                    return new_area
                print "You can't go that way."
                return area

        for obj in area.object:
            if subject in obj.attrs['name'].split(','):
                print textwrap.fill(obj.interact[0].value), '\n'
                if obj.interact[0].attrs['alive'] == 'n':
                    return play_again(area)
                if obj.interact[0].attrs['inventory'] == 'y':
                    inv.append(obj.attrs['invname'])
                return area
        print "You can't do that."
        return area
    else:
        print textwrap.fill(area.description[0].value)
        return area


def eat(subject, area):
    global hung
    global inv
    if subject in inv:
        print "You eat the " + subject + "."
        hung += 1
        inv.remove(subject)
        if hung == 10:
            print "You are completely stuffed! With a full belly and your wits about you, you leave the city.  You win! \n"
            entry = raw_input("Enter your name to be enshrined in the Hall of Fame!\n")
            fo = open('hof.txt', 'w')
            fo.write(entry)
            fo.close()
            return False
        else:
            return area

    else:
        print "You can't eat that."
        return area


def play_again(current_area):
    x = raw_input("You are dead, play again? (Y/N)")
    x = x.lower()
    global inv
    if x == 'y':
        inv = []
        main()
    else:
        print "\n What a quitter. Your parents must be so proud."
        time.sleep(5)
        return False

if __name__ == "__main__":
    main()

# desc = game_map.area[0].description[0].value
# #print desc
# desc = desc.replace('\n', '')
# desc = textwrap.fill(desc)
# print desc
