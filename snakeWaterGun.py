import random
def swg():
    name = input("Enter Your Name: ").capitalize()
    print(f"\nHello {name}, Wlecome to Snake,Water & Gun Game")
    user_input = input("Enter Your Choice(Snake,Water,Gun) :").capitalize()
    computer_choice = random.choice(['Snake','Water','Gun'])
    print("Computer choice :",computer_choice)
    if(user_input == computer_choice) :
        print(f"{name}, You Draw The Game !!!")
    elif(user_input == "Snake" and computer_choice == "Water"):
        print(f"{name}, You Win The Game !!!")
    elif(user_input == "Snake" and computer_choice == "Gun"):
        print(f"{name}, You Loose The Game !!!")   
    elif(user_input == "Water" and computer_choice == "Snake"):
        print(f"{name}, You Loose The Game !!!")
    elif(user_input == "Water" and computer_choice == "Gun"):
        print(f"{name}, You win The Game !!!")
    elif(user_input == "Gun" and computer_choice == "Water"):
        print(f"{name}, You Loose The Game !!!")
    elif(user_input == "Gun" and computer_choice == "Snake"):
        print(f"{name}, You Win The Game !!!")
swg()

while True:
    swg()
    again= input("Do you Want to Play again (yes/no)").lower()
    if again != "yes" :
        print("Thank you to playing")
        break
        