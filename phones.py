
from urllib.request import  urlopen, Request
from urllib.parse import quote_plus, urlencode, unquote
from tkinter import*
from tkinter import font

import xml.etree.ElementTree as etree
from xml.dom.minidom import parse,parseString

urlArea = 'http://apis.data.go.kr/1320000/SearchMoblphonInfoInqireService/getMoblphonAcctoKindAreaPeriodInfo'
urlDetail = 'http://apis.data.go.kr/1320000/SearchMoblphonInfoInqireService/getMoblphonDetailInfo'
key = unquote("GFWlOARL5YzjFxZQ5fAm%2BwCT1GmoJ6xr5%2FgcHhEp5swmvqdb8H8OhJp2OokP5cd%2FA9bZd%2B3QsWdODF69c7lnFQ%3D%3D")


window = Tk()
window.geometry("800x600+150+50")
fFont = font.Font(window, size=15, weight='bold', family='Consolas')

RFont = font.Font(window, size=10, family='Consolas')

def InitTopText():
    TempFont = font.Font(window, size = 20, weight = 'bold', family = 'Consolas')
    MainText =Label(window, font = TempFont , text = "핸드폰아 어디있니~?")
    MainText.place(x = 280 , y= 0)

def InitSearchAreaBox():

    global AreaEntry
    AreaEntry = Entry(window, font = fFont, width = 13)
    AreaEntry.place(x= 450 , y= 60)

    AreaText = Label(window, font = fFont, text=  "지역 : ")
    AreaText.place(x = 350, y = 60)

