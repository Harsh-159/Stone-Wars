import pygame
import math
import random
import time

pygame.init()
screen=pygame.display.set_mode((1300,730),pygame.FULLSCREEN)
pygame.display.set_caption('Space Wars')
font=pygame.font.SysFont('arial',110)
running=True
w=0
clock=pygame.time.Clock()
screen.fill((0,0,0))
while w<180:
    w+=1
    option = font.render("I welcome u to Stone wars", True, (255, 255, 255))
    screen.blit(option, (50, 300))
    clock.tick(60)
    pygame.display.update()
def game():
    ship=pygame.image.load('Ship.png')
    sh=pygame.transform.rotate(ship,0)
    sx=650
    sy=290
    sx_change=0
    sy_change=0
    no_of_enemy=40
    no_of_bullet=18

    dil=pygame.image.load('Heart.png')
    dil=pygame.transform.scale(dil,(20,20))
    pubull=pygame.image.load('pickupbullet.png')
    ene=pygame.image.load('Enemy.png')
    bene=pygame.image.load('bigenemy.png')
    bull=pygame.image.load('bullet.png')
    bomb=pygame.image.load('Grenade.png')
    bx=0
    by=0
    bomb_dropped=False
    detonate=False
    detonate_count=1
    enemi=[]
    enemix=[]
    enemiy=[]
    enemix_change=[]
    enemiy_change=[]
    enemi_angle=['']*no_of_enemy
    bullet=['']*no_of_bullet*10
    bulletx=['']*no_of_bullet*10
    bullety=['']*no_of_bullet*10
    bulletx_change=['']*no_of_bullet*10
    bullety_change=['']*no_of_bullet*10
    bullet_angle=['']*no_of_bullet*10
    stock=[]
    fired=[]
    available_enemy=[]
    enemi_health=['']*no_of_enemy
    life=[]
    lifex=[]
    lifey=[]
    magazine=[]
    magazinex=[]
    magaziney=[]
    bomb_particle = []
    white=(255,255,255)
    red=(255,0,0)
    particles=[]
    spacy=[]

    for i in range(250):
        spacy.append([random.randint(0,1300),random.randint(0,730)])

    #pygame.mixer.music.load('background.mp3')
    #pygame.mixer.music.play(-1)
    def part(px,py,color):
        if color=='red':
            for j in range(12):
                particles.append([[px, py], [random.randint(0,20)/10-1, random.randint(0,20)/10-1], 6,color])
        elif color=='blue':
            for j in range(12):
                particles.append([[px, py], [random.randint(0,20)/10-1, random.randint(0,20)/10-1], 9,color])
    def pos():
        lstx=[0,350,725,1100,1250]
        lsty=[0,680]
        random.shuffle(lstx)
        random.shuffle(lsty)
        return lstx[0],lsty[0]

    def enemy(ene,ex,ey):
        screen.blit(ene,(ex,ey))

    def choosene():
        lst=[0,1,1,1,]
        random.shuffle(lst)
        if lst[0]==0:
            return bene
        else:
            return ene

    for i in range(no_of_enemy):
        enemi.append(choosene())
        if enemi[i]==bene:
            enemi_health[i]=3
        c,d=pos()
        enemix.append(c)
        enemiy.append(d)
        enemix_change.append(0)
        enemiy_change.append(0)

    def chance():
        lst=[0,1,2]
        random.shuffle(lst)
        if lst[0]==0:return True
        else:return False

    for i in range(no_of_bullet):
        stock.append(i)

    def fire(n,angle):
        bulletx[n]=sx
        bullety[n]=sy
        bullet_angle[n]=angle
        if sx>mx:
            bullet[n]=pygame.transform.rotate(bull,90-bullet_angle[n])
            bulletx_change[n]=-5*math.cos(math.radians(bullet_angle[n]))
            bullety_change[n]=-5*math.sin(math.radians(bullet_angle[n]))
        else:
            bullet[n]=pygame.transform.rotate(bull,-90-bullet_angle[n])
            bulletx_change[n] = 5 * math.cos(math.radians(bullet_angle[n]))
            bullety_change[n] = 5 * math.sin(math.radians(bullet_angle[n]))

    def slope(x1,y1,x2,y2):
        if x2==x1:
            return 1000
        else:
            return (y2-y1)/(x2-x1)
    def hero(ship,sx,sy):
        screen.blit(ship,(sx,sy))
    q=0
    main_clock=pygame.time.Clock()
    running=True
    p=0
    r=0
    s=0
    t=10
    heart=3
    possible=False

    while running:
        screen.fill((0, 0, 0))
        q+=1
        if p < no_of_enemy-1 and q>120:
            q-=120
            available_enemy.append(p)
            available_enemy.append(p+1)
            p += 2
        mx, my = pygame.mouse.get_pos()

        # def some terms
        sx += sx_change
        sy += sy_change
        m = slope(sx, sy, mx, my)
        angle = math.degrees(math.atan(m))

        #keyboard input
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running=False
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_d:
                    sx_change=3
                elif e.key==pygame.K_a:
                    sx_change=-3
                elif e.key==pygame.K_w:
                    sy_change=-3
                elif e.key==pygame.K_s:
                    sy_change=3
                elif e.key==pygame.K_q:
                    sx_change=0
                    sy_change=0
                elif e.key==pygame.K_ESCAPE:
                    running=False
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if e.button==1:
                    if len(stock)>0:
                        fire(stock[0],angle)
                        fired.append(stock.pop(0))
                    sx-=4*bulletx_change[fired[-1]]
                    sy-=4*bullety_change[fired[-1]]
                elif e.button==3 :
                    if not bomb_dropped:
                        bx = sx
                        by = sy
                        bomb_dropped=True
                    else:
                        detonate=True

        #enemy follows
        for i in available_enemy:
            enemi_angle[i]=(math.degrees(math.atan(slope(enemix[i],enemiy[i],sx,sy))))
            if enemix[i]>sx:
                enemix_change[i]=-2*(math.cos(math.radians(enemi_angle[i])))
                enemiy_change[i]=-2*(math.sin(math.radians(enemi_angle[i])))
            elif enemix[i]<sx:
                enemix_change[i] = 2 * (math.cos(math.radians(enemi_angle[i])))
                enemiy_change[i] = 2 * (math.sin(math.radians(enemi_angle[i])))
            else:
                if enemiy[i]>sy:
                    enemiy_change[i]=-2
                else:
                    enemiy_change[i]=2
            enemix[i] += enemix_change[i]
            enemiy[i] += enemiy_change[i]

        #rotate
        if my>=sy:
            if mx>=sx:
                sh=pygame.transform.rotate(ship,-90-angle)

            else:
                sh=pygame.transform.rotate(ship,90-angle)
        else:
            if mx>=sx:
                sh=pygame.transform.rotate(ship,-90-angle)
            else:
                sh=pygame.transform.rotate(ship,90-angle)

        #bullet implementation
        for i in fired:
            screen.blit(bullet[i],(bulletx[i],bullety[i]))
            bulletx[i]+=bulletx_change[i]
            bullety[i]+=bullety_change[i]
            for j in available_enemy:
                if enemi[j]==ene:
                    if 15>bulletx[i]-enemix[j]>-15 and 15>bullety[i]-enemiy[j]>-15:
                        part(bulletx[i],bullety[i],'red')
                        if chance():
                            magazine.append(s)
                            magazinex.append(enemix[j])
                            magaziney.append(enemiy[j])
                            s+=1
                        enemi[j]=['']
                        fired.remove(i)
                        available_enemy.remove(j)
                        break
                else:
                    if 25>bulletx[i]-enemix[j]>-25 and 25>bullety[i]-enemiy[j]>-25:
                        enemi_health[j]-=1
                        if enemi_health[j]==0:
                            part(bulletx[i], bullety[i], 'blue')
                            if chance():
                                life.append(r)
                                lifex.append(enemix[j])
                                lifey.append(enemiy[j])
                                r += 1
                            enemi[j]=['']
                            available_enemy.remove(j)
                        fired.remove(i)
                        break

        #boundary conditions
        if sx>1250:
            sx_change=0
            sx=1250
        elif sx<0:
            sx_change=0
            sx=0
        if sy>680:
            sy_change=0
            sy=680
        elif sy<0:
            sy_change=0
            sy=0


        #collision with enemy
        for i in available_enemy:
                enemy(enemi[i],enemix[i],enemiy[i])
                if enemi[i]==ene:
                    if 15>enemix[i]-sx>-15 and 15>enemiy[i]-sy>-15:
                        heart-=1
                        enemi[i] = ''
                        available_enemy.remove(i)
                        if heart<1:
                            screen.fill((0,0,0))
                            option = font.render("You Lose", True, (255, 255, 255))
                            screen.blit(option, (470, 300))
                            pygame.display.update()
                            time.sleep(2)
                            running=False
                        elif chance():
                            magazine.append(s)
                            magazinex.append(sx)
                            magaziney.append(sy)
                            s+=1
                        for j in range(12):
                            particles.append([[sx, sy], [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1], 6, 'red'])

                else:
                    if 25>enemix[i]-sx>-25 and 25>enemiy[i]-sy>-25:
                        heart -= 2
                        if heart <1:
                            option = font.render("You Lose", True, (255, 255, 255))
                            screen.fill((0,0,0))
                            screen.blit(option, (470, 300))
                            pygame.display.update()
                            time.sleep(2)
                            running = False
                        else:
                            if chance():
                                life.append(r)
                                lifex.append(sx)
                                lifey.append(sy)
                                r += 1
                            for j in range(12):
                                particles.append([[sx, sy], [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1], 9, 'blue'])
                            enemi[i]=''
                            available_enemy.remove(i)
        #heart left
        for i in life:
            screen.blit(dil,(lifex[life.index(i)],lifey[life.index(i)]))
        #picking heart
        for i in life:
            if 15>sx-lifex[life.index(i)]>-15 and 15>sy-lifey[life.index(i)]>-15:
                heart+=1
                lifex.remove(lifex[life.index(i)])
                lifey.remove(lifey[life.index(i)])
                life.remove(i)
                break
        #magazine left
        for i in range(len(magazine)):
            screen.blit(pubull,(magazinex[i],magaziney[i]))
        #picking magazine

        for i in magazine:
            if 25>sx-magazinex[magazine.index(i)]>-25 and 25>sy-magaziney[magazine.index(i)]>-25:
                stock.extend([t,t+1,t+2,t+3])
                t+=4
                magazinex.pop(magazine.index(i))
                magaziney.pop(magazine.index(i))
                magazine.remove(i)
                break

        for particle in particles:
            particle[0][0]+=particle[1][0]
            particle[0][1]+=particle[1][1]
            particle[2]-=0.2
            if particle[3]=='red':
                pygame.draw.circle(screen,(255,0,0),(int(particle[0][0]),int(particle[0][1])),int(particle[2]))
            elif particle[3]=='blue':
                pygame.draw.circle(screen, (0, 0, 255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))
            if particle[2]<=0:
                particles.remove(particle)
                break
        for star in spacy:
            pygame.draw.circle(screen,(255,255,255),(star[0],star[1]),random.randint(1,3))

        if no_of_enemy-2 in available_enemy:
            possible=True

        if len(available_enemy)==0 and possible and running:
            screen.fill((0, 0, 0))
            option = font.render("You Win", True, (255, 255, 255))
            screen.blit(option, (500, 300))
            pygame.display.update()
            time.sleep(2)
            running=False

        fon=pygame.font.SysFont('arial',30)
        health=fon.render("Hearts remaining="+str(heart),True,(255,0,0))
        ammo=fon.render("Bullets remaining="+str(len(stock)),True,(255,0,0))

        if bomb_dropped and not detonate:
            screen.blit(bomb,(bx,by))
        if detonate and detonate_count>0:
            detonate_count-=1

            for i in range(15):
                for j in available_enemy:
                    if 50>bx-enemix[j]>-75 and 50>by-enemiy[j]>-75:
                        if enemi[j]==ene and chance():
                            magazine.append(s)
                            magazinex.append(enemix[j])
                            magaziney.append(enemiy[j])
                            s += 1
                        elif enemi[j]==bene and chance():
                            life.append(r)
                            lifex.append(enemix[j])
                            lifey.append(enemiy[j])
                            r += 1
                        enemi[j] = ['']
                        available_enemy.remove(j)
                        break

                colours = [(255, 0, 0), (237, 119, 0), (255, 251, 0)]
                random.shuffle(colours)
                bomb_particle.append([[bx,by],[random.randint(0,20)/10-1, random.randint(0,20)/10-1], 18,colours[0]])
        if len(bomb_particle)>0:
            for particle in bomb_particle:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.2
                pygame.draw.circle(screen, particle[3], (int(particle[0][0]), int(particle[0][1])),int(particle[2]))
                if particle[2] <= 0:
                    bomb_particle.remove(particle)
                    break
        screen.blit(health,(0,0))
        screen.blit(ammo,(0,30))
        hero(sh,sx,sy)
        main_clock.tick(60)
        pygame.display.update()
game()

running=True
while running:
    screen.fill((0,0,0))
    option=font.render("Do u wanna play again:(Y/N)",True,(255,255,255))
    screen.blit(option,(0,300))
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_ESCAPE:
                running=False
            elif e.key==pygame.K_y:
                game()
            elif e.key==pygame.K_n:
                running=False
        pygame.display.update()