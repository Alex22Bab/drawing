from PIL import Image
from pynput.mouse import Button, Controller
from pynput import mouse
import keyboard
import time

hc = Controller()
colorFound = False
startClick = True
startX = 2980
endX = 3100
startY = 510
endY = 810
bX=[3000,4000]  
#bX = [3200, 4300] # GP
bY=[200,1000] 
#bY = [420, 1030] # GP

Special=[0,0]
Sp1=[0,0]
Sp2=[0,0]
Sp3=[0,0]
specialTurn=0

square = [0,0]
pencil = [0,0]
toolTurn=0

Spacement =1

gcolor = (
    (0,0,0),
    (102,102,102),
    (0,80,205),
    (255,255,255),
    (170,170,170),
    (38,201,255),
    (1,116,32),
    (153,0,0),
    (150,65,18),
    (17,176,60),
    (255,0,19),
    (255,120,41),
    (176,112,28),
    (153,0,78),
    (203,90,87),
    (255,193,38),
    (255,0,143),
    (254,175,168)
)

def on_click_for_tools(x,y,button,pressed):
    global square
    global pencil
    global toolTurn

    if pressed:
        if toolTurn == 0:
            toolTurn = 1
            pencil = [x,y]
            return True
        if toolTurn == 1:
            toolTurn = 2
            square = [x,y]
            return True
    
    if not pressed:
        # Stop listener
        return False

def on_click_for_pos(x,y,button,pressed):
        global Special
        global Sp1
        global Sp2
        global Sp3
        global specialTurn
        if pressed:
            if specialTurn == 0:
                specialTurn=1
                Special=[x,y]
                return True
            if specialTurn == 1:
                specialTurn=2
                Sp1=[x,y]
                return True
            if specialTurn == 2:
                specialTurn=3
                Sp2=[x,y]
                return True
            if specialTurn == 3:
                specialTurn=4
                Sp3=[x,y]
                return True
        if not pressed:
        # Stop listener
            return False

def on_click(x, y, button, pressed):
    global colorFound
    global startClick
    global startX
    global startY
    global endX
    global endY
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if pressed:
        if not colorFound and startClick:
            startX = x
            startY = y
            startClick = False
            return True

        if not startClick and not colorFound:
            endX = x
            endY = y  
            colorFound= True
            startClick = True
            return True

        if startClick and colorFound:
            bX[0] = x
            bY[0] = y
            startClick = False
            return True

        if not startClick and colorFound:
            bX[1] = x
            bY[1] = y
            return True

    
    if not pressed:
        # Stop listener
        return False


def cToGc(a):
    c=[]
    for i in range(len(gcolor)):
        tmp=0
        for j in range(3):
            tmp+=abs(a[j]-gcolor[i][j])
        c.append(tmp)
    return gcolor[c.index(min(c))] , c.index(min(c))


def countGC(f,sX,sY):
    res = []
    for i in range(len(gcolor)):
        res.append(0)
    for i in range(sX):
        for j in range(sY):
            res[gcolor.index(f[i,j])] += 1
    for i in range(len(res)):
        print(res[i])

def isSameColor(a,b):
    c=[]
    for i in range(3):
        c.append(abs(a[i] - b[i]))
        if c[-1] > 20:
            return False
    return True

def changeColor(color):
    hc.position = (4750,210)
    hc.press(Button.left)
    hc.release(Button.left)
    time.sleep(.1)
    keyboard.write(color)

