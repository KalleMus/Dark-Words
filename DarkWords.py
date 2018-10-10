#import os
import random
import time
import sys
import sqlite3
#RootPath='/storage/emulated/0/com.hipipal.qpyplus'
#db = sqlite3.connect(os.path.join(RootPath,'rpg.db'))
db = sqlite3.connect('rpg.db')
cur = db.cursor()

#Slow printer for a dramatic effect.
def slow_print04(text):
    for c in text:
        time.sleep(0.4)
        print(c, end='')
        sys.stdout.flush()

def slow_print01(text):
    for c in text:
        time.sleep(0.03)
        print(c, end='')
        sys.stdout.flush()

def mainMenu():
    print('______  ___  ______ _   __  _    _  _________________  _____ '),slp02()
    print('|  _  \/ _ \ | ___ \ | / / | |  | ||  _  | ___ \  _  \/  ___|'),slp02()
    print('| | | / /_\ \| |_/ / |/ /  | |  | || | | | |_/ / | | |\ `--. '),slp02()
    print('| | | |  _  ||    /|    \  | |/\| || | | |    /| | | | `--. \''),slp02()
    print('| |/ /| | | || |\ \| |\  \ \  /\  /\ \_/ / |\ \| |/ / /\__/ /'),slp02()
    print('|___/ \_| |_/\_| \_\_| \_/  \/  \/  \___/\_| \_|___/  \____/ '),slp02()
    menuloop = 1
    while menuloop == 1:
        action = input('New game or Load game.')
        action.lower()
        global Gcurrent_location
        if action == 'new game' or action == 'new':
            db.rollback()
            create_table()
            data_entry()
            #Gcurrent_location = LocationFetch()
            Gcurrent_location = 'cell'
            print('\n' * 100)
            MainGameLoop()
        elif action == 'load game' or action == 'load':
            cur.execute("SELECT count(*) FROM sqlite_master WHERE Type = 'table' AND name='Player'")
            for row in cur.fetchall():
                load = row[0]
            if load == 1:
                Gcurrent_location = LocationFetch()
                if Gcurrent_location == 'empty':
                    print('No previous save to load.')
                else:
                    print('\n' * 5)
                    MainGameLoop()
            else:
                print('No previous save to load.')
        elif action == 'quit':
            exit()

def victory():
    print('\n'*100)
    slow_print01('The last lord has fallen and the curse has been lifted.'),slp2(),print()
    slow_print01('You can see life growing rapidly everywhere and the sun shining bright.'),slp2(),print()
    slow_print01('Let\'s hope everything is going to be well in this new world.'),slp2(),slp2(),print()
    slow_print01(' _   _ _____ _____ _____ _____________   __'),print()
    slow_print01('| | | |_   _/  __ \_   _|  _  | ___ \ \ / /'),print()
    slow_print01('| | | | | | | /  \/ | | | | | | |_/ /\ V / '),print()
    slow_print01('| | | | | | | |     | | | | | |    /  \ /  '),print()
    slow_print01('\ \_/ /_| |_| \__/\ | | \ \_/ / |\ \  | |  '),print()
    slow_print01(' \___/ \___/ \____/ \_/  \___/\_| \_| \_/  '),print()
    print('Thank you for playing!')
    print('This game was made by Kalle Mustonen on Python 3.4.4.')
    input('Press enter to continue...')
    print('\n' * 100)
    db.rollback()
    mainMenu()


def gameOver():
    global Gcurrent_location
    print('__   _______ _   _  ______ _____ ___________ '),slp02()
    print('\ \ / /  _  | | | | |  _  \_   _|  ___|  _  \''),slp02()
    print(' \ V /| | | | | | | | | | | | | | |__ | | | |'),slp02()
    print('  \ / | | | | | | | | | | | | | |  __|| | | |'),slp02()
    print('  | | \ \_/ / |_| | | |/ / _| |_| |___| |/ / '),slp02()
    print('  \_/  \___/ \___/  |___/  \___/\____/|___/  '),slp02()
    input('Press enter to continue...')
    print('\n'*100)
    cur.execute("SELECT Bonfire FROM Player WHERE ID = 1")
    for row in cur:
        Gcurrent_location = row[0]
    cur.execute("UPDATE Enemy SET Available = 1 WHERE Name IS NOT 'Red Dragon'")
    cur.execute("UPDATE Enemy SET HP = MaxHP")
    cur.execute("UPDATE Boss SET HP = MaxHP")
    cur.execute("UPDATE Player SET HP = MaxHP")
    cur.execute("UPDATE Player SET Estus = 3 WHERE ID = 1")
    MainGameLoop()

#Time sleep1
def slp05():
    time.sleep(0.5)

#Time sleep2
def slp1():
    time.sleep(1)

#Time sleep3
def slp2():
    time.sleep(2)

#Time sleep4
def slp02():
    time.sleep(0.3)

#Current location fetch:
def LocationFetch():
    Location = 'cell'
    cur.execute("SELECT Location FROM Player WHERE ID = 1")
    for row in cur:
        Location = row[0]
    return Location

def mapPrint(current_location):
    cur.execute("SELECT Room1 FROM Location WHERE ID ='" + current_location + "'")
    for row in cur:
        print(row[0])
    cur.execute("SELECT Room2 FROM Location WHERE ID ='" + current_location + "'")
    for row in cur:
        print(row[0])
    cur.execute("SELECT Room3 FROM Location WHERE ID ='" + current_location + "'")
    for row in cur:
        print(row[0])
    return


#Location DB update
def LocationUpdate(Gcurrent_location):
    cur.execute("UPDATE Player SET Location = '" + Gcurrent_location + "'")
    return

#Help
def help():
    print('Basic controls:')
    print('Movement: n, e, w, s to move north, east, west or south.')
    print('Interaction: examine, look around, take, equip, unequip, drop and i/inventory are the basics to let you get started.')
    print('Be sure to pay attention to your surroundings and pay very close attention to words with Capital letters.')
    print('Tip: examine everything!')
    print('Basic enemy encounter: c/combat, a/avoid and e/examine.')
    print('Basic combat: a/attack, f/flee and h/heal.')
    return

#Bonfire Rest
def bonfire(Gcurrent_location):
    bf = ''
    cur.execute("SELECT Location FROM Bonfire WHERE Location ='" + Gcurrent_location + "'AND Available = 1")
    for row in cur:
        bf = row[0]
    if len(bf) > 1:
        cur.execute("UPDATE Player SET Bonfire = '" + bf + "'WHERE ID = 1")
        cur.execute("UPDATE Enemy SET Available = 1 WHERE Name IS NOT 'Red Dragon'")
        cur.execute("UPDATE Enemy SET HP = MaxHP")
        cur.execute("UPDATE Boss SET HP = MaxHP")
        cur.execute("UPDATE Player SET Estus = 3 WHERE ID = 1")
        cur.execute("UPDATE Player SET HP = MaxHP")
        print('You Rested at the Bonfire.')
        LocationUpdate(Gcurrent_location)
        db.commit()
        print('Game saved.')
    return

#ENEMY.....................................
#EnemyNameFech
def FetchEnemyName(current_location):
    name = ''
    cur.execute("SELECT Name FROM Enemy WHERE Location='" + current_location + "'AND Available = 1")
    for row in cur.fetchall():
        name = row[0]
    return name

#EnemyDescFetch
def FetchEnemyDesc(current_location,target):
    desc = ''
    cur.execute("SELECT Description FROM Enemy WHERE Location='" + current_location + "'AND Available = 1 AND Name ='" + target + "'")
    for row in cur.fetchall():
        desc = row[0]
    return desc

#Enemy HP Fetch
def EnemyHPfetch(current_location,enemy):
    EnemyHP = 0
    cur.execute("SELECT HP FROM Enemy WHERE Name ='" + enemy + "'AND Location ='" + current_location + "'")
    for row in cur:
        EnemyHP = row[0]
    return EnemyHP


#Enemy Attack Fetch
def EnemyAttackFetch(current_location,enemy):
    EnemyAttack = 0
    cur.execute("SELECT Attack FROM Enemy WHERE Name ='" + enemy + "'AND Location ='" + current_location + "'")
    for row in cur:
        EnemyAttack = row[0]
    return EnemyAttack

#Enemy Accuracy Fetch
def EnemyAccuracyFetch(current_location,enemy):
    EnemyAccuracy = 0
    cur.execute("SELECT Accuracy FROM Enemy WHERE Name ='" + enemy + "'AND Location ='" + current_location + "'")
    for row in cur:
        EnemyAccuracy = row[0]
    return EnemyAccuracy

#Enemy Dodge Fetch
def EnemyDodgeFetch(current_location,enemy):
    EnemyDodge = 0
    cur.execute("SELECT Dodge FROM Enemy WHERE Name ='" + enemy + "'AND Location ='" + current_location + "'")
    for row in cur:
        EnemyDodge = row[0]
    return EnemyDodge

#BOSS..........................................
#BossNameFech
def FetchBossName(current_location):
    name = ''
    cur.execute("SELECT Name FROM Boss WHERE Location='" + current_location + "'AND Available = 1")
    for row in cur.fetchall():
        name = row[0]
    return name

#BossDescFetch
def FetchBossDesc(current_location,target):
    desc = ''
    cur.execute("SELECT Description FROM Boss WHERE Location='" + current_location + "'AND Available = 1 AND Name ='" + target + "'")
    for row in cur.fetchall():
        desc = row[0]
    return desc

