import os
from tkinter import N
health = 100
strength = 5
defense = 0
x = 0
y = 0
potion = 0
Gold = 0
base_map = [
  ["-","-","[","_","_","_","]","H","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["$","-","-","-","-","-","-","-","-","-"],
  ["-","-","[","|","|","|","]","-","-","-"],
  ["-","-","[","-","-","-","]","-","-","-"],
  ["-","-","[","_","_","_","]","-","-","-"]
]

level = [
  ["-","-","[","_","_","_","]","H","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["-","-","-","-","-","-","-","-","-","-"],
  ["$","-","-","-","-","-","-","-","-","-"],
  ["-","-","[","|","|","|","]","-","-","-"],
  ["-","-","[","-","-","-","]","-","-","-"],
  ["-","-","[","_","_","_","]","-","-","-"]
]


store_base_map = [
  [".",".",".",".","."],
  [".",".",".",".","."],
  ["N",".",".",".","."],
  [".",".",".",".","."],
  [".",".","E",".","."]
] 

level1 = [
  [".",".",".",".","."],
  [".",".",".",".","."],
  ["N",".",".",".","."],
  [".",".",".",".","."],
  [".",".","E",".","."]
] 



store_sells = ["Potion 10 Gold", "Common Sword 50 Gold", "Silver Chestplate 70 Gold", "Bow 40 Gold", "Exit"]

extra_sells = ["Potion 10 Gold", "Common Sword 50 Gold", "Silver Chestplate 70 Gold", "Bow 40 Gold", "Exit"]
location = "overworld"

while True:
  if location == "overworld":
    level[y][x] = "O"


    # Map
    for row in level:
      for c in row:
        print(c, end=" ")
      print()

    print()



    # Intro
    print(f"You are at location({x}, {y}).")
    print()
    # heal = (7,0)
    if base_map[y][x] == "H":
      print("You reached a heal point.")
      heal = input("[2] Would you like to heal? ")
      if heal == "2":
        health = 100
        print("You will be healed.")
      else:
        print("Have a good day then.")
    
    # store = (0,4)
    if base_map[y][x] == "$":
      print("You arrive at a store.")
      store = input("[1] Enter the store. ")
      if store == "1":
        location = "store"
        print("Press enter to go into the store.")


    # Walls
    
      
      print()



    # controls
    print("What direction would you like to move in?")
    print("[N]orth")
    print("[S]outh")
    print("[E]ast")
    print("[W]est")

    # move
    move = input("Move: ").upper()

    level[y][x] = base_map[y][x]
    # ai produces:

    if move == "N":
      y -= 1
    elif move == "S":
      y += 1
    elif move == "E":
      x += 1
    elif move == "W":
      x -= 1
    
    else:
      print("That is not a valid option.")

    if base_map[y][x] == "[":
      print("Oops! You hit a wall.")
      x -= 1
    if base_map[y][x] == "]":
      print("Oops! You hit a wall.")
      x += 1
    if base_map[y][x] == "|":
      print("Oops! You hit a wall.")
      y -= 1
      
    if base_map[y][x] == "_":
      print("Oops! You hit a wall.")
      y += 1



  elif location == "store":
    level1[y][x] = "O"


    # Store Map
    for row in level1:
      for c in row:
          print(c, end=" ")
      print()

    print()
    print("You are now in the store")
    
    # NPC
    if store_base_map[y][x] == "N":
      print("Would you like to buy or sell?")
      decision = input("[1] buy : [2] sell ")
      if decision == "1":
        location = "store_menu"

    if store_base_map[y][x] == "E":
      print("Would you like to exit the store?")
      a = input("Press [1] to exit store")
      if a == "1":
        location = "overworld"




    print("What direction would you like to most in?")
    print("[N]orth")
    print("[S]outh")
    print("[E]ast")
    print("[W]est")

    # move
    move = input("Move: ").upper()

    level1[y][x] = store_base_map[y][x]
    # ai produces:

    if move == "N":
      y -= 1
    elif move == "S":
      y += 1
    elif move == "E":
      x += 1
    elif move == "W":
      x -= 1
    
    else:
      print("That is not a valid option.")



  elif location == "store_menu":
    extra_sells[x] = "O"
    for c in extra_sells:
      print(c)
    print()


    print("move [N]orth or [S]outh to go up and down the shop and [P]ick your item you want to buy")
    
    
    choice = input("Move: ").upper()



    print("What would you like to buy?")
      
      

    extra_sells[x] = store_sells[x]
    if choice == "N":
          x -= 1
    elif choice == "S":
          x += 1
    elif choice == "P":
      if store_sells[x] == "Potion 10 Gold":
        if Gold < 10:
              print("You do not have enough for this item.")
        else:
              potion += 1
              Gold -= 10
      elif store_sells[x] == "Common Sword 50 Gold":
        if Gold < 50:
              print("You do not have enough for this item.")
        else:
              strength += 20
              Gold -= 50
      elif store_sells[x] == "Silver Chestplate 70 Gold":
        if Gold < 70:
              print("You do not have enough for this item.")
        else:
              defense += 30
              Gold -= 70
      elif store_sells[x] == "Bow 40 Gold":
        if Gold < 40:
              print("You do not have enough for this item.")
        else:
              strength += 15
              Gold -= 40
      elif store_sells[x] == "Exit":
          print("You are now leaving the store menu")
          location = "store"

          
  os.system("clear")