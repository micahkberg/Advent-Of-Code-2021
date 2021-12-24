from load import openfile
import itertools
today = "Day20"
lines = openfile(today+".txt")
algo_key = lines[0]
img = lines[2:]

class Image:
    def __init__(self, img):
        self.img = img
        self.bg = "."

    def __repr__(self):
        out = ""
        for line in self.img:
            out += line + "\n"
        return out

    def get_gamma(self, x, y):
        neighbors = list(itertools.product([-1,0,1],repeat=2))
        output = ""
        for n in neighbors:
            nx = n[1]+x
            ny = n[0]+y
            if nx in range(len(self.img[0])) and ny in range(len(self.img)):    # in y,x format because why not
                output+=self.img[ny][nx]
            else:
                output+=self.bg
        return output

    def pad(self):

        for i in range(len(self.img[0])):
            self.img[i] = self.bg*3 + self.img[i] + self.bg*3
        top_bot_pad = 3*[len(self.img[i])*self.bg]
        self.img = top_bot_pad+self.img+top_bot_pad

    def gamma_value(self, gamma):
        b = 0
        for i in range(9):
            if gamma[-(i+1)] == "#":
                b+=2**i
        return algo_key[b]

    def switch_background(self):
        self.bg = "#" if self.bg == "." else "."


    def enhance(self):
        self.pad()
        new_img = []
        for y in range(len(self.img)):
            new_line = ""
            for x in range(len(self.img[y])):
                gamma = self.get_gamma(x,y)
                new_line += self.gamma_value(gamma)
            new_img.append(new_line)
        self.img = new_img
        self.switch_background()

    def get_lit(self):
        c=0
        for i in self.img:
            for j in i:
                if j=="#":
                    c+=1
        return(c)




image = Image(img)
image.enhance()
image.enhance()
print(image.get_lit())
for i in range(48):
    image.enhance()
print(image.get_lit())