def changeGColor(colorIndex):
    #2980, 510 => 3100, 810
    
    stepX = int((endX-startX)/2)
    stepY = int((endY-startY)/5)
    hc.position = (startX + stepX * (colorIndex%3),startY + stepY * (colorIndex//3))

    hc.press(Button.left)
    hc.release(Button.left)
    time.sleep(.1)

def changeGComplexColor(color):
    hc.position=(Special[0],Special[1])
    hc.press(Button.left)
    hc.release(Button.left)
    time.sleep(.1)

    hc.position=(Sp1[0],Sp1[1])
    hc.press(Button.left)
    hc.release(Button.left)
    tmp = str(color[0])
    keyboard.write(tmp)
    time.sleep(.1)

    hc.position=(Sp2[0],Sp2[1])
    hc.press(Button.left)
    hc.release(Button.left)
    tmp = str(color[1])
    keyboard.write(tmp)
    time.sleep(.1)

    hc.position=(Sp3[0],Sp3[1])
    hc.press(Button.left)
    hc.release(Button.left)
    tmp = str(color[2])
    keyboard.write(tmp)
    time.sleep(.1)



def valueToColor(a):
    txt = ""
    for i in range(3):
        k = hex(a[i])
        #print(str(len(k)) +" " + k)
        if len(k)==4:
            txt+=k[2]+k[3]
        elif len(k)==3:
            txt+="0"+k[2]
        else:
            #print("error\n")
            return "000000"
    #print(txt + "\n")
    return txt

def isInList(a,list):
    for i in range(len(list)):
        if isSameColor(a,list[i]):
            return i
    return -1

def readImage(name,sX,sY):
    f = Image.open(name)
    f = f.resize((int(sX),int(sY)))
    #f = f.resize(sX,sY)
    sizeX,sizeY = f.size
    f= f.load()
    return f
    
def limitColors(f,sX,sY):
    l=[]
    n=[]
    #for i in range(len(gcolor)):
    #    n.append(0)
    #    l.append(gcolor[i])

    for i in range(sX):
        for j in range(sY):
            k = isInList(f[i,j],l)
            if k <0 :
                l.append(f[i,j])
                n.append(1)
                k=len(l)-1
            else:
                f[i,j] = l[k]
                n[k]+=1
    return f,l,n

def limitGColors(f):
    n=[]
    for i in range(len(gcolor)):
        n.append(0)
    for i in range(sX):
        for j in range(sY):
            f[i,j],r = cToGc(f[i,j])
            n[r]+=1
    return f,n
    
def printImage(f,l,sX,sY,bX,bY,eX,eY):
    colored=[]
    for i in range(sX):
        tmp=[]
        for j in range(sY):
            tmp.append(0)
        colored.append(tmp)
    
    for c in range(len(l)):
        changeColor(valueToColor(l[c]))
        for i in range(sX):
            for j in range(sY):
                #print(str(f[i,j]) + " " + str(l[c]))
                if f[i,j] == l[c] and colored[i][j] == 0:
                    p = j

                    while p<sY and f[i,p] == l[c]:
                        p+=1

                    hc.position=(int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*j))
                    hc.press(Button.left)
                    
                    if p != j:
                        time.sleep(.01)
                        hc.position=(int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*p))
                    hc.release(Button.left)
                    
                    for ck in range(j,p):
                        #print(k)
                        colored[i][ck]=1
                    
                    time.sleep(.01)

def printGImage(f,n,sX,sY,bX,bY,eX,eY):
    colored=[]
    for i in range(sX):
        tmp=[]
        for j in range(sY):
            tmp.append(0)
        colored.append(tmp)
    
    for c in range(len(gcolor)):
        maxi = n.index(max(n))
        changeGColor(maxi)
        n[maxi] = -1
        for i in range(sX):
            for j in range(sY):
                #print(str(f[i,j]) + " " + str(l[c]))
                if f[i,j] == gcolor[maxi] and colored[i][j] == 0:
                    p = j
                    while p<sY and f[i,p] == gcolor[maxi]:
                        p+=1
                    hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*j))
                    hc.press(Button.left)
                    
                    if p != j:
                        hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*p))
                        time.sleep(.01)
                    hc.release(Button.left)
                    for ck in range(j,p):
                        #print(k)
                        colored[i][ck]=1
                    
                    time.sleep(.01)

def printGComplexImage(f,l,n,sX,sY,bX,bY,eX,eY,square,pencil):
    colored=[]
    sTime = time.time()
    for i in range(sX):
        tmp=[]
        for j in range(sY):
            tmp.append(0)
        colored.append(tmp)
    print(str(len(n)) + " colors")
    for c in range(len(n)):
        maxi = n.index(max(n))
        if n[maxi] > 0:
            changeGComplexColor(l[maxi])
            duration = time.time() - sTime
            #50 pixels : 1 seconde
            #1 pixel : 1/2 seconde
            left = (0.5+(1/50)*n[maxi]+(1/50000)*n[maxi]*n[maxi])*(len(n)-c)
            print("color "+str(c+1)+" / "+str(len(n))+" : "+str(n[maxi])+" pixels. "+str(int(duration))+" seconds In. " +str(int(left))+ " seconds left.")
            n[maxi] = -1
            
            if c == 0 :
                print("first color : rectangle draw")
                hc.position = (square[0],square[1])
                hc.press(Button.left)
                time.sleep(.01)
                hc.release(Button.left)
                time.sleep(.01)

                hc.position = (bX[0],bY[0])
                time.sleep(1)
                hc.press(Button.left)
                time.sleep(1)
                hc.move(eX,eY)
                time.sleep(1)
                hc.release(Button.left)
                time.sleep(1)

                hc.position = (pencil[0],pencil[1])
                hc.press(Button.left)
                time.sleep(.01)
                hc.release(Button.left)
                time.sleep(.01)
            else:
                for i in range(sX):
                    for j in range(sY):
                        #print(str(f[i,j]) + " " + str(l[c]))
                        if f[i,j] == l[maxi] and colored[i][j] == 0:
                            p = j
                            while p+1<sY and f[i,p] == l[maxi]:
                                p+=1
                            #hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*j))
                            hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*j))
                            hc.press(Button.left)
                            
                            if p != j:
                                hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*(p-1)))
                                time.sleep(.02)
                            hc.release(Button.left)
                            for ck in range(j,p):
                                #print(k)
                                colored[i][ck]=1
                            
                            time.sleep(.01)
    print("finished. "+str(int(time.time() - sTime))+" seconds.")