def InitSearchBrandBox():
    global SearchBrandBox


    BrandText =Label(window, font = fFont , text = "브랜드: ")
    BrandText.place(x = 0, y = 100)

    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.place(x = 150, y = 95)

    SearchBrandBox = Listbox(window, font=fFont, activestyle='none',
                            width=6, height=1, borderwidth=1, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    SearchBrandBox.insert(1, "삼성")
    SearchBrandBox.insert(2, "엘지")
    SearchBrandBox.insert(3, "스카이")
    SearchBrandBox.insert(4, "아이폰")
    SearchBrandBox.insert(5, "기타")
    SearchBrandBox.place(x=80, y =100)

    ListBoxScrollbar.config(command=SearchBrandBox.yview)


def InitSearchColorBox():
    global SearchColorBox


    ColorText =Label(window, font = fFont , text = "색상: ")
    ColorText.place(x = 180, y = 100)

    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.place(x = 310, y = 95)

    SearchColorBox = Listbox(window, font=fFont, activestyle='none',
                            width=6, height=1, borderwidth=1, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    SearchColorBox.insert(1, "화이트")
    SearchColorBox.insert(2, "검정")
    SearchColorBox.insert(3, "빨강")
    SearchColorBox.insert(4, "주황")
    SearchColorBox.insert(5, "노랑")
    SearchColorBox.insert(6, "초록")
    SearchColorBox.insert(7, "파랑")
    SearchColorBox.insert(8, "브라운")
    SearchColorBox.insert(9, "보라")
    SearchColorBox.insert(10, "기타")
    SearchColorBox.place(x=240, y=100)

    ListBoxScrollbar.config(command=SearchColorBox.yview)




def InitSearchYMD():
    global StartEntry, EndEntry
    StartEntry = Entry(window, font = fFont, width = 9)
    StartEntry.place(x= 60, y=60)

    EndEntry = Entry(window, font = fFont, width = 9)
    EndEntry.place(x= 190, y=60)

    BrandText =Label(window, font = fFont , text = "기간:")
    BrandText.place(x = 0, y = 60)

    BrandText2 =Label(window, font = fFont , text = "~")
    BrandText2.place(x = 168, y = 60)

def InitModelName(): #검색버튼도 있음
    global ModelEntry
    global SearchButton

    SearchButton = Button(window, text =  "검색", width = 10, height = 2 , font = fFont)
    SearchButton.place(x = 630, y = 60)

    ModelEntry = Entry(window, font = fFont, width = 13)
    ModelEntry.place(x= 450 , y= 100)

    ModelText = Label(window, font = fFont, text=  "모델명 : ")
    ModelText.place(x = 350, y = 100)

def OpenURL(queryp):

    query = '?' + urlencode({quote_plus('ServiceKey'): queryp['keynum'],
                             quote_plus('COL_CD'): queryp['Color'],
                             quote_plus('FD_LCT_CD'): queryp['Location'],
                             quote_plus('START_YMD'): queryp['start'],
                             quote_plus('END_YMD'): queryp['end'],
                             quote_plus('PRDT_CL_CD_02'):queryp['Brand'],
                             quote_plus('pageNo'): queryp['page'],
                             quote_plus('numOfRows'): queryp['numOfRows'],
                             })

    tree = etree.parse(urlopen(urlArea + query))
    root = tree.getroot()
    body = root[1]
    items = body[0]
    for item in items:
        print(item.findtext('fdSbjt'))
        print("관리 ID      : ", item.findtext('atcId'))
        print("물품분류명    : ", item.findtext('prdtClNm'))
        print("물품명        : ", item.findtext('fdPrdtNm'))
        print("모델코드      : ", item.findtext('mdcd'))
        print("보관장소      : ",item.findtext('depPlace'))
        print("습득일자      : ", item.findtext('fdYmd'))
        print("이미지        : ",item.findtext('fdFilePathImg'))
        print("----------------------------")

    return body.findtext('totalCount')


def InitResultList():
    global ResultList

    ResultBoxScrollbar = Scrollbar(window)
    ResultBoxScrollbar.place(x = 365, y = 170,width = 30, height = 370)

    ResultList = Listbox(window, font = RFont, width = 50, height = 23, yscrollcommand=ResultBoxScrollbar.set)
    ResultList.place(x= 20, y = 170)

    ResultBoxScrollbar.config(command=ResultList.yview)



def printMain():
    BrandCode = {'삼성': "PRJ100",'엘지':"PRJ200",'스카이':"PRJ300",'아이폰':"PRJ400",'기타':"PRJ500"}
    ColorCode = {'화이트':"CL1001",'검정':"CL1002",'빨강':"CL1003",'주황':"CL1004",'노랑':"CL1005",'초록':"CL1006",'파랑':"CL1007",'브라운':"CL1008",'보라':"CL1009",'기타':"CL1010"}

    print("핸드폰아 어디있니 ~~~?")
    print("============MENU===========")
    startymd = input("검색 시작일 : ")
    endymd = input("검색 종료일 : ")
    brand = input("브랜드 : ")
    color = input("색상: ")
    pageNum = 1
    inputPage = 'a'
    while(True):
        queryp = {'keynum': key, 'Color' : ColorCode[color], 'Location' : 'LCA000',
               'start' : startymd, 'end': endymd, 'Brand':BrandCode[brand],
                 'page' : pageNum, 'numOfRows' : 20}
        totalnum = OpenURL(queryp)
        totalPage = int(int(totalnum)/20)
        if totalPage ==0 :
            totalPage = 1
        print("(",pageNum,"/",totalPage,") 이전 페이지 : a, 다음 페이지 : d")
        inputPage = input()
        if inputPage == 'a':
            if(pageNum > 1):
                pageNum -= 1
        elif inputPage == 'd':
            if(pageNum < totalPage):
                pageNum += 1
        else:
            break

def InitDetailWindow():
    global imageLabel
    photo = PhotoImage(file="Default.gif")
    imageLabel = Label(window, image=photo)
    imageLabel.place(x = 0, y = 0)

    global DetailEntry
    DetailText = Text(window, font = RFont, width = 50, height = 9)
    DetailText.place(x= 400 , y= 400)


def InitOtherButton():
    global EmailButton
    global MapButton
    EmailButton = Button(window, text = "E-mail", width= 10, height = 1, font = fFont)
    EmailButton.place(x = 430, y = 550)

    MapButton = Button(window, text = "보관장소 지도",font = fFont )
    MapButton.place(x = 580 , y = 550)



re = 'a'
while(re == 'a'):
    printMain()
    re = input("계속 (a) : ")

    
InitOtherButton()
InitSearchAreaBox()
InitDetailWindow()
InitResultList()
InitTopText()
InitSearchBrandBox()
InitSearchYMD()
InitSearchColorBox()
InitModelName()
window.mainloop()
