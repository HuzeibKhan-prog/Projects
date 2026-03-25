print("---Welcome to kaun banega crorepati---")

question1 = "Which keyword is used to define a function in Python?"
option1 = ["1)func","2)def","3)define","4)function"]
print(question1)
for i in option1:
    print(i)
correct_option1 = "2"
input1 = input("Enter Your Answer:")
if(input1 == correct_option1):
    print("Correct Option!!")
    print("You won 100$")
else:
    print("Wrong Option")
    print("You loose!!")
    exit

question2 = "What will len('Python') return?"
option2 = [1,2,7,6]
print(question2)
for j in option2:
    print(j)
correct_option2 = 4
input2 = int(input("Enter Your Answer:"))
if(input2 == correct_option2):
    print("Correct Option!!")
    print("You won 200$")
else:
    print("Wrong Option")
    print("You won only 100$")
    exit

question3 = "Which of these is a valid variable name in Python?"
option3 = ["1)2value" , "2)value_2" , "3)value-2" , "4)value 2"]
print(question3)
for k in option3:
    print(k)
correct_option3 = "2"
input3 = input("Enter Your Answer:")
if(input3 == correct_option3):
    print("Correct Option!!")
    print("You won 300$")
else:
    print("Wrong Option")
    print("You won only 200$")
    exit