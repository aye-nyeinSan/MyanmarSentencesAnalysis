from external.myWord.myword import tokenize_text

text = "ကျွန်တော်မြန်မာစာကို စမ်းသပ်နေပါတယ်။"
tokens = tokenize_text(text)
print(tokens)

with open("output.txt", "w") as f:
    f.write(tokens)