def printSpacement(f,l,n,sX,sY,bX,bY,eX,eY,square,pencil):
    colored=[]
    for i in range(sX):
        tmp=[]
        for j in range(sY):
            tmp.append(0)
        colored.append(tmp)
    print(str(len(n)) + " colors")
    #print("sX : "+str(sX)+" // sY : "+str(sY))
    for c in range(len(n)):
        maxi = n.index(max(n))
        if n[maxi] > 0:
            changeGComplexColor(l[maxi])
            #print("color "+str(c+1)+" : "+str(n[maxi])+" pixels")
            n[maxi] = -1
            for i in range(sX):
                for j in range(sY):
                    #print(str(f[i,j]) + " " + str(l[c]))
                    #print(i,j,maxi)
                    if f[i][j] == l[maxi] and colored[i][j] == 0:

                        hc.position = (int(bX[0]+(eX/sX)*i),int(bY[0]+(eY/sY)*j))
                        hc.press(Button.left)
                        time.sleep(.01)
                        hc.release(Button.left)
                        colored[i][j]=1
                        
                        time.sleep(.01)
    print("finished")

def simpleColorG():
    print("press color start")

    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    print("press color end")

    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    print("press draw start")

    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    print("press draw end")

    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    sX=int((bX[1] - bX[0])/7)
    sY=int((bY[1] - bY[0])/7)
    ##bX=[3000,4000]  
    #bX = [3200, 4300] # GP
    ##bY=[200,1000] 
    #bY = [420, 1030] # GP
    eX = bX[1] - bX[0]
    eY = bY[1] - bY[0]
    #
    #for i in range(len(gcolor)):
    #    changeGColor(i)
    #    time.sleep(.1)
    f = readImage("./g.jpg",sX,sY)
    ##l=gcolor
    ###f,l,n = limitColors(f)
    f,n = limitGColors(f)
    ###countGC(f,sX,sY)
    printGImage(f,n,sX,sY,bX,bY,eX,eY)

    #hc.move((3100,810),0)

def specialColorG():
    global colorFound

    print("press color special")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color R")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color G")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color B")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()
    
    

    print("where is pencil")
    with mouse.Listener(
            on_click=on_click_for_tools ) as listener:
        listener.join()

    print("where is square")
    with mouse.Listener(
            on_click=on_click_for_tools ) as listener:
        listener.join()


    colorFound = True

    print("press draw start")
    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    print("press draw end")

    with mouse.Listener(
            on_click=on_click ) as listener:
        listener.join()

    sX=int((bX[1] - bX[0])/7)
    sY=int((bY[1] - bY[0])/7)
    ##bX=[3000,4000]  
    #bX = [3200, 4300] # GP
    ##bY=[200,1000] 
    #bY = [420, 1030] # GP
    eX = bX[1] - bX[0]
    eY = bY[1] - bY[0]
    #
    #for i in range(len(gcolor)):
    #    changeGColor(i)
    #    time.sleep(.1)
    f = readImage("./g.jpg",sX,sY)
    f,l,n = limitColors(f,sX,sY)
    printGComplexImage(f,l,n,sX,sY,bX,bY,eX,eY,square,pencil)

def spacementTest():
    global Spacement
    #global bX
    #global bY
    l=[]
    n=[]
    f=[]
    for i in range(3):
        tmp2=[]
        for j in range(6):
            n.append(1)
            tmp2.append(gcolor[i*3+j])
            l.append(gcolor[i*3+j])
        f.append(tmp2)
    

    futurSpacement=[1,2,3,4,5,6,7]

    print("press color special")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color R")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color G")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    print("press color B")
    with mouse.Listener(
            on_click=on_click_for_pos ) as listener:
        listener.join()

    colorFound = True

    #print("bX0 : "+str(bX[0]) + " //bX1 : "+str(bX[1]))
    #print("press draw start")
    #with mouse.Listener(
    #        on_click=on_click ) as listener:
    #    listener.join()
    bX[0] = 2560
    bY[0] = 460
    print("bX0 : "+str(bX[0]) + " //bX1 : "+str(bX[1])+"\n")
    for i in range(len(futurSpacement)):
        print("Spacement : "+str(futurSpacement[i]))
        
        bX[0]+=(5*futurSpacement[i])
        bX[1] = bX[0] + 3*futurSpacement[i]
        bY[1] = bY[0] + 6*futurSpacement[i]
        print("bX0 : "+str(bX[0]) + " //bX1 : "+str(bX[1]))
        print("bY0 : "+str(bY[0]) + " //bY1 : "+str(bY[1]))

        sX=int(3)
        sY=int(6)
        ##bX=[3000,4000]  
        #bX = [3200, 4300] # GP
        ##bY=[200,1000] 
        #bY = [420, 1030] # GP
        eX = bX[1] - bX[0]
        eY = bY[1] - bY[0]
        printSpacement(f,l,n,sX,sY,bX,bY,eX,eY,square,pencil)
        for j in range(len(n)):
            n[j]=1




print("1 : normal // 2 : complex // 3 : Spacement Test")
a = input()
if a =='1':
    simpleColorG()
if a == '2':
    specialColorG()
if a == '3':
    spacementTest()