#Boss HP Fetch
def BossHPfetch(current_location,boss):
    cur.execute("SELECT HP FROM Boss WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
    for row in cur:
        BossHP = row[0]
    return BossHP

#Boss MaxHP Fetch
def BossMaxHPfetch(current_location,boss):
    cur.execute("SELECT MaxHP FROM Boss WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
    for row in cur:
        BossHP = row[0]
    return BossHP

#Boss Attack Fetch
def BossAttackFetch(current_location,boss):
    cur.execute("SELECT Attack FROM Boss WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
    for row in cur:
        BossAttack = row[0]
    return BossAttack

#Boss Accuracy Fetch
def BossAccuracyFetch(current_location,boss):
    cur.execute("SELECT Accuracy FROM Boss WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
    for row in cur:
        BossAccuracy = row[0]
    return BossAccuracy

#Boss Dodge Fetch
def BossDodgeFetch(current_location,boss):
    cur.execute("SELECT Dodge FROM Boss WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
    for row in cur:
        BossDodge = row[0]
    return BossDodge

#PLAYER...........................................
#Player HP Fetch
def PlayerHPfetch():
    cur.execute("SELECT HP FROM Player WHERE ID = 1")
    for row in cur:
        PlayerHP = row[0]
    return PlayerHP

#Player Max HP Fetch
def PlayerMaxHPfetch():
    cur.execute("SELECT MaxHP FROM Player WHERE ID = 1")
    for row in cur:
        MaxHP = row[0]
    return MaxHP

#Player HP Add
def PlayerHPAdd(Ammount):
    HP=PlayerHPfetch()
    MaxHP=PlayerMaxHPfetch()
    if HP + Ammount > MaxHP:
        newHP = 100
        cur.execute("UPDATE Player SET HP ='" + str(newHP) + "'")
    else:
        newHP = HP + Ammount
        cur.execute("UPDATE Player SET HP ='" + str(newHP) + "'")
    return

def estusAmmountPrint():
    cur.execute("SELECT Estus FROM Player WHERE ID = 1")
    for row in cur:
        count1 = row[0]
    if count1 >= 1:
        cur.execute("SELECT Estus FROM Player WHERE ID = 1")
        for row in cur.fetchall():
            print(' Estus: ' + str(row[0]) + 'pc')
    else:
        print(' Estus: 0pc')
    return

#Insight Equipped
def insightEquipped():
    name = ''
    cur.execute("SELECT Name FROM Helmet WHERE Equipped = 1 AND PlayerID = 1")
    for row in cur:
        name = row[0]
    if name == 'insight':
        return 1
    else:
        return 0

#Player Damage Fetch
def PlayerDamageFetch():
    cur.execute("SELECT Attack FROM Weapon WHERE Equipped = 1")
    for row in cur:
        Attack = row[0]
    return Attack

#Player Accuracy Fetch
def PlayerAccuracyFetch():
    cur.execute("SELECT Accuracy FROM Weapon WHERE Equipped = 1")
    for row in cur:
        Accuracy = row[0]
    return Accuracy

#Player Block Fetch
def PlayerBlockFetch():
    Block = 0
    cur.execute("SELECT Block FROM Shield Where Equipped = 1")
    for row in cur:
        Block = row[0]
    return Block

#Player Armor Fetch
def PlayerArmorFetch():
    armor = 0
    helmet = 0
    cur.execute("SELECT armor FROM Armor WHERE Equipped = 1")
    for row in cur:
        armor = row[0]
    cur.execute("SELECT helmet FROM Helmet WHERE Equipped = 1")
    for row in cur:
        helmet = row[0]
    fullArmor = armor + helmet
    return fullArmor

#Gold Fetch
def GoldFetch():
    cur.execute("SELECT Gold FROM Player")
    for row in cur:
        currentGold = row[0]
    return currentGold

#Gold Add
def GoldAdd(gold):
    print('You got',gold,'gold.')
    currentGold = GoldFetch()
    newGold = currentGold + gold
    cur.execute("UPDATE Player SET Gold ='" + str(newGold) +"'")
    return

#Gold Loss
def GoldLoss(gold):
    print('You lost',gold,'gold.')
    currentGold = GoldFetch()
    newGold = currentGold - gold
    cur.execute("UPDATE Player SET Gold ='" + str(newGold) +"'")
    return

#MoveFecth
def MoveFetch(current_location,direction):
    destination = ''
    cur.execute("SELECT Destination FROM Passage WHERE Direction='" + direction + "' AND Source='" + current_location + "' AND Locked = 0")
    for row in cur.fetchall():
        destination = row[0]
    return destination

#ObjectDescFetch
def FetchObjectDesc(current_location,target):
    desc = ''
    cur.execute("SELECT Description FROM Object WHERE (Location='" + current_location + "'AND Available = 1 AND Name ='" + target + "')OR (PlayerID = 1 AND Available = 0 AND Name ='"+target+"')")
    for row in cur.fetchall():
        desc = row[0]
    return desc

#ObjectAvailableFetch
def FetchObjAvailable(current_location,target):
    available = 0
    cur.execute("SELECT Available FROM Object WHERE Location ='" + current_location + "'AND Available = 1 AND Name = '"+target+"'")
    for row in cur.fetchall():
        available = row[0]
    return available

'''
#WeaponAvailableFecth
def FetchWpnAvailable(current_location,target):
    available = 0
    cur.execute("SELECT Available FROM Weapon WHERE Location ='" + current_location + "'AND Available = 1 AND Name = '" + target + "'")
    for row in cur.fetchall():
        available = row[0]
    return available


#WeaponDetailsFetch
def FetchWpnDetails(current_location):
    details = ''
    cur.execute("SELECT Details FROM Weapon WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur.fetchall():
        details = row[0]
    return details
'''

#ObjecDetailsFetch
def FetchObjDetails():
    details = ''
    cur.execute("SELECT Details FROM Object WHERE PlayerID = 1")
    for row in cur.fetchall():
        details = row[0]
    return details

#WeaponGearDetailsFetch
def FetchWeaponGearDetails():
    details = ''
    cur.execute("SELECT Details FROM Weapon WHERE PlayerID = 1 AND Equipped = 0 AND Name IS NOT 'fists'")
    for row in cur.fetchall():
        details = row[0]
    return details

#ShieldGearDetailsFetch
def FetchShieldGearDetails():
    details = ''
    cur.execute("SELECT Details FROM Shield WHERE PlayerID = 1 AND Equipped = 0")
    for row in cur.fetchall():
        details = row[0]
    return details

#HelmetGearDetailsFetch
def FetchHelmetGearDetails():
    details = ''
    cur.execute("SELECT Details FROM Helmet WHERE PlayerID = 1 AND Equipped = 0")
    for row in cur.fetchall():
        details = row[0]
    return details

#ArmorGearDetailsFetch
def FetchArmorGearDetails():
    details = ''
    cur.execute("SELECT Details FROM Armor WHERE PlayerID = 1 AND Equipped = 0")
    for row in cur.fetchall():
        details = row[0]
    return details

#EquippedWeaponFetch
def FetchEquipWpnDetails():
    details = ''
    cur.execute("SELECT Details FROM Weapon WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        details = row[0]
    return details

#EquippedShieldFetch
def FetchEquipShieldDetails():
    details = ''
    cur.execute("SELECT Details FROM Shield WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        details = row[0]
    return details

#EquippedHelmetFetch
def FetchEquipHelmetDetails():
    details = ''
    cur.execute("SELECT Details FROM Helmet WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        details = row[0]
    return details

#EquippedArmorFetch
def FetchEquipArmorDetails():
    details = ''
    cur.execute("SELECT Details FROM Armor WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        details = row[0]
    return details

#WpnEquipped
def FetchEquipWpn():
    equipped = 0
    cur.execute("SELECT Equipped FROM Weapon WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        equipped = row[0]
    return equipped

#ShieldEquipped
def FetchEquipShield():
    equipped = 0
    cur.execute("SELECT Equipped FROM Shield WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        equipped = row[0]
    return equipped

#HelmetEquipped #Maybe USELESS???
def FetchEquipHelmet():
    equipped = 0
    cur.execute("SELECT Equipped FROM Helmet WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        equipped = row[0]
    return equipped

#ArmorEquipped #Maybe USELESS???
def FetchEquipArmor():
    equipped = 0
    cur.execute("SELECT Equipped FROM Armor WHERE PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        equipped = row[0]
    return equipped

#Inventory.
def inventory():
    print('HP: ' + str(PlayerHPfetch()) +'/'+ str(PlayerMaxHPfetch()))
    print('Gold: ' + str(GoldFetch()))
    cur.execute("SELECT PlayerID FROM Object WHERE Name = 'scroll'")
    for row in cur:
        scroll = row[0]
    if scroll == 1:
        cur.execute("SELECT Available, Available, Available, Available FROM Boss")
        for row in cur:
            oldGiant = row[0]
            pharaohKing = row[1]
            sandwormQueen = row[2]
            smolderingDragon = row[3]
        if oldGiant == 1:
            oldGiant = ' '
        else:
            oldGiant = 'x'
        if pharaohKing == 1:
            pharaohKing = ' '
        else:
            pharaohKing = 'x'
        if sandwormQueen == 1:
            sandwormQueen = ' '
        else:
            sandwormQueen = 'x'
        if smolderingDragon == 1:
            smolderingDragon = ' '
        else:
            smolderingDragon = 'x'
        #print('Old Giant [' + oldGiant + '] Pharaoh King [' + pharaohKing + '] Sandworm Queen [' + sandwormQueen + '] Smoldering Dragon [' + smolderingDragon + ']')

    cur.execute("SELECT Estus FROM Player WHERE ID = 1")
    for row in cur:
        count1 = row[0]
    if count1 >= 1:
        cur.execute("SELECT Estus FROM Player WHERE ID = 1")
        for row in cur.fetchall():
            print('Estus: ' + str(row[0]) + 'pc.')

    count2 = len(FetchObjDetails())
    if count2 >= 1:
        print('Items:')
        cur.execute("SELECT Details FROM Object WHERE PlayerID = 1")
        for row in cur.fetchall():
            print('-',row[0])
        for row in cur.fetchall():
            print('-',row[1])
        for row in cur.fetchall():
            print('-',row[2])
        for row in cur.fetchall():
            print('-',row[3])

    count3 = len(FetchWeaponGearDetails())
    if count3 >= 1:
        print('Gear:')
        cur.execute("SELECT Details, Attack, Accuracy FROM Weapon WHERE PlayerID = 1 AND Equipped = 0 AND Name IS NOT 'fists'")
        for row in cur.fetchall():
            print('-', row[0] + ': Att[' + str(row[1]) + '] Acc[' + str(row[2]) + '0]')
    count4 = len(FetchShieldGearDetails())
    if count4 >= 1:
        if count3 == 0:
            print('Gear:')
        cur.execute("SELECT Details, Block FROM Shield WHERE PlayerID = 1 AND Equipped = 0")
        for row in cur.fetchall():
            print('-', row[0] + ': Block[' + str(row[1]) + '0]')
    count5 = len(FetchHelmetGearDetails())
    if count5 >= 1:
        if count3 == 0 and count4 == 0:
            print('Gear:')
        cur.execute("SELECT Details, Helmet FROM Helmet WHERE PlayerID = 1 AND Equipped = 0")
        for row in cur.fetchall():
            print('-', row[0] + ': Armor[' + str(row[1]) + ']')
    count6 = len(FetchArmorGearDetails())
    if count6 >= 1:
        if count3 == 0 and count4 == 0 and count5 == 0:
            print('Gear:')
        cur.execute("SELECT Details, Armor FROM Armor WHERE PlayerID = 1 AND Equipped = 0")
        for row in cur.fetchall():
            print('-', row[0] + ': Armor[' + str(row[1]) + ']')

    count7 = len(FetchEquipWpnDetails())
    if count7 >= 1:
        print('Equipped:')
        cur.execute("SELECT Details, Attack, Accuracy FROM Weapon WHERE PlayerID = 1 AND Equipped = 1")
        for row in cur.fetchall():
            print('- Weapon: ', row[0] + ': Att[' + str(row[1]) + '] Acc[' + str(row[2]) + '0]')
        cur.execute("SELECT Details, Block FROM Shield WHERE PlayerID = 1 AND Equipped = 1")
        for row in cur.fetchall():
            print('- Shield: ', row[0] + ': Blk[' + str(row[1]) + '0]')
        cur.execute("SELECT Details, Helmet FROM Helmet WHERE PlayerID = 1 AND Equipped = 1")
        for row in cur.fetchall():
            print('- Helmet: ', row[0] + ': Armor[' + str(row[1]) + ']')
        cur.execute("SELECT Details, Armor FROM Armor WHERE PlayerID = 1 AND Equipped = 1")
        for row in cur.fetchall():
            print('- Armor: ', row[0] + ': Armor[' + str(row[1]) + ']')
    return

#Drink................................................
def drink(target):
    cur.execute("SELECT Estus FROM Player WHERE ID = 1")
    for row in cur:
        currentEstus = row[0]
    if currentEstus > 0:
        print('You drank one Estus, restoring your HP by 50 points.'),slp1()
        currentEstus = currentEstus - 1
        cur.execute("UPDATE Player SET Estus ='" + str(currentEstus) + "'WHERE ID = 1")
        PlayerHPAdd(50)
    else:
        print('You are out of Estus.')


#Equip.....................................................................................
def equip(target):
    WID = 0
    SID = 0
    HID = 0
    AID = 0
    cur.execute("SELECT PlayerID FROM Weapon WHERE Name = '"+ target + "' AND PlayerID = 1 AND Equipped = 0")
    for row in cur:
        WID = row[0]
    if WID == 1:
        cur.execute("UPDATE Weapon SET Equipped = 0 WHERE Equipped = 1")
        cur.execute("UPDATE Weapon SET Equipped = 1 WHERE Name = '" + target + "'")
        print('You equipped the: ' + FetchEquipWpnDetails())
        zweihanderEquipName = FetchEquipWpnDetails()
        shieldUnequip = FetchEquipShield()
        shieldUnequipName = FetchEquipShieldDetails()
        if zweihanderEquipName == 'Zweihander' and shieldUnequip == 1:
            cur.execute("UPDATE Shield SET Equipped = 0 WHERE Equipped = 1")
            print(shieldUnequipName + ' unequipped.')


    cur.execute("SELECT PlayerID FROM Shield WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 0")
    for row in cur.fetchall():
        SID = (row[0])
    if SID == 1:
        cur.execute("UPDATE Shield SET Equipped = 0 WHERE Equipped = 1")
        cur.execute("UPDATE Shield SET Equipped = 1 WHERE Name = '" + target + "'")
        print('You equipped the: ' + FetchEquipShieldDetails())
        zweihanderUnequip = FetchEquipWpn()
        zweihanderUnequipName = FetchEquipWpnDetails()
        if zweihanderUnequipName == 'Zweihander' and zweihanderUnequip == 1:
            cur.execute("UPDATE Weapon SET Equipped = 0 WHERE Equipped = 1")
            print(zweihanderUnequipName + ' unequipped.')

    cur.execute("SELECT PlayerID FROM Helmet WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 0")
    for row in cur:
        HID = row[0]
    if HID == 1:
        cur.execute("UPDATE Helmet SET Equipped = 0 WHERE Equipped = 1")
        cur.execute("UPDATE Helmet SET Equipped = 1 WHERE Name = '" + target + "'")
        print('You equipped the: ' + FetchEquipHelmetDetails())

    cur.execute("SELECT PlayerID FROM Armor WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 0")
    for row in cur:
        AID = row[0]
    if AID == 1:
        cur.execute("UPDATE Armor SET Equipped = 0 WHERE Equipped = 1")
        cur.execute("UPDATE Armor SET Equipped = 1 WHERE Name = '" + target + "'")
        print('You equipped the: ' + FetchEquipArmorDetails())

    if WID == 0 and SID == 0 and AID == 0 and HID == 0:
        print('You don\'t have ' + target + ' to equip.')
    return

#Unequip.....................................
def unequip(target):
    WID = 0
    SID = 0
    HID = 0
    AID = 0
    if target == 'fists':
        print('You can\'t unequip your fists.')
        return
    #WEAPON..............
    cur.execute("SELECT PlayerID FROM Weapon WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        WID = (row[0])
    if WID == 1:
        print('You unequipped the: ' + FetchEquipWpnDetails())
        cur.execute("UPDATE Weapon SET Equipped = 0 WHERE Equipped = 1")
        cur.execute("UPDATE Weapon SET Equipped = 1 WHERE Name = 'fists'")
    #SHIELD..............
    cur.execute("SELECT PlayerID FROM Shield WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        SID = (row[0])
    if SID == 1:
        print('You unequipped the: ' + FetchEquipShieldDetails())
        cur.execute("UPDATE Shield SET Equipped = 0 WHERE Equipped = 1")
    #HELMET.................
    cur.execute("SELECT PlayerID FROM Helmet WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        HID = (row[0])
    if HID == 1:
        print('You unequipped the: ' + FetchEquipHelmetDetails())
        cur.execute("UPDATE Helmet SET Equipped = 0 WHERE Equipped = 1")
    #ARMOR.................
    cur.execute("SELECT PlayerID FROM Armor WHERE Name = '" + target + "' AND PlayerID = 1 AND Equipped = 1")
    for row in cur.fetchall():
        AID = (row[0])
    if AID == 1:
        print('You unequipped the: ' + FetchEquipArmorDetails())
        cur.execute("UPDATE Armor SET Equipped = 0 WHERE Equipped = 1")
    if WID == 0 and SID == 0 and HID == 0 and AID == 0:
        print('You don\'t have ' + target + ' unequip.')
    return


#Drop......................................................................................
def drop(current_location,target):
    details = ''
    #WEAPON
    cur.execute("UPDATE Weapon SET Location = '" + current_location + "',PlayerID = 0, Available = 1 WHERE Name ='" + target + "'AND PlayerID = 1 AND Equipped = 0")
    cur.execute("SELECT Details FROM Weapon WHERE Name = '" + target + "'AND PlayerID = 0 AND Equipped = 0 AND Location ='" + current_location + "'")
    for row in cur:
        print('You dropped the ' + row[0] + '.')
        details = row[0]
    #SHIELD
    cur.execute("UPDATE Shield SET Location = '" + current_location + "',PlayerID = 0, Available = 1 WHERE Name ='" + target + "'AND PlayerID = 1 AND Equipped = 0")
    cur.execute("SELECT Details FROM Shield WHERE Name = '" + target + "'AND PlayerID = 0 AND Equipped = 0 AND Location ='" + current_location + "'")
    for row in cur:
        print('You dropped the ' + row[0] + '.')
        details = row[0]
    #HELMET
    cur.execute("UPDATE Helmet SET Location = '" + current_location + "',PlayerID = 0, Available = 1 WHERE Name ='" + target + "'AND PlayerID = 1 AND Equipped = 0")
    cur.execute("SELECT Details FROM Helmet WHERE Name = '" + target + "'AND PlayerID = 0 AND Equipped = 0 AND Location ='" + current_location + "'")
    for row in cur:
        print('You dropped the ' + row[0] + '.')
        details = row[0]
    #ARMOR
    cur.execute("UPDATE Armor SET Location = '" + current_location + "',PlayerID = 0, Available = 1 WHERE Name ='" + target + "'AND PlayerID = 1 AND Equipped = 0")
    cur.execute("SELECT Details FROM Armor WHERE Name = '" + target + "'AND PlayerID = 0 AND Equipped = 0 AND Location ='" + current_location + "'")
    for row in cur:
        print('You dropped the ' + row[0] + '.')
        details = row[0]
    if len(details) <= 0:
        print('You can\'t drop ' + target + '.')
    return


#Examine....................................................................................
def examineObject(current_location,target):
    desc = ''

    #OBJECT
    cur.execute("SELECT Description FROM Object Where (Location ='" + current_location + "' AND Name = '" + target + "'AND Available = 1) OR (PlayerID = 1 AND Name ='" + target + "')")
    for row in cur:
        print(row[0])
        desc = row[0]
    if len(desc) <= 0:
        cur.execute("SELECT Desc2 FROM Object Where Location ='" + current_location + "' AND Name = '" + target + "'AND Available = 0 AND Takeable = 0")
        for row in cur:
            print(row[0])
            desc = row[0]
    #Bonfire
    if target == 'bonfire':
        cur.execute("SELECT Description FROM Bonfire Where Location ='" + current_location + "'")
        for row in cur:
            print(row[0])
            desc = row[0]
    #NPC
    cur.execute("SELECT Description FROM NPC Where Location ='" + current_location +"'AND Name ='" + target + "'")
    for row in cur:
        print(row[0])
        desc = row[0]
    #WEAPON
    cur.execute("SELECT Description FROM Weapon Where PlayerID = 1 AND Name ='" + target + "'AND Equipped = 0")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT DescGround FROM Weapon Where Location ='" + current_location + "' AND Name = '" + target + "'AND PlayerID = 0 AND Available = 1")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT Details, Attack, Accuracy FROM Weapon Where Name = '" + target + "'AND PlayerID = 1 AND Equipped = 1")
    for row in cur:
        print('-', row[0] + ': Att[' + str(row[1]) + '] Acc[' + str(row[2]) + '0]')
        desc = row[0]
    #SHIELD
    cur.execute("SELECT Description FROM Shield Where PlayerID = 1 AND Name ='" + target + "'AND Equipped = 0")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute(
        "SELECT DescGround FROM Shield Where Location ='" + current_location + "' AND Name = '" + target + "'AND PlayerID = 0 AND Available = 1")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute(
        "SELECT Details, Block FROM Shield Where Name = '" + target + "'AND PlayerID = 1 AND Equipped = 1")
    for row in cur:
        print('-', row[0] + ': Block[' + str(row[1]) + '0]')
        desc = row[0]
    #HELMET
    cur.execute("SELECT Description FROM Helmet Where PlayerID = 1 AND Name ='" + target + "'AND Equipped = 0")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT DescGround FROM Helmet Where Location ='" + current_location + "' AND Name = '" + target + "'AND PlayerID = 0 AND Available = 1")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT Details, Helmet FROM Helmet Where Name = '" + target + "'AND PlayerID = 1 AND Equipped = 1")
    for row in cur:
        print('-', row[0] + ': Armor[' + str(row[1]) + ']')
        desc = row[0]
    if target == 'insight' and insightEquipped() == 1:
        print('Effect: Gives more information about your enemies.')
    #ARMOR
    cur.execute("SELECT Description FROM Armor Where PlayerID = 1 AND Name ='" + target + "'AND Equipped = 0")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT DescGround FROM Armor Where Location ='" + current_location + "' AND Name = '" + target + "'AND PlayerID = 0 AND Available = 1")
    for row in cur:
        print(row[0])
        desc = row[0]
    cur.execute("SELECT Details, Armor FROM Armor Where Name = '" + target + "'AND PlayerID = 1 AND Equipped = 1")
    for row in cur:
        print('-', row[0] + ': Armor[' + str(row[1]) + ']')
        desc = row[0]
    #Estus
    cur.execute("SELECT Estus FROM Player WHERE ID = 1")
    estus = 0
    for row in cur:
        estus = row[0]
    if estus > 0 and target == 'estus':
        print('A small Estus that I could Drink to restore 50 hp.')
    if len(desc) <= 0:
        if estus == 0 and target == 'estus':
            print('You are out of ' + target + '. Rest at Bonfire for a refill.')
        elif target != 'estus':
            print('No ' + target + ' to examine.')

    return

#Enemy Examine........................................................................
def examineEnemy(current_location,target):
    desc = len(FetchEnemyDesc(current_location,target))
    if desc >= 1:
        print(FetchEnemyDesc(current_location,target))
        if insightEquipped() == 1:
            cur.execute("SELECT MaxHP, Attack, Accuracy, Dodge FROM Enemy WHERE Name ='" + target + "'AND Location = '" + current_location + "'")
            for row in cur.fetchall():
                print('Max HP['+ str(row[0]) + '] Att[' + str(row[1]) + '] Acc[' + str(row[2]) + '0] Dodge[' + str(row[3]) + '0]')
    slp1()
    return

#Take..................................................................................
def take(current_location,target):
    gold = 0
    details = ''
    PlayerID = 0
    #Gold
    '''
    if target == 'gold':
        cur.execute("SELECT Gold FROM Object WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1")
        for row in cur:
            gold = row[0]
            GoldAdd(gold)
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'container' AND Location = '" + current_location + "'")
        if gold == 0:
            print('No Gold to Take.')
        return
    '''
    #Object
    cur.execute("SELECT Details FROM Object WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1 AND PlayerID = 0 AND Takeable = 1")
    for row in cur:
        print('You took the ',row[0])
        details = row[0]
    if len(details) > 1:
        cur.execute("UPDATE Object SET Available = 0, PlayerID = 1, Takeable = 0 WHERE Name = '" + target + "'AND Location ='" + current_location + "'AND Takeable = 1")
        cur.execute("UPDATE Object SET Available = 0 WHERE Takeable = 0 AND Location ='" + current_location + "'AND Door = 0 AND Available = 1")

    #Weapon
    cur.execute("SELECT Details FROM Weapon WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1 AND PlayerID = 0")
    for row in cur:
        print('You took the ', row[0])
        details = row[0]
    cur.execute("UPDATE Weapon SET Available = 0, PlayerID = 1 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")

    #Shield
    cur.execute("SELECT Details FROM Shield WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1 AND PlayerID = 0")
    for row in cur:
        print('You took the ', row[0])
        details = row[0]
    cur.execute("UPDATE Shield SET Available = 0, PlayerID = 1 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")
    #Helmet
    cur.execute("SELECT Details FROM Helmet WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1 AND PlayerID = 0")
    for row in cur:
        print('You took the ', row[0])
        details = row[0]
    cur.execute("UPDATE Helmet SET Available = 0, PlayerID = 1 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")
    #Armor
    cur.execute("SELECT Details FROM Armor WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1 AND PlayerID = 0")
    for row in cur:
        print('You took the ', row[0])
        details = row[0]
    cur.execute("UPDATE Armor SET Available = 0, PlayerID = 1 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")
    '''
    #Consumable
    vial = ''
    cur.execute("SELECT Details FROM Consumable WHERE Location = '" + current_location + "'AND Name = '" + target + "'AND Available = 1")
    for row in cur:
        print('You took the:', row[0])
        details = row[0]
        vial = row[0]
    if vial == 'Health Vial':
        cur.execute("UPDATE Consumable SET Available = 0 WHERE Name = '" + target + "'AND Location ='" + current_location + "'")
        cur.execute("SELECT Vials FROM Player WHERE ID=1")
        for row in cur:
            vials = row[0]
        newVials = 1 + vials
        cur.execute("UPDATE Player SET Vials ='"+ str(newVials) + "'")
    if len(details) <= 0:
        print('No ' + target + ' to take.')
    '''
    return

def merchant(current_location):
    buyloop = 1
    gear1 = ''
    g1cost = 0
    gear2 = ''
    g2cost = 0
    print('Hello there stranger!')
    print('What are you buying?')
    while buyloop == 1:
        gold = GoldFetch()
        print('You have: ' + str(gold) + ' gold.')
        cur.execute("SELECT Gear1, G1cost FROM NPC Where Details = 'Merchant' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-',row[0],row[1],'gold.',end='')
                gear1 = row[0]
                g1cost = row[1]
                cur.execute("SELECT Armor FROM Armor WHERE Details ='" + gear1 + "'")
                for row in cur.fetchall():
                    print(' Armor[' + str(row[0]) + ']')
        cur.execute("SELECT Gear2, G2cost FROM NPC Where Details = 'Merchant' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-', row[0], row[1], 'gold.',end='')
                gear2 = row[0]
                g2cost = row[1]
                cur.execute("SELECT Attack, Accuracy FROM Weapon WHERE Details ='" + gear2 + "'")
                for row in cur.fetchall():
                    print(' Att[' + str(row[0]) + '] Acc[' + str(row[1]) + '0]')
        print('Write the item name you wan\'t to buy or type Leave.')
        action = input()
        action.lower()
        print('\n'*4)
        if action == 'leave' or action == 'l':
            MainGameLoop()
        elif action == gear1.lower() and gold >= g1cost:
            GoldLoss(g1cost)
            print('You bought ' + gear1)
            cur.execute("UPDATE Armor SET PlayerID = 1 WHERE Details = '" + gear1 + "'")
            cur.execute("UPDATE NPC SET Gear1 = '' WHERE Location ='" + current_location + "'")
        elif action == gear2.lower() and gold >= g2cost:
            GoldLoss(g2cost)
            print('You bought ' + gear2)
            cur.execute("UPDATE Weapon SET PlayerID = 1 WHERE Details = '" + gear2 + "'")
            cur.execute("UPDATE NPC SET Gear2 = '' WHERE Location ='" + current_location + "'")
        elif gold < g1cost or gold < g2cost:
            print('Not enough gold to buy '+ action)
        else:
            print('No '+ action + ' to buy.')

def pyromancer(current_location):
    buyloop = 1
    gear1 = ''
    g1cost = 0
    gear2 = ''
    g2cost = 0
    print('Hello there stranger!')
    print('Interested in Explosives?')
    while buyloop == 1:
        gold = GoldFetch()
        print('You have: ' + str(gold) + ' gold.')
        cur.execute("SELECT Gear1, G1cost FROM NPC Where Details = 'Pyromancer' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-', row[0], row[1], 'gold.',end='')
                gear1 = row[0]
                g1cost = row[1]
                cur.execute("SELECT Attack, Accuracy FROM Weapon WHERE Details ='" + gear1 + "'")
                for row in cur.fetchall():
                    print(' Att[' + str(row[0]) + '] Acc[' + str(row[1]) + '0]')
        cur.execute("SELECT Gear2, G2cost FROM NPC Where Details = 'Pyromancer' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-', row[0], row[1], 'gold.')
                gear2 = row[0]
                g2cost = row[1]
        print('Write the item name you wan\'t to buy or type Leave.')
        action = input()
        action.lower()
        print('\n' * 4)
        if action == 'leave' or action == 'l':
            MainGameLoop()
        elif action == gear1.lower() and gold >= g1cost:
            GoldLoss(g1cost)
            print('You bought ' + gear1)
            cur.execute("UPDATE Weapon SET PlayerID = 1 WHERE Details = '" + gear1 + "'")
            cur.execute("UPDATE NPC SET Gear1 = '' WHERE Location ='" + current_location + "'")
        elif action == gear2.lower() and gold >= g2cost:
            GoldLoss(g2cost)
            print('You bought ' + gear2)
            cur.execute("UPDATE Object SET PlayerID = 1 WHERE Details = '" + gear2 + "'")
            cur.execute("UPDATE NPC SET Gear2 = '' WHERE Location ='" + current_location + "'")
        elif gold < g1cost or gold < g2cost:
            print('Not enough gold to buy ' + action)
        else:
            print('No ' + action + ' to buy.')

def armorer(current_location):
    buyloop = 1
    gear1 = ''
    g1cost = 0
    gear2 = ''
    g2cost = 0
    print('Hello there stranger!')
    print('Interested in some armor?')
    while buyloop == 1:
        gold = GoldFetch()
        print('You have: ' + str(gold) + ' gold.')
        cur.execute("SELECT Gear1, G1cost FROM NPC Where Details = 'Armorer' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-', row[0], row[1], 'gold.', end='')
                gear1 = row[0]
                g1cost = row[1]
                cur.execute("SELECT Armor FROM Armor WHERE Details ='" + gear1 + "'")
                for row in cur.fetchall():
                    print(' Armor[' + str(row[0]) + ']')
        cur.execute("SELECT Gear2, G2cost FROM NPC Where Details = 'Armorer' AND Location ='" + current_location + "'")
        for row in cur:
            if len(row[0]) > 1:
                print('-', row[0], row[1], 'gold.', end='')
                gear2 = row[0]
                g2cost = row[1]
                cur.execute("SELECT Attack, Accuracy FROM Weapon WHERE Details ='" + gear2 + "'")
                for row in cur.fetchall():
                    print(' Att[' + str(row[0]) + '] Acc[' + str(row[1]) + '0]')
        print('Write the item name you wan\'t to buy or type Leave.')
        action = input()
        action.lower()
        print('\n' * 4)
        if action == 'leave' or action == 'l':
            MainGameLoop()
        elif action == gear1.lower() and gold >= g1cost:
            GoldLoss(g1cost)
            print('You bought ' + gear1)
            cur.execute("UPDATE Armor SET PlayerID = 1 WHERE Details = '" + gear1 + "'")
            cur.execute("UPDATE NPC SET Gear1 = '' WHERE Location ='" + current_location + "'")
        elif action == gear2.lower() and gold >= g2cost:
            GoldLoss(g2cost)
            print('You bought ' + gear2)
            cur.execute("UPDATE Weapon SET PlayerID = 1 WHERE Details = '" + gear2 + "'")
            cur.execute("UPDATE NPC SET Gear2 = '' WHERE Location ='" + current_location + "'")
        elif gold < g1cost or gold < g2cost:
            print('Not enough gold to buy ' + action)
        else:
            print('No ' + action + ' to buy.')


#Open..................................................................................
def open(current_location,target):
    if target == 'door': #Open lock
        ObjAvailable = FetchObjAvailable(current_location, target)
        if ObjAvailable >= 1:
            cur.execute("SELECT PlayerID FROM Object WHERE Details = 'Rusty Key'")
            for row in cur:
                key = row[0]
            if key == 1:
                cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = '" + current_location + "'")
                print('You opened the cell Door, but the rusty Key snapped in half.')
                cur.execute("UPDATE Object SET PlayerID = 0 WHERE Details = 'Rusty Key'")
                cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'door'")
        else:
            print('There\'s no ' + target + ' to open.')
    elif target == 'shutters':
        ObjAvailable = FetchObjAvailable(current_location, target)
        if ObjAvailable >= 1:
            cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = '" + current_location + "'")
            print('You opened the wooden Shutters. You can now jump North through the window. Its not a large drop.')
            cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'shutters'")
        else:
            print('Theres no ' + target + ' to open.')
    else:
        print('Theres no ',target,'to open.')
    return

def pullChains(current_location):
    chains = ''
    cur.execute("SELECT Name FROM Object WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        chains = row[0]
    if chains == 'chains':
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'cell3' AND Destination = 'celltombtop'")
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'celltombtop' AND Destination = 'cell3' ")
        if current_location == 'cell3':
            print('You Pulled from the Chains and a secret door opened to your East.')
        elif current_location == 'celltombtop':
            print('You Pulled from the Chains and a secret door opened to your West.')
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'chains'")

def pullLever(current_location):
    lever = ''
    cur.execute("SELECT Name FROM Object WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        lever = row[0]
    if lever == 'lever':
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'hallentry' AND Destination = 'hallout'")
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'hallout' AND Destination = 'hallentry' ")
        print('You Pulled from the Lever and the huge gate opened.')
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'lever'")

def cutTree(current_location):
    tree = ''
    hatchet = ''
    axe = ''
    cur.execute("SELECT Name FROM Weapon WHERE PlayerID = 1 AND Name = 'hatchet'")
    for row in cur:
        hatchet = row[0]
    cur.execute("SELECT Name FROM Weapon WHERE PlayerID = 1 AND Name = 'axe'")
    for row in cur:
        axe = row[0]
    cur.execute("SELECT Name FROM Object WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        tree = row[0]
    if tree == 'tree' and (hatchet == 'hatchet' or axe == 'axe'):
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'forestsoutheast' AND Destination = 'desertwest'")
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'desertwest' AND Destination = 'forestsoutheast' ")
        print('You Cut down The tree and opened up a new route.')
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'tree'")

def throwWhip(current_location):
    cur.execute("SELECT Name FROM Weapon WHERE PlayerID = 1")
    for row in cur:
        whip = row[0]
    if whip == 'whip' and current_location == 'forests':
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'forests' AND Destination = 'hallnorth'")
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'hallnorth' AND Destination = 'forests'")
        print('You threw the Whip onto the window. You can now climb South.')
    elif whip == 'whip' and current_location == 'mountain4':
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'mountain4' AND Destination = 'mountain5'")
        print('You threw the Whip onto the ledge. You can now climb South.')


def blowupBoulder(current_location):
    boulder = ''
    explosives = ''
    cur.execute("SELECT Name FROM Object WHERE PlayerID = 1 AND Name = 'explosives'")
    for row in cur:
        explosives = row[0]
    cur.execute("SELECT Name FROM Object WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        boulder = row[0]
    if boulder == 'boulder' and explosives == 'explosives':
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'mountain8' AND Destination = 'mountain7'")
        cur.execute("UPDATE Passage SET Locked = 0 WHERE Source = 'mountain7' AND Destination = 'mountain8'")
        cur.execute("UPDATE Object SET PlayerID = 0 WHERE Name = 'explosives'")
        print('You blew up the Boulder and opened up a new route.')
        cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'boulder'")

def readScroll(Gcurrent_location, target):
    scroll = 1
    cur.execute("SELECT PlayerID FROM Object WHERE Name = '" + target + "'")
    for row in cur:
        scroll = row[0]
    if scroll == 1 and target == 'scroll':
        slow_print01('An evil curse has fallen on to this land.'),print(),slp1()
        slow_print01('The curse has turned most of it\'s living creatures undead'),print()
        slow_print01('and those who avoided this fate must now survive in this horrible new world.'),print()
        print(),slp2()
        slow_print01('This evil curse is maintained by 4 lords that govern this land.'),print(),slp1()
        slow_print01('The Old Giant, lord of the forest.'),print(),slp1()
        slow_print01('The Sandworm Queen, lord of the desert.'),print(),slp1()
        slow_print01('The Pharaoh King, lord of the underworld.'),print(),slp1()
        slow_print01('The Smoldering Dragon, lord of the mountain.'),print()
        print(),slp2()
        slow_print01('An old prophecy says that one day a chosen undead will come and slay these lords'),print()
        slow_print01('and lift the curse from these lands.'),print(),slp1()
    return

#Combat................................................
def combat(current_location,enemy):
    print('\n'*100)
    print(' [Combat]')
    action = ''
    Attack = PlayerDamageFetch()
    Accuracy = PlayerAccuracyFetch()
    Block = PlayerBlockFetch()
    Armor = PlayerArmorFetch()
    EnemyAccuracy = EnemyAccuracyFetch(current_location,enemy)
    EnemyDodge = EnemyDodgeFetch(current_location,enemy)
    print('You are in a battle with: ' + enemy)
    while action != 'flee' or action != 'f':
        print()
        HP = PlayerHPfetch()
        EnemyHP = EnemyHPfetch(current_location, enemy)
        EnemyAttack = EnemyAttackFetch(current_location, enemy)
        print('[Player HP: '+str(HP)+']: ',end='')
        print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) +']',end='')
        estusAmmountPrint()
        print('[' + enemy + ' HP: ' + str(EnemyHP) + ']: ',end='')
        if insightEquipped() == 1:
            print('Att[' + str(EnemyAttack) + '] Acc[' + str(EnemyAccuracy) + '0] Dodge[' + str(EnemyDodge) + '0]')
        print('\n'*2)
        player_input = input('Attack/Flee/Heal: ')
        action = player_input.lower()
        if action == 'attack' or action == 'a':
            print('You attack with your',FetchEquipWpnDetails(),end=''),slow_print04('.'*4)
            hitChance = Accuracy - EnemyDodge
            hit = random.randint(1,10)
            if hit <= hitChance:
                critical = random.randint(1,10)
                if critical == 10:
                    print('Critical Hit! 2xdamage.'),slp05()
                    Edamage = int(EnemyHP) - int(Attack)*2
                    print('You dealt ' + str(Attack*2) + ' damage.'), slp1()
                else:
                    print('Hit!'),slp05()
                    Edamage = int(EnemyHP) - int(Attack)
                    print('You dealt ' + str(Attack) + ' damage.'), slp1()
                cur.execute("UPDATE Enemy Set HP ='"+ str(Edamage) +"'WHERE Location ='" + current_location + "'AND Name ='" + enemy + "'")
                EnemyHP = EnemyHPfetch(current_location, enemy)
                if EnemyHP <= 0:
                    print('The ' + enemy + ' died.'),slp1()
                    cur.execute("SELECT Gold FROM Enemy WHERE Location ='" + current_location + "'")
                    for row in cur.fetchall():
                        gold = row[0]
                    cur.execute("UPDATE Enemy Set Available = 0, Gold = 0 WHERE Name ='" + enemy + "'AND Location ='" + current_location + "'")
                    GoldAdd(gold)
                    slp1()
                    print('\n'*2)
                    MainGameLoop()
            else:
                miss = random.randint(1,3)
                if miss == 1:
                    print('you missed.'),slp1()
                elif miss == 2:
                    print('the ' + enemy + ' deflects your attack.'),slp1()
                else:
                    print('the ' + enemy + ' dodges your attack.'),slp1()

        elif action == 'flee' or action == 'f':
            mapPrint(current_location)
            cur.execute("SELECT Description FROM Location WHERE ID='" + current_location + "'")
            for row in cur:
                print(row[0])
            return
        elif action == 'heal' or action == 'h':
            target = 'estus'
            drink(target)
            HP = PlayerHPfetch()

        print(enemy+' attacks.',end=''),slow_print04('.'*4)
        Blocked = random.randint(1,10)
        if Blocked <= Block:
            print('you blocked the ' + enemy + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
        else:
            Enemyhit = random.randint(1,10)
            if Enemyhit <= EnemyAccuracy:
                print('Hit!'),slp05()
                print(enemy+' dealt '+ str(EnemyAttack) + ' damage to you.'),slp1()
                ArmorEquipped = FetchEquipArmor()
                HelmetEquipped = FetchEquipHelmet()
                if ArmorEquipped == 1 or HelmetEquipped == 1:
                    print('Your armor negated ' + str(Armor) + ' damage.')
                slp1()
                if EnemyAttack <= Armor:
                    EnemyAttack = 0
                EnemyAttack = EnemyAttack - Armor
                Pdamage = int(HP) - int(EnemyAttack)
                cur.execute("UPDATE Player Set HP ='"+ str(Pdamage) +"'")
                HP = PlayerHPfetch()
                if HP <= 0:
                    gameOver()
            else:
                miss = random.randint(1, 3)
                if miss == 1:
                    print('the ' + enemy + ' missed you.'), slp1()
                elif miss == 2:
                    print('you deflect the ' + enemy + '\'s attack.'), slp1()
                else:
                    print('you dodge the ' + enemy + '\'s attack.'), slp1()
    return

#Enemy encounter................................
def enemyEncounter(current_location):
    action = ''
    EnemyName = FetchEnemyName(current_location)
    EnemyAttack = EnemyAttackFetch(current_location,EnemyName)
    EnemyAccuracy = EnemyAccuracyFetch(current_location,EnemyName)
    Block = PlayerBlockFetch()
    Armor = PlayerArmorFetch()
    if len(EnemyName) >= 1:
        while action != 'avoid' or action != 'a':
            if len(EnemyName) >= 1:
                print('Enemies: ')
                print('-',EnemyName)
                print()
                player_input = input('Combat/Avoid/Examine?')
                action = player_input.lower()
                if action == 'combat' or action == 'c':
                    combat(current_location,EnemyName)
                elif action == 'examine' or action == 'e':
                    examineEnemy(current_location,EnemyName)
                elif action == 'avoid' or action == 'a':
                    print('The '+ EnemyName + ' attacks you while you try to avoid it',end=''),slow_print04('.'*4)
                    cur.execute("SELECT Attack FROM Enemy WHERE Location ='" + current_location + "'AND Available = 1")
                    for row in cur:
                        EnemyAttack = row[0]
                        EnemyAttack = EnemyAttack * 2
                    cur.execute("SELECT Accuracy FROM Enemy WHERE Name ='" + EnemyName + "'AND Location ='" + current_location + "'")
                    for row in cur:
                        EnemyAccuracy = row[0]
                    HP = PlayerHPfetch()
                    Blocked = random.randint(1, 10)
                    if Blocked <= Block:
                        print('you blocked the ' + EnemyName + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
                        print('You can now move freely.')
                        return
                    else:
                        Enemyhit = random.randint(1,10)
                        if Enemyhit <= EnemyAccuracy:
                            print(EnemyName + ' hits you critically.'),slp1()
                            print(EnemyName + ' dealt ' + str(EnemyAttack) + ' damage to you.'),slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if EnemyAttack <= Armor:
                                EnemyAttack = 0
                            EnemyAttack = EnemyAttack - Armor
                            Pdamage = int(HP) - int(EnemyAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            print(EnemyName + ' misses.'),slp1()
                        print('You can now move freely.')
                        return
                else:
                    print('Combat, Avoid or Examine.')
        return

#Boss Encouter............................
def BossEncounter(current_location):
    BossName = FetchBossName(current_location)
    if len(BossName) >= 1:
        target = BossName
        print(FetchBossDesc(current_location, target))
        if insightEquipped() == 1:
            cur.execute("SELECT Maxhp, Attack, Accuracy, Dodge FROM Boss WHERE Location = '" + current_location + "'AND Name ='" + BossName + "'")
        input('Press enter to start the fight...')
        if BossName == 'Old Giant':
            GiantBattle(current_location,BossName)
        elif BossName == 'Pharaoh King':
            PharaohBattle(current_location,BossName)
        elif BossName == 'Sandworm Queen':
            SandwormQueen(current_location, BossName)
        elif BossName == 'Smoldering Dragon':
            SmolderingDragon(current_location, BossName)

#Old Giant battle................................
def GiantBattle(current_location,boss):
    print('\n'*100)
    print(' [Boss]')
    action = ''
    Attack = PlayerDamageFetch()
    Accuracy = PlayerAccuracyFetch()
    Armor = PlayerArmorFetch()
    Block = PlayerBlockFetch()
    BossHP = BossHPfetch(current_location, boss)
    BossAccuracy = BossAccuracyFetch(current_location,boss)
    BossDodge = BossDodgeFetch(current_location,boss)
    print('You are in a battle with: ' + boss)
    while BossHP > 0:
        print()
        HP = PlayerHPfetch()
        BossHP = BossHPfetch(current_location, boss)
        BossAttack = BossAttackFetch(current_location, boss)
        print('[Player HP: '+str(HP)+'] ',end='')
        print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) + ']',end='')
        estusAmmountPrint()
        print('[' + boss + ' HP: ' + str(BossHP) + '] ',end='')
        if insightEquipped() == 1:
            cur.execute("SELECT Attack, Accuracy, Dodge FROM Boss WHERE Location = '" + current_location + "'AND Name ='" + boss + "'")
            for row in cur:
                print('Att[' + str(row[0]) + ' Acc[' + str(row[1]) + '0] Dodge[' + str(row[2]) + '0]')
        print('\n'*2)
        bossAction = random.randint(1,6)
        if bossAction == 1 or bossAction == 2:
            bossAction = 1
        elif bossAction == 3 or bossAction == 4:
            bossAction = 2
        else:
            bossAction = 3
        if bossAction == 1:
            print('The ' + boss + ' attacks you.',end=''),slow_print04('.'*4)
            while bossAction == 1:
                action = input('[Attack/Dodge/Run/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'run' or action == 'r' or action == 'heal' or action == 'h':
                    if action == 'attack' or action == 'a':
                        bossAction = 0
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.'),slp1()

                    elif action == 'run' or action == 'r':
                        bossAction = 0
                        print('You try to run',end=''),slow_print04('.'*4)

                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Blocked = random.randint(1, 10)
                    if Blocked <= Block:
                        print('You blocked the ' + boss + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
                    else:
                        Bosshit = random.randint(1, 10)
                        if Bosshit <= BossAccuracy:
                            print(boss + ' Hit\'s you!'), slp05()
                            print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if BossAttack <= Armor:
                                BossAttack = 0
                            BossAttack = BossAttack - Armor
                            Pdamage = int(HP) - int(BossAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            miss = random.randint(1, 3)
                            if miss == 1:
                                print('The ' + boss + ' missed you.'), slp1()
                            elif miss == 2:
                                print('You deflect the ' + boss + '\'s attack.'), slp1()
                            else:
                                print('You dodge the ' + boss + '\'s attack.'), slp1()

                elif action == 'dodge' or action == 'd':
                    bossAction = 0
                    dodgeFail = random.randint(1, 10)
                    if dodgeFail == 10:
                        print('You tried to dodge the attack, but it still hit you.'), slp1()
                        print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossAttack <= Armor:
                            BossAttack = 0
                        BossAttack = BossAttack - Armor
                        Pdamage = int(HP) - int(BossAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('You dodged the ' + boss + '\'s attack.'), slp1()

        if bossAction == 2:
            print('The ' + boss + ' does a huge attack.', end=''), slow_print04('.' * 4)
            while bossAction == 2:
                action = input('[Attack/Dodge/Run/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'dodge' or action == 'd' or action == 'heal' or action == 'h':
                    bossAction = 0
                    if action == 'attack' or action == 'a':
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(5, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(
                                Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.'),slp1()

                    elif action == 'dodge' or action == 'd':
                        if action == 'dodge' or action == 'd':
                            print('You try to dodge the ' + boss + '\'s attack',end=''),slow_print04('.'*4)
                    elif action == 'heal' or action == 'h':
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Bosshit = random.randint(1, 10)
                    if Bosshit <= BossAccuracy:
                        BossCriticalAttack = BossAttack * 2
                        print(boss + ' Hit\'s you critically!'), slp05()
                        print(boss + ' dealt ' + str(BossCriticalAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossCriticalAttack <= Armor:
                            BossCriticalAttack = 0
                        BossCriticalAttack = BossCriticalAttack - Armor
                        Pdamage = int(HP) - int(BossCriticalAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('The ' + boss + ' missed you.'), slp1()

                elif action == 'run' or action == 'r':
                    print('You ran far enough to avoid the ' + boss + '\'s attack.'), slp1()
                    bossAction = 0

        if bossAction == 3:
            print('The ' + boss + ' just stands there. Now\'s your chance!',end='')
            while bossAction == 3:
                action = input('[Attack/Dodge/Run/Heal]')
                action.lower()
                if action == 'run' or action == 'r' or action == 'dodge' or action == 'd' or action == 'heal' or action == 'h':
                    if action == 'run' or action == 'r':
                        bossAction = 0
                        print('You run away from the ' + boss + '\'s')
                    elif action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('Dodge nothing. A wasted opportunity.'),slp1()
                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                elif action == 'attack' or action == 'a':
                    print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                    hitChance = Accuracy - BossDodge
                    hit = random.randint(1, 10)
                    if hit <= hitChance:
                        critical = random.randint(1, 10)
                        if critical == 10:
                            print('Critical Hit! 2xdamage.'), slp05()
                            Bdamage = int(BossHP) - int(Attack) * 2
                            print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                        else:
                            print('Hit!'), slp05()
                            Bdamage = int(BossHP) - int(Attack)
                            print('You dealt ' + str(Attack) + ' damage.'), slp1()
                        cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                        BossHP = BossHPfetch(current_location, boss)
                        if BossHP <= 0:
                            cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                            for row in cur:
                                print(row[0]),slp2()
                            cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                            cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                            for row in cur.fetchall():
                                gold = row[0]
                            GoldAdd(gold)
                            slp1()
                            print('\n' * 2)
                            MainGameLoop()
                    else:
                        print('you missed.'),slp1()
                    bossAction = 0



#Pharaoh King battle................................
def PharaohBattle(current_location, boss):
    print('\n' * 100)
    print(' [Boss]')
    action = ''
    Attack = PlayerDamageFetch()
    Accuracy = PlayerAccuracyFetch()
    Armor = PlayerArmorFetch()
    Block = PlayerBlockFetch()
    BossHP = BossHPfetch(current_location, boss)
    BossMaxHP = BossMaxHPfetch(current_location,boss)
    BossAccuracy = BossAccuracyFetch(current_location, boss)
    BossDodge = BossDodgeFetch(current_location, boss)
    print('You are in a battle with: ' + boss)
    while BossHP > 0:
        print()
        HP = PlayerHPfetch()
        BossHP = BossHPfetch(current_location, boss)
        BossAttack = BossAttackFetch(current_location, boss)
        print('[Player HP: ' + str(HP) + '] ',end='')
        print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) + ']',end='')
        estusAmmountPrint()
        print('[' + boss + ' HP: ' + str(BossHP) + '] ',end='')
        if insightEquipped() == 1:
            cur.execute("SELECT Attack, Accuracy, Dodge FROM Boss WHERE Location = '" + current_location + "'AND Name ='" + boss + "'")
            for row in cur:
                print('Att[' + str(row[0]) + ' Acc[' + str(row[1]) + '0] Dodge[' + str(row[2]) + '0]')
        print('\n' * 2)
        bossAction = random.randint(1, 6)
        if bossAction == 1:
            bossAction = 1  #Minion
        elif bossAction == 2 or bossAction == 3:
            bossAction = 2  #Curse
        elif bossAction == 4:
            bossAction = 3  #Sit
        else:
            bossAction = 4  #Spear
        if bossAction == 1:
            print('The ' + boss + ' send\'s one of his minions at you.', end=''), slow_print04('.' * 4)
            cur.execute("UPDATE Enemy SET HP = MaxHP WHERE Location = 'king'")
            mummy = random.randint(1,2)
            if mummy == 1:
                mummy = 1
            if mummy == 1:
                enemy = 'Mummy'
            else:
                enemy = 'Mummy Soldier'
            while bossAction == 1:
                print('\n' * 2)
                print(' [Combat]')
                action = ''
                location = 'king'
                EnemyAccuracy = EnemyAccuracyFetch(location, enemy)
                EnemyDodge = EnemyDodgeFetch(location, enemy)
                print('You are in a battle with: ' + enemy)
                cur.execute("UPDATE Enemy SET Hp = MaxHP WHERE Location = 'king'")
                while (enemy == 'Mummy' or enemy == 'Mummy Soldier') and bossAction == 1:
                    print()
                    HP = PlayerHPfetch()
                    EnemyHP = EnemyHPfetch(location, enemy)
                    EnemyAttack = EnemyAttackFetch(location, enemy)
                    print('[Player HP: ' + str(HP) + ']: ', end='')
                    print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) + ']',end='')
                    estusAmmountPrint()
                    print('[' + enemy + ' HP: ' + str(EnemyHP) + ']: ', end='')
                    if insightEquipped() == 1:
                        print('Att[' + str(EnemyAttack) + '] Acc[' + str(EnemyAccuracy) + '0] Dodge[' + str(EnemyDodge) + '0]')
                    print('\n' * 2)
                    player_input = input('Attack/Heal: ')
                    action = player_input.lower()
                    if action == 'attack' or action == 'a':
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - EnemyDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Edamage = int(EnemyHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Edamage = int(EnemyHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Enemy Set HP ='" + str(Edamage) + "'WHERE Location = 'king' AND Name ='" + enemy + "'")
                            EnemyHP = EnemyHPfetch(location, enemy)
                            if EnemyHP <= 0:
                                bossAction = 0
                                print('The ' + enemy + ' died.'), slp1()
                                print('You attack the ' + boss + ' with your ' + FetchEquipWpnDetails(),end=''),slow_print04('.'*4)
                                Bdamage = int(BossHP) - int(Attack)
                                critical = random.randint(1, 10)
                                if critical == 10:
                                    print('Critical Hit! 2xdamage.'), slp05()
                                    Bdamage = int(BossHP) - int(Attack) * 2
                                    print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                                else:
                                    print('Hit!'), slp05()
                                    Bdamage = int(BossHP) - int(Attack)
                                    print('You dealt ' + str(Attack) + ' damage.'), slp1()
                                cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                                BossHP = BossHPfetch(current_location, boss)
                                if BossHP <= 0:
                                    cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                    for row in cur:
                                        print(row[0]),slp2()
                                    cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                    cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                    for row in cur.fetchall():
                                        gold = row[0]
                                    GoldAdd(gold)
                                    slp1()
                                    print('\n' * 2)
                                    MainGameLoop()


                        else:
                            miss = random.randint(1, 3)
                            if miss == 1:
                                print('you missed.'), slp1()
                            elif miss == 2:
                                print('the ' + enemy + ' deflects your attack.'), slp1()
                            else:
                                print('the ' + enemy + ' dodges your attack.'), slp1()

                    elif action == 'heal' or action == 'h':
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()
                    if bossAction == 1:
                        print(enemy + ' attacks.', end=''), slow_print04('.' * 4)
                        Blocked = random.randint(1, 10)
                        if Blocked <= Block:
                            print('you blocked the ' + enemy + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
                        else:
                            Enemyhit = random.randint(1, 10)
                            if Enemyhit <= EnemyAccuracy:
                                print('Hit!'), slp05()
                                print(enemy + ' dealt ' + str(EnemyAttack) + ' damage to you.'),slp1()
                                ArmorEquipped = FetchEquipArmor()
                                HelmetEquipped = FetchEquipHelmet()
                                if ArmorEquipped == 1 or HelmetEquipped == 1:
                                    print('Your armor negated ' + str(Armor) + ' damage.')
                                slp1()
                                if EnemyAttack <= Armor:
                                    EnemyAttack = 0
                                EnemyAttack = EnemyAttack - Armor
                                Pdamage = int(HP) - int(EnemyAttack)
                                cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                                HP = PlayerHPfetch()
                                if HP <= 0:
                                    gameOver()
                            else:
                                miss = random.randint(1, 3)
                                if miss == 1:
                                    print('the ' + enemy + ' missed you.'), slp1()
                                elif miss == 2:
                                    print('you deflect the ' + enemy + '\'s attack.'), slp1()
                                else:
                                    print('you dodge the ' + enemy + '\'s attack.'), slp1()

        if bossAction == 2:
            print('The ' + boss + ' casts a curse on you.',end=''),slow_print04('.' * 4)
            while bossAction == 2:
                action = input('[Attack/Dodge/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'heal' or action == 'h':
                    if action == 'attack' or action == 'a':
                        bossAction = 0
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.'),slp1()

                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()
                    elif action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('You try to dodge a curse?'),slp1()

                curseHit = random.randint(1,3)
                if curseHit == 1:
                    print('The curse didn\'t land.'),slp1()
                else:
                    CurseAttack = 20
                    print(boss + ' steals ' + str(CurseAttack) + ' life from you.'),slp1()
                    Pdamage = int(HP) - int(CurseAttack)
                    cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                    HP = PlayerHPfetch()
                    if HP <= 0:
                        gameOver()
                    if (CurseAttack + BossHP) > BossMaxHP:
                        cur.execute("UPDATE Boss SET HP = MaxHP WHERE Name = 'Pharaoh King'")
                    else:
                        BossLifeGain = BossHP + CurseAttack
                        cur.execute("UPDATE Boss SET HP = '" + str(BossLifeGain) + "'WHERE Name = 'Pharaoh King'")
                    print(boss + ' gained ' + str(CurseAttack) + ' life.'),slp1()

        if bossAction == 3:
            print('The ' + boss + ' sit\'s on his throne and laughs at you.')
            while bossAction == 3:
                action = input('[Attack/Dodge/Heal]')
                action.lower()
                if action == 'dodge' or action == 'd' or action == 'heal' or action == 'h':
                    if action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('You dodged nothing. A wasted opportunity.'),slp1()
                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                elif action == 'attack' or action == 'a':
                    bossAction = 0
                    print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                    hitChance = Accuracy - BossDodge
                    hit = random.randint(1, 10)
                    if hit <= hitChance:
                        critical = random.randint(1, 10)
                        if critical == 10:
                            print('Critical Hit! 2xdamage.'), slp05()
                            Bdamage = int(BossHP) - int(Attack) * 2
                            print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                        else:
                            print('Hit!'), slp05()
                            Bdamage = int(BossHP) - int(Attack)
                            print('You dealt ' + str(Attack) + ' damage.'), slp1()
                        cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                        BossHP = BossHPfetch(current_location, boss)
                        if BossHP <= 0:
                            cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                            for row in cur:
                                print(row[0]),slp2()
                            cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                            cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                            for row in cur.fetchall():
                                gold = row[0]
                            GoldAdd(gold)
                            slp1()
                            print('\n' * 2)
                            MainGameLoop()
                    else:
                        print('you missed.'),slp1()

        if bossAction == 4:
            print('The ' + boss + ' throws a spear at you.', end=''), slow_print04('.' * 4)
            while bossAction == 4:
                action = input('[Attack/Dodge/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'heal' or action == 'h':
                    if action == 'attack' or action == 'a':
                        bossAction = 0
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.'),slp1()


                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Blocked = random.randint(1, 10)
                    if Blocked <= Block:
                        print('You blocked the spear with your ' + FetchEquipShieldDetails() + '.'), slp1()
                    else:
                        Bosshit = random.randint(1, 10)
                        if Bosshit <= BossAccuracy:
                            print('The Spear Hit\'s you!'), slp05()
                            print('The spear dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if BossAttack <= Armor:
                                BossAttack = 0
                            BossAttack = BossAttack - Armor
                            Pdamage = int(HP) - int(BossAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            miss = random.randint(1, 3)
                            if miss == 1:
                                print('The spear missed you.'), slp1()
                            elif miss == 2:
                                print('You deflected the spear.'), slp1()
                            else:
                                print('You dodged the spear.'), slp1()

                elif action == 'dodge' or action == 'd':
                    bossAction = 0
                    dodgeFail = random.randint(1,10)
                    if dodgeFail == 10:
                        print('You tried to dodge the spear, but it still hit you.'),slp1()
                        print('The spear dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossAttack <= Armor:
                            BossAttack = 0
                        BossAttack = BossAttack - Armor
                        Pdamage = int(HP) - int(BossAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('You dodged the spear.'), slp1()

# Sandworm Queen battle................................
def SandwormQueen(current_location, boss):
    print('\n' * 100)
    print(' [Boss]')
    action = ''
    Attack = PlayerDamageFetch()
    Accuracy = PlayerAccuracyFetch()
    Armor = PlayerArmorFetch()
    Block = PlayerBlockFetch()
    BossHP = BossHPfetch(current_location, boss)
    BossAccuracy = BossAccuracyFetch(current_location, boss)
    BossDodge = BossDodgeFetch(current_location, boss)
    print('You are in a battle with: ' + boss)
    rocks = 4
    while BossHP > 0:
        print()
        HP = PlayerHPfetch()
        BossHP = BossHPfetch(current_location, boss)
        BossAttack = BossAttackFetch(current_location, boss)
        print('[Player HP: ' + str(HP) + '] ', end='')
        print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) + ']',end='')
        estusAmmountPrint()
        print('[' + boss + ' HP: ' + str(BossHP) + '] ',end='')
        if insightEquipped() == 1:
            cur.execute("SELECT Attack, Accuracy, Dodge FROM Boss WHERE Location = '" + current_location + "'AND Name ='" + boss + "'")
            for row in cur:
                print('Att[' + str(row[0]) + ' Acc[' + str(row[1]) + '0] Dodge[' + str(row[2]) + '0]')
        print('\n' * 2)
        bossAction = random.randint(1, 4)
        if bossAction == 1 or bossAction == 2:
            bossAction = 1  #Attack
        elif bossAction == 3:
            bossAction = 2  #Burrow
        else:
            bossAction = 3 #Idle
        if bossAction == 1:
            print('The ' + boss + ' attacks you.', end=''), slow_print04('.' * 4)
            while bossAction == 1:
                action = input('[Attack/Dodge/High Ground/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'high ground' or action == 'hg' or action == 'heal' or action == 'h':
                    if action == 'attack' or action == 'a':
                        bossAction = 0
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04(
                            '.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.'),slp1()

                    elif action == 'high ground' or action == 'hg':
                        bossAction = 0
                        print('You try to get up on a rock', end=''), slow_print04('.' * 4)

                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Blocked = random.randint(1, 10)
                    if Blocked <= Block:
                        print(
                            'You blocked the ' + boss + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
                    else:
                        Bosshit = random.randint(1, 10)
                        if Bosshit <= BossAccuracy:
                            print(boss + ' Hit\'s you!'), slp05()
                            print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if BossAttack <= Armor:
                                BossAttack = 0
                            BossAttack = BossAttack - Armor
                            Pdamage = int(HP) - int(BossAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            miss = random.randint(1, 3)
                            if miss == 1:
                                print('The ' + boss + ' missed you.'), slp1()
                            elif miss == 2:
                                print('You deflect the ' + boss + '\'s attack.'), slp1()
                            else:
                                print('You dodge the ' + boss + '\'s attack.'), slp1()

                elif action == 'dodge' or action == 'd':
                    bossAction = 0
                    dodgeFail = random.randint(1, 10)
                    if dodgeFail == 10:
                        print('You tried to dodge the attack, but it still hit you.'), slp1()
                        print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossAttack <= Armor:
                            BossAttack = 0
                        BossAttack = BossAttack - Armor
                        Pdamage = int(HP) - int(BossAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('You dodged the ' + boss + '\'s attack.'), slp1()

        if bossAction == 2:
            print('The ' + boss + ' burrows into the ground.', end=''), slow_print04('.' * 4)
            while bossAction == 2:
                action = input('[Attack/Dodge/High Ground/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'dodge' or action == 'd' or action == 'heal' or action == 'h':
                    bossAction = 0
                    if action == 'attack' or action == 'a':
                        print(boss + ' is nowhere to be seen.'),slp1()
                    elif action == 'dodge' or action == 'd':
                        print('You dodge nothing'),slp1()
                    elif action == 'heal' or action == 'h':
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Bosshit = random.randint(1, 10)
                    if Bosshit <= BossAccuracy:
                        BossCriticalAttack = BossAttack * 2
                        print('The ' + boss + ' bursts out of the sand'), slp1()
                        print(boss + ' Hit\'s you critically!'), slp1()
                        print(boss + ' dealt ' + str(BossCriticalAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossCriticalAttack <= Armor:
                            BossCriticalAttack = 0
                        BossCriticalAttack = BossCriticalAttack - Armor
                        Pdamage = int(HP) - int(BossCriticalAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('The ' + boss + ' missed you.'), slp1()

                elif action == 'high ground' or action == 'hg':
                    if rocks > 0:
                        rocks -= 1
                        print('You climbed up on a rock.'), slp2()
                        print('The ' + boss + ' bursts out of the sand and swallows the rock you are standing on.'), slp2()
                        print('You jump off the rock and avoid the attack.'),slp2()
                    else:
                        print('No more rocks to climb on.'),slp2()
                        print('The ' + boss + ' bursts out of the sand'), slp2()
                        Bosshit = random.randint(1, 10)
                        if Bosshit <= BossAccuracy:
                            BossCriticalAttack = BossAttack * 2
                            print(boss + ' Hit\'s you critically!'), slp1()
                            print(boss + ' dealt ' + str(BossCriticalAttack) + ' damage to you.'),slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if BossCriticalAttack <= Armor:
                                BossCriticalAttack = 0
                            BossCriticalAttack = BossCriticalAttack - Armor
                            Pdamage = int(HP) - int(BossCriticalAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            print('The ' + boss + ' missed you.'), slp1()
                    bossAction = 0

        if bossAction == 3:
            print('The ' + boss + ' screeches at you!', end='')
            while bossAction == 3:
                action = input('[Attack/Dodge/High Ground/Heal]')
                action.lower()
                if action == 'high ground' or action == 'hg' or action == 'dodge' or action == 'd' or action == 'heal' or action == 'h':
                    if action == 'high ground' or action == 'hg':
                        bossAction = 0
                        print('You climbed on a rock.'),slp1()
                    elif action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('Dodge nothing. A wasted opportunity.'),slp1()
                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                elif action == 'attack' or action == 'a':
                    print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                    hitChance = Accuracy - BossDodge
                    hit = random.randint(1, 10)
                    if hit <= hitChance:
                        critical = random.randint(1, 10)
                        if critical == 10:
                            print('Critical Hit! 2xdamage.'), slp05()
                            Bdamage = int(BossHP) - int(Attack) * 2
                            print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                        else:
                            print('Hit!'), slp05()
                            Bdamage = int(BossHP) - int(Attack)
                            print('You dealt ' + str(Attack) + ' damage.'), slp1()
                        cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                        BossHP = BossHPfetch(current_location, boss)
                        if BossHP <= 0:
                            cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                            for row in cur:
                                print(row[0]),slp2()
                            cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                            cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                            for row in cur.fetchall():
                                gold = row[0]
                            GoldAdd(gold)
                            slp1()
                            print('\n' * 2)
                            MainGameLoop()
                    else:
                        print('you missed.'),slp1()
                    bossAction = 0

#Smoldering Dragon battle................................
def SmolderingDragon(current_location, boss):
    print('\n' * 100)
    print(' [Boss]')
    action = ''
    Attack = PlayerDamageFetch()
    Accuracy = PlayerAccuracyFetch()
    Armor = PlayerArmorFetch()
    Block = PlayerBlockFetch()
    BossHP = BossHPfetch(current_location, boss)
    BossAccuracy = BossAccuracyFetch(current_location, boss)
    BossDodge = BossDodgeFetch(current_location, boss)
    print('You are in a battle with: ' + boss)
    while BossHP > 0:
        print()
        HP = PlayerHPfetch()
        BossHP = BossHPfetch(current_location, boss)
        BossAttack = BossAttackFetch(current_location, boss)
        print('[Player HP: ' + str(HP) + '] ', end='')
        print('Att[' + str(Attack) + '] Acc[' + str(Accuracy) + '0] Blk[' + str(Block) + '0] Armor[' + str(Armor) + ']',end='')
        estusAmmountPrint()
        print('[' + boss + ' HP: ' + str(BossHP) + '] ',end='')
        if insightEquipped() == 1:
            cur.execute("SELECT Attack, Accuracy, Dodge FROM Boss WHERE Location = '" + current_location + "'AND Name ='" + boss + "'")
            for row in cur:
                print('Att[' + str(row[0]) + ' Acc[' + str(row[1]) + '0] Dodge[' + str(row[2]) + '0]')
        print('\n' * 2)
        bossAction = random.randint(1, 8)
        if bossAction == 1 or bossAction == 2 or bossAction == 3:
            bossAction = 1  #Claws
        elif bossAction == 4:
            bossAction = 2  #Fly
        elif bossAction == 5 or bossAction == 6:
            bossAction = 3 #FireBreath
        else:
            bossAction = 4 #Idle
        if bossAction == 1:
            print('The ' + boss + ' swings it\'s claws at you.', end=''), slow_print04('.' * 4)
            while bossAction == 1:
                action = input('[Attack/Dodge/Cover/Run/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'cover' or action == 'c' or action == 'run' or action == 'r' or action == 'heal' or action == 'h':
                    if action == 'attack' or action == 'a':
                        bossAction = 0
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(1, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.')

                    elif action == 'cover' or action == 'c':
                        bossAction = 0
                        print('You try to find a place to hide under', end=''), slow_print04('.' * 4)

                    elif action == 'run' or action == 'r':
                        bossAction = 0
                        print('You try to run to avoid the attack', end=''), slow_print04('.' * 4)

                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Blocked = random.randint(1, 10)
                    if Blocked <= Block:
                        print('You blocked the ' + boss + '\'s attack with your ' + FetchEquipShieldDetails() + '.'), slp1()
                    else:
                        Bosshit = random.randint(1, 10)
                        if Bosshit <= BossAccuracy:
                            print(boss + ' Hit\'s you!'), slp1()
                            print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'), slp1()
                            ArmorEquipped = FetchEquipArmor()
                            HelmetEquipped = FetchEquipHelmet()
                            if ArmorEquipped == 1 or HelmetEquipped == 1:
                                print('Your armor negated ' + str(Armor) + ' damage.')
                            slp1()
                            if BossAttack <= Armor:
                                BossAttack = 0
                            BossAttack = BossAttack - Armor
                            Pdamage = int(HP) - int(BossAttack)
                            cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                            HP = PlayerHPfetch()
                            if HP <= 0:
                                gameOver()
                        else:
                            miss = random.randint(1, 3)
                            if miss == 1:
                                print('The ' + boss + ' missed you.'), slp1()
                            elif miss == 2:
                                print('You deflected the ' + boss + '\'s attack.'), slp1()
                            else:
                                print('You dodged the ' + boss + '\'s attack.'), slp1()

                elif action == 'dodge' or action == 'd':
                    bossAction = 0
                    dodgeFail = random.randint(1, 10)
                    if dodgeFail == 10:
                        print('You tried to dodge the claws, but it still hits you.'), slp1()
                        print(boss + ' dealt ' + str(BossAttack) + ' damage to you.'), slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossAttack <= Armor:
                            BossAttack = 0
                        BossAttack = BossAttack - Armor
                        Pdamage = int(HP) - int(BossAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('You dodged the ' + boss + '\'s attack.'), slp1()

        if bossAction == 2:
            print('The ' + boss + ' flies up into the air.', end=''), slow_print04('.' * 4)
            while bossAction == 2:
                action = input('[Attack/Dodge/Cover/Run/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'dodge' or action == 'd' or action == 'run' or action == 'r' or action == 'heal' or action == 'h':
                    bossAction = 0
                    if action == 'attack' or action == 'a':
                        print(boss + ' is nowhere to be seen.'), slp1()
                    elif action == 'dodge' or action == 'd':
                        print('You dodge nothing'), slp1()
                    elif action == 'heal' or action == 'h':
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()
                    print('The ' + boss + ' flies over you and burns you into a crisp.'),slp2()
                    gameOver()

                elif action == 'cover' or action == 'c':
                    print('You find a rock to hide under.'), slp2()
                    print('The ' + boss + ' can\'t find you and lands.'), slp2()
                    bossAction = 0

        if bossAction == 3:
            print('The ' + boss + ' stands on all fours and opens it\'s mouth.', end=''), slow_print04('.' * 4)
            while bossAction == 3:
                action = input('[Attack/Dodge/Cover/Run/Heal]')
                action.lower()
                if action == 'attack' or action == 'a' or action == 'dodge' or action == 'd' or action == 'cover' or action == 'c' or action == 'heal' or action == 'h':
                    bossAction = 0
                    if action == 'attack' or action == 'a':
                        print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                        hitChance = Accuracy - BossDodge
                        hit = random.randint(1, 10)
                        if hit <= hitChance:
                            critical = random.randint(5, 10)
                            if critical == 10:
                                print('Critical Hit! 2xdamage.'), slp05()
                                Bdamage = int(BossHP) - int(Attack) * 2
                                print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                            else:
                                print('Hit!'), slp05()
                                Bdamage = int(BossHP) - int(Attack)
                                print('You dealt ' + str(Attack) + ' damage.'), slp1()
                            cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                            BossHP = BossHPfetch(current_location, boss)
                            if BossHP <= 0:
                                cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                                for row in cur:
                                    print(row[0]),slp2()
                                cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                                cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                                for row in cur.fetchall():
                                    gold = row[0]
                                GoldAdd(gold)
                                slp1()
                                print('\n' * 2)
                                MainGameLoop()
                        else:
                            print('you missed.')

                    elif action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('You try to dodge the ' + boss + '\'s attack',end=''),slow_print04('.'*4)
                    elif action == 'cover' or action == 'c':
                        bossAction = 0
                        print('You try to find a place to hide under', end=''), slow_print04('.' * 4)
                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                    Bosshit = random.randint(1, 10)
                    if Bosshit <= BossAccuracy:
                        BossCriticalAttack = BossAttack * 2
                        print(boss + ' breathes fire at you.'),slp05()
                        print(boss + ' Hit\'s you critically!'), slp05()
                        print(boss + ' dealt ' + str(BossCriticalAttack) + ' damage to you.'),slp1()
                        ArmorEquipped = FetchEquipArmor()
                        HelmetEquipped = FetchEquipHelmet()
                        if ArmorEquipped == 1 or HelmetEquipped == 1:
                            print('Your armor negated ' + str(Armor) + ' damage.')
                        slp1()
                        if BossCriticalAttack <= Armor:
                            BossCriticalAttack = 0
                        BossCriticalAttack = BossCriticalAttack - Armor
                        Pdamage = int(HP) - int(BossCriticalAttack)
                        cur.execute("UPDATE Player Set HP ='" + str(Pdamage) + "'")
                        HP = PlayerHPfetch()
                        if HP <= 0:
                            gameOver()
                    else:
                        print('The ' + boss + ' missed you.'), slp1()

                elif action == 'run' or action == 'r':
                    print(boss + ' breathes fire at you.'), slp05()
                    print('You ran far enough to avoid the fire.'), slp1()
                    bossAction = 0

        if bossAction == 4:
            print('The ' + boss + ' stares at you.', end='')
            while bossAction == 4:
                action = input('[Attack/Dodge/Cover/Run/Heal]')
                action.lower()
                if action == 'cover' or action == 'c' or action == 'dodge' or action == 'd' or action == 'run' or action == 'r' or action == 'heal' or action == 'h':
                    if action == 'cover' or action == 'c':
                        bossAction = 0
                        print('You hide under a rock.'),slp1()
                    elif action == 'run' or action == 'r':
                        bossAction = 0
                        print('You ran away from the ' + boss), slp1()
                    elif action == 'dodge' or action == 'd':
                        bossAction = 0
                        print('Dodge nothing. A wasted opportunity.'),slp1()
                    elif action == 'heal' or action == 'h':
                        bossAction = 0
                        target = 'estus'
                        drink(target)
                        HP = PlayerHPfetch()

                elif action == 'attack' or action == 'a':
                    print('You attack with your', FetchEquipWpnDetails(), end=''), slow_print04('.' * 4)
                    hitChance = Accuracy - BossDodge
                    hit = random.randint(1, 10)
                    if hit <= hitChance:
                        critical = random.randint(1, 10)
                        if critical == 10:
                            print('Critical Hit! 2xdamage.'), slp05()
                            Bdamage = int(BossHP) - int(Attack) * 2
                            print('You dealt ' + str(Attack * 2) + ' damage.'), slp1()
                        else:
                            print('Hit!'), slp05()
                            Bdamage = int(BossHP) - int(Attack)
                            print('You dealt ' + str(Attack) + ' damage.'), slp1()
                        cur.execute("UPDATE Boss Set HP ='" + str(Bdamage) + "'WHERE Location ='" + current_location + "'AND Name ='" + boss + "'")
                        BossHP = BossHPfetch(current_location, boss)
                        if BossHP <= 0:
                            cur.execute("SELECT Diedesc FROM Boss WHERE Name = '" + boss + "'")
                            for row in cur:
                                print(row[0]),slp2()
                            cur.execute("UPDATE Boss Set Available = 0 WHERE Name ='" + boss + "'AND Location ='" + current_location + "'")
                            cur.execute("SELECT Gold FROM Boss WHERE Location ='" + current_location + "'")
                            for row in cur.fetchall():
                                gold = row[0]
                            GoldAdd(gold)
                            slp1()
                            print('\n' * 2)
                            MainGameLoop()
                    else:
                        print('you missed.'),slp1()
                    bossAction = 0


#Location.............................................................................

#Prints name of the current location..............
def locationName(current_location):
    cur.execute("SELECT Name FROM Location WHERE ID='" + current_location + "'")
    for row in cur:
        print(' ['+row[0]+']'),print()
        # Red Dragon Drop------------------------
    cur.execute("SELECT Available FROM Enemy WHERE Name= 'Red Dragon'")
    for row in cur:
        redDragonAvailable = row[0]
    if redDragonAvailable == 0:
        cur.execute("UPDATE Shield SET Location = 'mountain22' WHERE Name = 'greatshield'")
    location_description(current_location)

#Prints description of the current location.......
def location_description(current_location):
    mapPrint(current_location)
    cur.execute("SELECT Description FROM Location WHERE ID='" + current_location + "'")
    for row in cur:
        print(row[0])
    enemyEncounter(current_location)
    BossEncounter(current_location)
    lootNames(current_location)

#Weapon,Shield,Armor&Consumable Names...............
def lootNames(current_location):
    cur.execute("SELECT Details FROM Weapon WHERE PlayerID = 0 AND Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-',row[0])
    cur.execute("SELECT Details FROM Shield WHERE PlayerID = 0 AND Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-', row[0])
    cur.execute("SELECT Details FROM Helmet WHERE PlayerID = 0 AND Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-', row[0])
    cur.execute("SELECT Details FROM Armor WHERE PlayerID = 0 AND Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-', row[0])
    cur.execute("SELECT Details FROM Consumable WHERE PlayerID = 0 AND Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-', row[0])
    cur.execute("SELECT Details FROM Bonfire WHERE Location ='" + current_location + "'AND Available = 1")
    for row in cur:
        print('Something on the ground:')
        print('-', row[0])
    return

#Movement..............................................................................
def move(current_location, direction):
    lock = 0
    cur.execute("SELECT Locked FROM Passage WHERE Direction= '" + direction + "' AND Source='" + current_location + "'")
    for row in cur:
        lock = (row[0])
    if lock == 1:
        cur.execute("SELECT Locknote FROM Passage WHERE Source ='" + current_location + "'AND Direction = '" + direction + "'")
        for row in cur.fetchall():
            print(row[0])
    unlocked = (len(MoveFetch(current_location,direction)))
    if unlocked > 1:
        print('\n' * 100)
        destination = MoveFetch(current_location,direction)
        if destination == 'forests':
            cur.execute("UPDATE Object SET Available = 0 WHERE Name = 'shutters'")

    else:
        destination = current_location
        if lock != 1:
            print("You can\'t move to that direction.")
    cur.execute("UPDATE Passage SET Locked = 1 WHERE Source = 'forests' AND Destination = 'hallnorth'")
    cur.execute("UPDATE Passage SET Locked = 1 WHERE Source = 'mountain4' AND Destination = 'mountain5'")
    return destination

#Game loop...................
def MainGameLoop():
    game_loop = 1
    global Gcurrent_location
    locationName(Gcurrent_location)  # Global current location.
    while game_loop == 1:

        #Input-------------------------------

        player_input = input('').split()
        if len(player_input)>=1:
            action = player_input[0].lower()
        else:
            action = ""
        if len(player_input)>=2:
            target = player_input[len(player_input)-1].lower()
        else:
            target = ""
        print()




        #Complete-----------------------------
        cur.execute("SELECT Available FROM Boss Where Name = 'Old Giant'")
        for row in cur:
            OldGiantHP = row[0]
            #print(OldGiantHP)
        cur.execute("SELECT Available FROM Boss Where Name = 'Pharaoh King'")
        for row in cur:
            PharaohKingHP = row[0]
            #print(PharaohKingHP)
        cur.execute("SELECT Available FROM Boss Where Name = 'Sandworm Queen'")
        for row in cur:
            SandwormQueenHP = row[0]
            #print(SandwormQueenHP)
        cur.execute("SELECT Available FROM Boss Where Name = 'Smoldering Dragon'")
        for row in cur:
            SmolderingDragonHP = row[0]
            #print(SmolderingDragonHP)
        if OldGiantHP <= 0 and PharaohKingHP <= 0 and SandwormQueenHP <= 0 and SmolderingDragonHP <= 0:
            victory()

        #Rest-----------------------------------------
        if action == 'rest' and target == 'bonfire':
            bonfire(Gcurrent_location)

        #Inventory------------------------------------
        elif action == 'i' or action == 'inventory':
            inventory()

        #Look around-------------------------------
        elif action == 'look' and target == 'around':
            location_description(Gcurrent_location)

        # Examine--------------------------------------
        elif (action == 'read' or action == 'examine') and target == 'scroll':
            readScroll(Gcurrent_location, target)

        # Examine--------------------------------------
        elif action == 'examine' or action == 'look':
            examineObject(Gcurrent_location,target)

        #Talk------------------------------------------
        elif action == 'talk':
            if target == 'merchant' and Gcurrent_location == 'forestcabin':
                merchant(Gcurrent_location)
            elif target == 'pyromancer' and Gcurrent_location == 'deserthut':
                pyromancer(Gcurrent_location)
            elif target == 'armorer' and Gcurrent_location == 'road2':
                armorer(Gcurrent_location)
            else:
                print('No ' + target + ' to talk to.')

        # Take------------------------------------------------
        elif action == 'take' or action == 'pickup':
            take(Gcurrent_location, target)

        #Help------------------------------------------------------
        elif action == 'help':
            help()

        #Open---------------------------------------------------
        elif action == 'open':
            open(Gcurrent_location, target)

        #Pull----------------------------------------------------
        elif action == 'pull':
            if target == 'chains':
                pullChains(Gcurrent_location)
            elif target == 'lever':
                pullLever(Gcurrent_location)
            else:
                print('No ' + target + ' to pull here.')

        #Throw Whip
        elif action == 'throw' and target == 'whip':
            throwWhip(Gcurrent_location)

        #Cut-------------------------
        elif action == 'cut' and target == 'tree':
            cutTree(Gcurrent_location)

        #Blowup
        elif action == 'blowup' and target == 'boulder':
            blowupBoulder(Gcurrent_location)

        #Drink--------------------------------------------------
        elif action == 'drink':
            drink(target)

        #Equip--------------------------------------------------
        elif action == 'equip':
            equip(target)

        #Unequip---------------------------------
        elif action == 'unequip':
            unequip(target)

        #Drop--------------------------------
        elif action == 'drop':
            drop(Gcurrent_location,target)

        #Movement----------------------------------------------
        elif action == 'north' or action == 'n' or action == 'west' or action == 'w' or action == 'south' or action == 's' or action == 'east' or action == 'e' \
        or action == 'up' or action == 'u' or action == 'down' or action == 'd':
            if action == 'north':
                action = 'n'
            if action == 'south':
                action = 's'
            if action == 'west':
                action = 'w'
            if action == 'east':
                action = 'e'
            if action == 'up':
                action = 'u'
            if action == 'down':
                action = 'd'

            newlocation = move(Gcurrent_location,action)

            if Gcurrent_location == newlocation:
                print(end='')
            else:
                Gcurrent_location = newlocation
                locationName(Gcurrent_location)
        #Save------------
        elif action == 'save':
            if target == 'game':
                LocationUpdate(Gcurrent_location)
                db.commit()
                print('Game saved.')
            else:
                save = input('Do you want to save the game?')
                save.lower()
                if save == 'yes' or save == 'y':
                    LocationUpdate(Gcurrent_location)
                    db.commit()
                    print('Game saved.')

        #Quit----------
        elif action == 'quit':
            quit = input('Are you sure you want to quit?')
            quit[0].lower()
            if quit == 'yes':
                mainMenu()
        elif action == '' and target == '':
            print()

        #Wrong Input-------------------
        else:
            if target != '':
                print('I don\'t know how to', action,target+'.')
            else:
                print('I don\'t know how to',action+'.')

def create_table():
    cur.execute("DROP TABLE IF EXISTS Location")
    cur.execute("DROP TABLE IF EXISTS Passage")
    cur.execute("DROP TABLE IF EXISTS Player")
    cur.execute("DROP TABLE IF EXISTS Weapon")
    cur.execute("DROP TABLE IF EXISTS Shield")
    cur.execute("DROP TABLE IF EXISTS Armor")
    cur.execute("DROP TABLE IF EXISTS Helmet")
    cur.execute("DROP TABLE IF EXISTS Enemy")
    cur.execute("DROP TABLE IF EXISTS NPC")
    cur.execute("DROP TABLE IF EXISTS Boss")
    cur.execute("DROP TABLE IF EXISTS Object")
    cur.execute("DROP TABLE IF EXISTS Bonfire")
    cur.execute("DROP TABLE IF EXISTS Consumable")
    cur.execute("CREATE TABLE IF NOT EXISTS Location(ID TEXT, Name TEXT, Room1 TEXT, Room2 TEXT, Room3 TEXT, Description TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Passage(ID TEXT, Source TEXT, Destination TEXT, Direction TEXT, Locked INT,Locknote TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Player(ID INT, HP INT, MaxHP INT, Gold INT, Estus INT, Bonfire TEXT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Weapon(ID INT, Name TEXT, Details TEXT, Description TEXT, DescGround TEXT, Available INT, Attack INT, Accuracy INT, Equipped INT, PlayerID INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Shield(ID INT, Name TEXT, Details TEXT, Description TEXT, DescGround TEXT, Available INT, Block INT, Equipped INT, PlayerID INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Armor(ID INT, Name TEXT, Details TEXT, Description TEXT, DescGround TEXT, Available INT, Armor INT, Equipped INT, PlayerID INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Helmet(ID INT, Name TEXT, Details TEXT, Description TEXT, DescGround TEXT, Available INT, Helmet INT, Equipped INT, PlayerID INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Enemy(ID INT, Name TEXT, Description TEXT, HP INT, MaxHP INT, Attack INT, Accuracy INT, Dodge INT, Available INT, Gold INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Boss(ID INT, Name TEXT, Description TEXT, Diedesc TEXT, HP INT, MaxHP INT, Attack INT, Accuracy INT, Dodge INT, Available INT, Gold INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS NPC(ID INT, Name TEXT, Details TEXT, Description TEXT, Available INT, Gear1 TEXT, G1cost INT, Gear2 TEXT, G2cost INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Object(ID INT, Name TEXT, Details TEXT, Description TEXT, Desc2 TEXT, Available INT, Takeable INT, Gold INT, PlayerID INT, Door INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Bonfire(ID INT, Name TEXT, Details TEXT, Description TEXT, Available INT, Location TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Consumable(ID INT, Name Text, Details Text, Description TEXT, DescGround TEXT, Available INT, Health INT, PlayerID INT, Location TEXT)")

def data_entry():
    #PRISON
    cur.execute("INSERT INTO Location VALUES('cell', 'Cell', ' /-  -\ ', ' |    |', ' \----/','A dark cell. There is a cell Door to North and a Puddle in the ground.')")
    cur.execute("INSERT INTO Location VALUES('cell2', 'Cell #2', ' /----\ ', ' |', ' \----/', 'A dark cell with a skeleton lying on the ground. There is a open cell door to East.')")
    cur.execute("INSERT INTO Location VALUES('cell3', 'Cell #3', ' /----\ ', '      |', ' \----/','A dark cell with Chains hanging off from the cealing. There is a open cell door to West.')")
    cur.execute("INSERT INTO Location VALUES('cellcorridor', 'Cell Corridor', ' /-  -\ ', ' ', ' \-  -/','A dark corridor leads to North, there is also an open cell door to your South, West and East.')")
    cur.execute("INSERT INTO Location VALUES('pitbottom', 'Bottom of a Pit', ' /----\ ', ' | =  |', ' \-  -/','There is a Ladder going Up here and a way to South.')")
    cur.execute("INSERT INTO Location VALUES('pittop', 'Top of a Pit', ' /-  -\ ', ' | =  |', ' \----/','A small room that has a ladder going Down and an open doorway to North.')")

    #Tomb
    cur.execute("INSERT INTO Location VALUES('celltombtop', 'Tomb Entrance', ' /----\ ', ' |  = |', ' \----/','A small room that has a ladder going Down and a way to West. The is also Chains hanging off from the cealing.')")
    cur.execute("INSERT INTO Location VALUES('tombsouthwest', 'Tomb', ' /-  -\ ', ' | =  |', ' \----/','A small room that has a ladder going Up and a open doorway to North.')")
    cur.execute("INSERT INTO Location VALUES('tombwest', 'Tomb', ' /-  -\ ', ' |', ' \-  -/','A small room that has an open doorway to North, South and East.')")
    cur.execute("INSERT INTO Location VALUES('tombnorthwest', 'Tomb', ' /----\ ', ' |', ' \-  -/','A small room that has an open doorway to South and East.')")
    cur.execute("INSERT INTO Location VALUES('tombnortheast', 'Tomb', ' /----\ ', '    = |', ' \-  -/','A small room that has a ladder going Up and an open doorway to South and West.')")
    cur.execute("INSERT INTO Location VALUES('tombeast', 'Tomb', ' /-  -\ ', '      |', ' \-  -/','A small room that has an open doorway to North, West and South.')")
    cur.execute("INSERT INTO Location VALUES('tombsoutheast', 'Throne Room Entrance',' /-  -\ ', ' |', ' \----/', 'A small room that has an open doorway to North and East')")
    cur.execute("INSERT INTO Location VALUES('throneroom', 'Throne Room',' /----\ ', '      |', ' \----/', 'A large room with a huge throne and an open doorway to West')")

    #Hall
    cur.execute("INSERT INTO Location VALUES('hall', 'Large Hall', ' /-  -\ ', ' ', ' \-  -/','A large hall. You can go South, North, West or East')")
    cur.execute("INSERT INTO Location VALUES('halleast', 'Large Hall East', ' /-  -\ ', '      |', ' \-  -/','You can go West and there is an open doorway to North and South.')")
    cur.execute("INSERT INTO Location VALUES('hallnortheast', 'Small Room',' /----\ ', ' |    |', ' \-  -/', 'There is an open doorway to South.')")
    cur.execute("INSERT INTO Location VALUES('hallarmory', 'Armory', ' /-  -\ ', ' |    |', ' \----/','A large room with lots of empty weapon racks.')")
    cur.execute("INSERT INTO Location VALUES('hallentry', 'Large Hall Entrance', ' /-  -\ ', ' ', ' \-  -/','The entrance to this Hall. A large Gate to West and open archway to East, North and South')")
    cur.execute("INSERT INTO Location VALUES('hallnorth', 'Large Hall North',' /-  -\ ', ' |    |', ' \-  -/', 'There is a small window here with wooden Shutters to North and you can move to South.')")
    cur.execute("INSERT INTO Location VALUES('hallstorage', 'Destroyed Library', ' /-  -\ ', ' |    |', ' \----/','A room that use to be a library, but now its just a storage for burnt books. There is still one not so broken book Shelf in here.')")
    cur.execute("INSERT INTO Location VALUES('hallroom', 'Small Room',' /----\ ', ' | =  |', ' \-  -/', 'A small room with a ladder going Up and an open doorway to South.')")
    cur.execute("INSERT INTO Location VALUES('halltower', 'Tower',' /----\ ', ' | =  |', ' \----/', 'There is a beautiful view here: A large mountain to west, a dense forest to north and a large desert to east. There is also a Lever here and a ladder going Down.')")

    #Road
    cur.execute("INSERT INTO Location VALUES('hallout', 'Draw Bridge',' ------', '', ' ------', 'The bridge leads to West and East')")
    cur.execute("INSERT INTO Location VALUES('road1', 'Road',' /-  -\ ', ' |', ' \----/', 'The road leads to North and East')")
    cur.execute("INSERT INTO Location VALUES('road2', 'Road',' /-  -\ ', ' |    |', ' \-  -/', 'There is an Armorer and his vagon here. The road leads to North and South')")
    cur.execute("INSERT INTO Location VALUES('road3', 'Road',' /-  -\ ', '      |', ' \-  -/', 'The road leads to North, South and West')")
    cur.execute("INSERT INTO Location VALUES('road4', 'Road Riverbank', ' /----\ ', ' |', ' \-  -/','The road leads to South and East')")
    cur.execute("INSERT INTO Location VALUES('bridge', 'Stone Bridge',' ------', ' ', ' ------', 'A rundown stone bridge. The bridge leads to west and East')")

    #Forest
    cur.execute("INSERT INTO Location VALUES('forests', 'Forest', ' /-  -\ ', ' |', ' \-  -/','A dark forest. The path leads to North, East and there is an open Window to your South.')")
    cur.execute("INSERT INTO Location VALUES('forestsoutheast', 'Forest', ' /-  -\ ', ' ', ' \----/','The path leads to West, North and there is a giant Tree to East.')")
    cur.execute("INSERT INTO Location VALUES('foreste', 'Forest', ' /----\ ', '      |', ' \-  -/','A dark forest. The path leads to South and West.')")
    cur.execute("INSERT INTO Location VALUES('forestarea', 'Forest',' /-  -\ ', ' ', ' \-  -/', 'Open forest in every direction.')")
    cur.execute("INSERT INTO Location VALUES('forestn', 'Forest', ' /-  -\ ', ' |    |', ' \-  -/','You are standing outside of a cabin. Cabin to your North and forest path to your South.')")
    cur.execute("INSERT INTO Location VALUES('forestcabin', 'Cabin', ' /----\ ', ' |    |', ' \-  -/','You are inside of a cabin. There is a Merchant here and an open door to your South.')")
    cur.execute("INSERT INTO Location VALUES('forestw', 'Forest Riverbank', ' /----\ ', ' ', ' \-  -/','A path leads to West, East and South.')")
    cur.execute("INSERT INTO Location VALUES('forestsouthwest', 'Forest',' /-  -\ ', ' |    |', ' \----/', 'A dead end. The path leads to north.')")

    #Desert
    cur.execute("INSERT INTO Location VALUES('desertwest', 'Desert',' /-  -\ ', ' ', ' \----/', 'The path leads to North and East and there is a giant Tree to West.')")
    cur.execute("INSERT INTO Location VALUES('desertledge', 'Desert Ledge', ' /----\ ', '      |', ' \-  -/','The path leads to South and there is a big drop here to West, but it should be safe.')")
    cur.execute("INSERT INTO Location VALUES('desertarea', 'Desert', ' /-  -\ ', ' ', ' \-  -/','A path leads to every direction.')")
    cur.execute("INSERT INTO Location VALUES('desertsouthwest', 'Desert',' /-  -\ ', ' |', ' \----/', 'A path leads to North and East.')")
    cur.execute("INSERT INTO Location VALUES('desertsoutheast', 'Desert Tomb Entrance', ' /-  -\ ', '    = |', ' \----/','A path leads to North, West and there is a ladder Down.')")
    cur.execute("INSERT INTO Location VALUES('deserteast', 'Desert', ' /-  -\ ', ' ', ' \-  -/','A path leads to North, South, West and there is a hut to East.')")
    cur.execute("INSERT INTO Location VALUES('desertnortheast', 'Desert', ' /----\ ', '      |', ' \-  -/','A path leads to South and West.')")
    cur.execute("INSERT INTO Location VALUES('desertnorthwest', 'Desert', ' /-  -\ ', ' |', ' \-  -/','A path leads to South, North and East.')")
    cur.execute("INSERT INTO Location VALUES('desertnorth', 'Sand Pit',' /----\ ', ' |    |', ' \-  -/', 'A large sand pit with four rocks gathered around here and there. A path leads to South.')")
    cur.execute("INSERT INTO Location VALUES('deserthut', 'Hut', ' /----\ ', '      |', ' \----/','There is Pyromancer looking guy in here and open doorway to West.')")

    #Mountain
    cur.execute("INSERT INTO Location VALUES('mountain1', 'Mountain Pass',' /-  -\ ', ' |', ' \-  -/', 'The path leads to North, South and East.')")
    cur.execute("INSERT INTO Location VALUES('mountain2', 'Mountain Pass',' /----\ ', '      |', ' \-  -/', 'The path leads to West and South.')")
    cur.execute("INSERT INTO Location VALUES('mountain3', 'Mountain Pass', ' /----\ ', ' ', ' \----/','The path leads to West and East.')")
    cur.execute("INSERT INTO Location VALUES('mountain4', 'Mountain Pass',' /-  -\ ', ' |', ' \-  -/', 'A dead end. The path leads to East and there is a high Ledge to the South and a Cave entrance to North.')")
    cur.execute("INSERT INTO Location VALUES('mountain5', 'Mountain Pass', ' /-  -\ ', ' |', ' \-  -/','The path leads to East and South and there is a small drop to the North.')")
    cur.execute("INSERT INTO Location VALUES('lavapit', 'Lava Pit', ' /----\ ', '      |', ' \----/','A really hot lava in here. The path leads to West.')")
    cur.execute("INSERT INTO Location VALUES('mountain6', 'Mountain Pass',' /-  -\ ', ' |', ' \----/', 'The path leads to East and North.')")
    cur.execute("INSERT INTO Location VALUES('mountain7', 'Mountain Pass', ' /----\ ', ' ', ' \----/','The path leads to West and East and there is a large Boulder to the East.')")
    cur.execute("INSERT INTO Location VALUES('mountain8', 'Mountain Pass',' /-  -\ ', '      |', ' \----/', 'The path leads to West and North and there is a large Boulder to the West.')")
    cur.execute("INSERT INTO Location VALUES('mountain21', 'Cave',' /-  -\ ', ' |    |', ' \-  -/', 'The path leads to North and South.')")
    cur.execute("INSERT INTO Location VALUES('mountain22', 'Dragons Lair',' /----\ ', ' |    |', ' \-  -/', 'The path leads to South.')")

    #CELL
    cur.execute("INSERT INTO Passage VALUES('celln', 'cell', 'cellcorridor', 'n', 1, 'A rusty cell Door blocks your way. There has to be a way to Open it.')")
    cur.execute("INSERT INTO Passage VALUES('cell2e', 'cell2', 'cellcorridor', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('cell3w', 'cell3', 'cellcorridor', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('cell3e', 'cell3', 'celltombtop', 'e', 1, 'It looks like there is a hidden door in here.')")

    cur.execute("INSERT INTO Passage VALUES('corridors', 'cellcorridor', 'cell', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('corridorw', 'cellcorridor', 'cell2', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('corridore', 'cellcorridor', 'cell3', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('corridorn', 'cellcorridor', 'pitbottom', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('pitbottoms', 'pitbottom', 'cellcorridor', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('pitbottomup', 'pitbottom', 'pittop', 'u', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('pittopdown', 'pittop', 'pitbottom', 'd', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('pittopn', 'pittop', 'hall', 'n', 0, NULL)")

    #TOMB
    cur.execute("INSERT INTO Passage VALUES('celltombtopdown', 'celltombtop', 'tombsouthwest', 'd', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('celltombtopwest', 'celltombtop', 'cell3', 'w', 1, 'Wall blocks your way.')")

    cur.execute("INSERT INTO Passage VALUES('tombsouthwestup', 'tombsouthwest', 'celltombtop', 'u', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombsouthwestn', 'tombsouthwest', 'tombwest', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('tombws', 'tombwest', 'tombsouthwest', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombwn', 'tombwest', 'tombnorthwest', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombwe', 'tombwest', 'tombeast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('tombnorthwests', 'tombnorthwest', 'tombwest', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombnorthweste', 'tombnorthwest', 'tombnortheast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('tombnortheastw', 'tombnortheast', 'tombnorthwest', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombnortheasts', 'tombnortheast', 'tombeast', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombnortheastup', 'tombnortheast', 'desertsoutheast', 'u', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('tombeastn', 'tombeast', 'tombnortheast', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombeastw', 'tombeast', 'tombwest', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombeaste', 'tombeast', 'tombsoutheast', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('tombsoutheastn', 'tombsoutheast', 'tombeast', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('tombsoutheaste', 'tombsoutheast', 'throneroom', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('throneroomw', 'throneroom', 'tombsoutheast', 'w', 0, NULL)")

    #HALL
    cur.execute("INSERT INTO Passage VALUES('halls', 'hall', 'pittop', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('halln', 'hall', 'hallnorth', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('hallw', 'hall', 'hallentry', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('halle', 'hall', 'halleast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('halleastw', 'halleast', 'hall', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('halleasts', 'halleast', 'hallarmory', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('halleastn', 'halleast', 'hallnortheast', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallarmoryn', 'hallarmory', 'halleast', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallnortheasts', 'hallnortheast', 'halleast', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallnorthn', 'hallnorth', 'forests', 'n', 1, 'The closed wooden Shutters block your way.')")
    cur.execute("INSERT INTO Passage VALUES('hallnorths', 'hallnorth', 'hall', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallentrye', 'hallentry', 'hall', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('hallentryw', 'hallentry', 'hallout', 'w', 1, 'The huge Gate wont budge.')")
    cur.execute("INSERT INTO Passage VALUES('hallentrys', 'hallentry', 'hallstorage', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('hallentryn', 'hallentry', 'hallroom', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallstoragen', 'hallstorage', 'hallentry', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('hallrooms', 'hallroom', 'hallentry', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('hallroomu', 'hallroom', 'halltower', 'u', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('halltowerd', 'halltower', 'hallroom', 'd', 0, NULL)")

    #Road
    cur.execute("INSERT INTO Passage VALUES('halloute', 'hallout', 'hallentry', 'e', 1, 'The huge Gate wont budge.')")
    cur.execute("INSERT INTO Passage VALUES('halloutw', 'hallout', 'road1', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('road1e', 'road1', 'hallout', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('road1n', 'road1', 'road2', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('road2s', 'road2', 'road1', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('road2n', 'road2', 'road3', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('road3s', 'road3', 'road2', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('road3n', 'road3', 'road4', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('road3w', 'road3', 'mountain1', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('road4s', 'road4', 'road3', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('road4e', 'road4', 'bridge', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('bridgee', 'bridge', 'forestw', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('bridgew', 'bridge', 'road4', 'w', 0, NULL)")

    #MOUNTAIN
    cur.execute("INSERT INTO Passage VALUES('mountain1e', 'mountain1', 'road3', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain1n', 'mountain1', 'mountain2', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain1s', 'mountain1', 'mountain8', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain2s', 'mountain2', 'mountain1', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain2w', 'mountain2', 'mountain3', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain3e', 'mountain3', 'mountain2', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain3s', 'mountain3', 'mountain4', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain4e', 'mountain4', 'mountain3', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain4n', 'mountain4', 'mountain21', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain4s', 'mountain4', 'mountain5', 's', 1, 'The Ledge is too high to climb.')")

    cur.execute("INSERT INTO Passage VALUES('mountain21s', 'mountain21', 'mountain4', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain21n', 'mountain21', 'mountain22', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain22s', 'mountain22', 'mountain21', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain5n', 'mountain5', 'mountain4', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain5s', 'mountain5', 'mountain6', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain5e', 'mountain5', 'lavapit', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('lavapitw', 'lavapit', 'mountain5', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain6n', 'mountain6', 'mountain5', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain6e', 'mountain6', 'mountain7', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('mountain7w', 'mountain7', 'mountain6', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain7e', 'mountain7', 'mountain8', 'e', 1, 'The large Boulder blocks your way.')")

    cur.execute("INSERT INTO Passage VALUES('mountain8n', 'mountain8', 'mountain1', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('mountain8w', 'mountain8', 'mountain7', 'w', 1, 'The large Boulder blocks your way.')")

    #FOREST
    cur.execute("INSERT INTO Passage VALUES('forestss', 'forests', 'hallnorth', 's', 1, 'The Window is too high to climb in.')")
    cur.execute("INSERT INTO Passage VALUES('forestsn', 'forests', 'forestarea', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestse', 'forests', 'forestsoutheast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestsoutheastw', 'forestsoutheast', 'forests', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestsoutheaste', 'forestsoutheast', 'desertwest', 'e', 1, 'The giant Tree blocks your way. I need to Cut it down first.')")
    cur.execute("INSERT INTO Passage VALUES('forestsoutheastn', 'forestsoutheast', 'foreste', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestes', 'foreste', 'forestsoutheast', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestew', 'foreste', 'forestarea', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestareas', 'forestarea', 'forests', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestareaw', 'forestarea', 'forestw', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestareae', 'forestarea', 'foreste', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestarean', 'forestarea', 'forestn', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestwe', 'forestw', 'forestarea', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestws', 'forestw', 'forestsouthwest', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestww', 'forestw', 'bridge', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestsouthwestn', 'forestsouthwest', 'forestw', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestns', 'forestn', 'forestarea', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('forestnn', 'forestn', 'forestcabin', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('forestcabins', 'forestcabin', 'forestn', 's', 0, NULL)")

    #Desert
    cur.execute("INSERT INTO Passage VALUES('desertwestw', 'desertwest', 'forestsoutheast', 'w', 1, 'The giant Tree blocks your way. I need to Cut it down first.')")
    cur.execute("INSERT INTO Passage VALUES('desertweste', 'desertwest', 'desertarea', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertwestn', 'desertwest', 'desertledge', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertledges', 'desertledge', 'desertwest', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertledgew', 'desertledge', 'foreste', 'w', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertareaw', 'desertarea', 'desertwest', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertareas', 'desertarea', 'desertsouthwest', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertareae', 'desertarea', 'deserteast', 'e', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertarean', 'desertarea', 'desertnorthwest', 'n', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertsouthwestn', 'desertsouthwest', 'desertarea', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertsouthweste', 'desertsouthwest', 'desertsoutheast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertnorthwests', 'desertnorthwest', 'desertarea', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertnorthwestn', 'desertnorthwest', 'desertnorth', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertnorthweste', 'desertnorthwest', 'desertnortheast', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertnortheastw', 'desertnortheast', 'desertnorthwest', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertnortheasts', 'desertnortheast', 'deserteast', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('deserteastn', 'deserteast', 'desertnortheast', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('deserteastw', 'deserteast', 'desertarea', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('deserteasts', 'deserteast', 'desertsoutheast', 's', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('deserteaste', 'deserteast', 'deserthut', 'e', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertsoutheastn', 'desertsoutheast', 'deserteast', 'n', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertsoutheastw', 'desertsoutheast', 'desertsouthwest', 'w', 0, NULL)")
    cur.execute("INSERT INTO Passage VALUES('desertsoutheastd', 'desertsoutheast', 'tombnortheast', 'd', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('desertnorths', 'desertnorth', 'desertnorthwest', 's', 0, NULL)")

    cur.execute("INSERT INTO Passage VALUES('deserthutw', 'deserthut', 'deserteast', 'w', 0, NULL)")

    #PLAYER
    cur.execute("INSERT INTO Player VALUES(1, 100, 100, 0, 0, 'cell', 'empty')")

    #ENEMIES
    cur.execute("INSERT INTO Enemy VALUES(0, 'Undead prisoner', 'A reanimated corpse. Weak and clumsy.', 30, 30, 10, 3, -2, 1, 5, 'pitbottom')")
    cur.execute("INSERT INTO Enemy VALUES(1, 'Undead prisoner', 'A reanimated corpse. Weak and clumsy.', 30, 30, 10, 3, -2, 1, 5, 'cell3')")
    cur.execute("INSERT INTO Enemy VALUES(2, 'Skeleton Guard', 'A reanimated Skeleton with a sword in its hand. Not very tough looking and slow.', 40, 40, 20, 5, 1, 1, 10, 'hall')")
    cur.execute("INSERT INTO Enemy VALUES(3, 'Skeleton Guard', 'A reanimated Skeleton with a sword in its hand. Not very tough looking and slow.', 40, 40, 20, 5, 1, 1, 10, 'hallnorth')")
    cur.execute("INSERT INTO Enemy VALUES(4, 'Skeleton Guard', 'A reanimated Skeleton with a sword in its hand. Not very tough looking and slow.', 40, 40, 20, 5, 1, 1, 10, 'hallnortheast')")
    cur.execute("INSERT INTO Enemy VALUES(5, 'Mummy', 'A reanimated Mummy. Strong but clumsy.', 80, 80, 30, 3, -2, 1, 15, 'tombwest')")
    cur.execute("INSERT INTO Enemy VALUES(6, 'Mummy', 'A reanimated Mummy. Strong but clumsy.', 80, 80, 30, 3, -2, 1, 15, 'tombeast')")
    cur.execute("INSERT INTO Enemy VALUES(7, 'Mummy Soldier', 'A reanimated Mummy Soldier. Strong but slow.', 80, 80, 40, 5, 1, 1, 30, 'desertarea')")
    cur.execute("INSERT INTO Enemy VALUES(8, 'Mummy Soldier', 'A reanimated Mummy Soldier. Strong but slow.', 80, 80, 40, 5, 1, 1, 30, 'deserteast')")
    cur.execute("INSERT INTO Enemy VALUES(9, 'Giant Scorpion', 'A Giant yellow Scorpion. Fast and deadly.', 70, 70, 40, 5, 4, 1, 50, 'desertnorthwest')")
    cur.execute("INSERT INTO Enemy VALUES(10, 'Ent', 'A giant walking tree. Strong, but clumsy.', 120, 120, 50, 3, 0, 1, 40, 'forestsoutheast')")
    cur.execute("INSERT INTO Enemy VALUES(11, 'Ent', 'A giant walking tree. Strong, but clumsy.', 120, 120, 50, 3, 0, 1, 40, 'forestw')")
    cur.execute("INSERT INTO Enemy VALUES(12, 'Undead Highwayman', 'An Undead Highwayman. Looks average.', 70, 70, 35, 7, 3, 1, 30, 'road4')")
    cur.execute("INSERT INTO Enemy VALUES(13, 'Undead Highwayman', 'An Undead Highwayman. Looks average.', 70, 70, 35, 7, 3, 1, 30, 'road1')")
    #cur.execute("INSERT INTO Enemy VALUES(13, 'Bridge Troll', 'An average looking Troll.', 140, 140, 40, 3, 0, 1, 30, 'bridge')")
    cur.execute("INSERT INTO Enemy VALUES(14, 'Baby Dragon', 'A weak, but fast looking little Dragon.', 30, 30, 35, 9, 5, 1, 40, 'mountain2')")
    cur.execute("INSERT INTO Enemy VALUES(15, 'Baby Dragon', 'A weak, but fast looking little Dragon.', 30, 30, 35, 9, 5, 1, 40, 'mountain4')")
    cur.execute("INSERT INTO Enemy VALUES(16, 'Mountain Troll', 'Large Moutain Troll.', 200, 200, 60, 3, -2, 1, 60, 'mountain3')")
    cur.execute("INSERT INTO Enemy VALUES(17, 'Mountain Troll', 'Large Moutain Troll.', 200, 200, 60, 3, -2, 1, 60, 'mountain6')")
    cur.execute("INSERT INTO Enemy VALUES(18, 'Baby Dragon', 'A weak, but fast looking little Dragon.', 30, 30, 40, 9, 5, 1, 40, 'mountain21')")
    cur.execute("INSERT INTO Enemy VALUES(19, 'Red Dragon', 'A large Red Dragon.', 150, 150, 40, 5, 5, 1, 70, 'mountain22')")

    cur.execute("INSERT INTO Enemy VALUES(20, 'Mummy Soldier', 'A reanimated Mummy Soldier. Strong but slow.', 80, 80, 40, 5, 1, 1, 20, 'king')")
    cur.execute("INSERT INTO Enemy VALUES(21, 'Mummy', 'A reanimated Mummy. Strong but clumsy.', 80, 80, 30, 3, -2, 1, 10, 'king')")

    cur.execute("INSERT INTO Boss VALUES(0, 'Old Giant', 'A large Old Giant. Looks powerful, but slow.', 'The Old Giant falls to the ground.',300, 300, 40, 5, -2, 1, 80, 'forestarea')")
    cur.execute("INSERT INTO Boss VALUES(1, 'Pharaoh King', 'An undead Pharaoh King just sitting there on his throne.', 'The Pharaoh King crumbles to dust.', 300, 300, 30, 8, -2, 1, 80, 'throneroom')")
    cur.execute("INSERT INTO Boss VALUES(2, 'Sandworm Queen', 'A Giant Sandworm bursts out of the sand. A long haired woman attached to its head.', 'The Sandworm Queen lets out her final screech and fall to the ground.', 400, 400, 35, 8, 0, 1, 80, 'desertnorth')")
    cur.execute("INSERT INTO Boss VALUES(3, 'Smoldering Dragon', 'A huge ancient Dragon bursts out of the molten lava.', 'The Smoldering Dragon falls to the ground.', 500, 500, 50, 6, 0, 1, 100, 'lavapit')")

    cur.execute("INSERT INTO NPC VALUES(0, 'cabinmerchant', 'Merchant', 'I could Talk to him', 1, 'Leather Vest', 60, 'Hatchet', 50, 'forestcabin')")
    cur.execute("INSERT INTO NPC VALUES(1, 'hutpyromancer', 'Pyromancer', 'I could Talk to him', 1, 'Spear', 180, 'Explosives', 20, 'deserthut')")
    cur.execute("INSERT INTO NPC VALUES(2, 'roadarmorer', 'Armorer', 'I could Talk to him', 1, 'Steel Cuirass', 300, 'Steel Axe', 200, 'road2')")

    cur.execute("INSERT INTO Object VALUES(0, 'door','cell door', 'A rusty locked cell Door.', 'Open cell Door', 1, 0, 0, 0, 1, 'cell')")
    cur.execute("INSERT INTO Object VALUES(1, 'puddle', 'cell puddle', 'A wet black shallow Puddle. Looks like there is a rusty Key in there that I could Take.', 'A wet black shallow Puddle.', 1, 0, 0, 0, 0, 'cell')")
    cur.execute("INSERT INTO Object VALUES(2, 'key', 'Rusty Key', 'A rusty Key. It could Open the cell Door.', '', 1, 1, 0, 0, 0, 'cell')")
    cur.execute("INSERT INTO Object VALUES(3, 'shutters', 'Open wooden Shutters', 'They dont seem to be locked. Maybe you could just Open them.', 'Open wooden Shutters. You can now jump to North through the window.', 1, 0, 0, 0, 0, 'hallnorth')")
    cur.execute("INSERT INTO Object VALUES(4, 'shelf', 'Book Shelf', 'There is an old Scroll in there. I could Take it.', 'Its empty.', 1, 0, 0, 0, 0, 'hallstorage')")
    #cur.execute("INSERT INTO Object VALUES(5, 'gold', 'gold1', 'You could take this gold.', NULL, 1, 1, 50, 0, 0, 'hallstorage')")
    cur.execute("INSERT INTO Object VALUES(5, 'scroll', 'Old Scroll', 'You could Take this scroll and Read it.', '', 1, 1, 0, 0, 0, 'hallstorage')")
    cur.execute("INSERT INTO Object VALUES(6, 'chains', 'Rusty Chains', 'Maybe I could Pull these Chains?', 'No need to Pull these Chains anymore.', 1, 0, 0, 0, 1, 'cell3')")
    cur.execute("INSERT INTO Object VALUES(7, 'chains', 'Rusty Chains', 'Maybe I could Pull these Chains?', 'No need to Pull these Chains anymore.', 1, 0, 0, 0, 1, 'celltombtop')")
    cur.execute("INSERT INTO Object VALUES(8, 'tree', 'Giant Tree', 'I could Cut this down if I had a Hatchet.', 'No need to Cut it down anymore.', 1, 0, 0, 0, 1, 'desertwest')")
    cur.execute("INSERT INTO Object VALUES(9, 'tree', 'Giant Tree', 'I could Cut this down if I had a Hatchet.', 'No need to Cut it down anymore.', 1, 0, 0, 0, 1, 'forestsoutheast')")
    cur.execute("INSERT INTO Object VALUES(10, 'lever', 'Tower Lever', 'A large Lever that I could Pull.', 'A pulled Lever.', 1, 0, 0, 0, 0, 'halltower')")
    cur.execute("INSERT INTO Object VALUES(11, 'boulder', 'A large Boulder', 'I could Blowup a hole in this Boulder if I had some Explosives.', 'No need to blow a hole in it anymore.', 1, 0, 0, 0, 1, 'mountain8')")
    cur.execute("INSERT INTO Object VALUES(12, 'boulder', 'A large Boulder', 'I could Blowup a hole in this Boulder if I had some Explosives.', 'No need to blow a hole in it anymore.', 1, 0, 0, 0, 1, 'mountain7')")
    cur.execute("INSERT INTO Object VALUES(13, 'explosives', 'Explosives', 'Pyromancers explosives. I could Blowup rocks with this.', NULL, 1, 1, 0, 0, 0, NULL)")
    cur.execute("INSERT INTO Object VALUES(14, 'window', 'Open Window', 'I could climb inside if I had the right tool.', 'NULL', 1, 0, 0, 0, 0, 'forests')")
    cur.execute("INSERT INTO Object VALUES(15, 'ledge', 'High Ledge', 'I could climb it if I had the right tool.', 'NULL', 1, 0, 0, 0, 0, 'mountain4')")

    cur.execute("INSERT INTO Bonfire VALUES(0, 'bonfirehallentrance', 'Bonfire', 'You can Rest at this Bonfire.', 1, 'hallentry')")
    cur.execute("INSERT INTO Bonfire VALUES(1, 'bonfireforestnorth', 'Bonfire', 'You can Rest at this Bonfire.', 1, 'forestn')")
    cur.execute("INSERT INTO Bonfire VALUES(2, 'bonfireroad3', 'Bonfire', 'You can Rest at this Bonfire.', 1, 'road3')")
    cur.execute("INSERT INTO Bonfire VALUES(3, 'bonfiredesertsouthwest', 'Bonfire', 'You can Rest at this Bonfire.', 1, 'desertsouthwest')")

    cur.execute("INSERT INTO Weapon VALUES(0, 'fists', 'Fists', 'Your hands', NULL, 0, 10, 7, 1, 1, NULL)")
    cur.execute("INSERT INTO Weapon VALUES(1, 'dagger', 'Iron Dagger', 'A sharp iron Dagger that I could Equip.', 'A sharp iron Dagger, that I could Take.', 1, 20, 9, 0, 0, 'cell2')")
    cur.execute("INSERT INTO Weapon VALUES(2, 'sword', 'Steel Sword', 'A sharp steel Sword that I could Equip.', 'A sharp steel Sword, that I could Take.', 1, 30, 8, 0, 0, 'hallarmory')")
    cur.execute("INSERT INTO Weapon VALUES(3, 'spear', 'Spear', 'A long Spear that I could Equip.', 'A long Spear, that I could Take.', 0, 40, 8, 0, 0, NULL)")
    cur.execute("INSERT INTO Weapon VALUES(4, 'hatchet', 'Hatchet', 'Hatchet I could Equip.', 'Hatchet that I could Take.', 0, 35, 7, 0, 0, NULL)")
    cur.execute("INSERT INTO Weapon VALUES(5, 'axe', 'Steel Axe', 'A steel Axe that I could Equip.', 'A steel Axe that I could Take.', 0, 50, 7, 0, 0, NULL)")
    cur.execute("INSERT INTO Weapon VALUES(6, 'zweihander', 'Zweihander', 'Zweihander. A large two handed sword that I could Equip.', 'Zweihander. A large two handed sword that I could Take.', 1, 70, 7, 0, 0, 'mountain7')")
    cur.execute("INSERT INTO Weapon VALUES(7, 'whip', 'Whip', 'A long Whip. Maybe I could throw this somewhere or use it as a weak weapon.', 'A long Whip. Could be useful.', 1, 15, 12, 0, 0, 'forestsouthwest')")
    #cur.execute("INSERT INTO Weapon VALUES(99, 'sword', 'Test Sword', 'Sharp iron Sword that I could Equip.', 'Sharp iron Sword. I should Take it with me.', 0, 200, 99, 1, 1, NULL)")

    cur.execute("INSERT INTO Shield VALUES(0, 'buckler', 'Leather Buckler', 'A small leather Buckler that I could Equip', 'A small leather Buckler that I could Take.', 1, 2, 0, 0, 'hallroom')")
    cur.execute("INSERT INTO Shield VALUES(1, 'shield', 'Steel Kite Shield', 'A standard steel kite Shield that I could Equip', 'A standard steel kite Shield that I could Take.', 1, 4, 0, 0, 'desertnortheast')")
    cur.execute("INSERT INTO Shield VALUES(2, 'greatshield', 'Dragon Greatshield', 'A massive Greatshield that I could Equip', 'A massive Greatshield that I could Take.', 1, 6, 0, 0, 'empty')")

    cur.execute("INSERT INTO Armor VALUES(0, 'cuirass', 'Steel Cuirass', 'A heavy knights armor that I could Equip', 'A heavy knights armor that I could Take.', 1, 15, 0, 0, NULL)")
    cur.execute("INSERT INTO Armor VALUES(1, 'vest', 'Leather Vest', 'A light leather Vest that I could Equip', 'A light leather Vest that I could Take.', 1, 5, 0, 0, NULL)")


    cur.execute("INSERT INTO Helmet VALUES(0, 'helmet', 'Steel Helmet', 'A steel Helmet that I could Equip', 'A steel Helmet that I could Take.', 1, 5, 0, 0, 'tombnorthwest')")
    cur.execute("INSERT INTO Helmet VALUES(1, 'insight', 'Mask of Insight', 'A weird looking mask that I could take.', 'While equipped: this mask gives me more information about my enemies.', 1, 3, 0, 0, 'hallnortheast')")

    #cur.execute("INSERT INTO Consumable VALUES(0, 'vial', 'Health Vial', 'A small healt Vial that I could Drink to restore 50 hp.', 'A small health Vial that I could Take.', 1, 50, 0, 'halleast')")
    #cur.execute("INSERT INTO Consumable VALUES(1, 'vial', 'Health Vial', 'A small healt Vial that I could Drink to restore 50 hp.', 'A small health Vial that I could Take.', 1, 50, 0, 'pitbottom')")


mainMenu()

