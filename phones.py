from urllib.request import  urlopen, Request
from urllib.parse import quote_plus, urlencode, unquote
from tkinter import*
from tkinter import font

import urllib
import urllib.request

from PIL import Image, ImageTk
from io import BytesIO



import xml.etree.ElementTree as etree
from xml.dom.minidom import parse,parseString

urlArea = 'http://apis.data.go.kr/1320000/SearchMoblphonInfoInqireService/getMoblphonAcctoKindAreaPeriodInfo'
urlDetail = 'http://apis.data.go.kr/1320000/SearchMoblphonInfoInqireService/getMoblphonDetailInfo'
key = unquote("GFWlOARL5YzjFxZQ5fAm%2BwCT1GmoJ6xr5%2FgcHhEp5swmvqdb8H8OhJp2OokP5cd%2FA9bZd%2B3QsWdODF69c7lnFQ%3D%3D")

BrandCode = {'삼성': "PRJ100", '엘지': "PRJ200", '스카이': "PRJ300", '아이폰': "PRJ400", '기타': "PRJ500"}
ColorCode = {'화이트': "CL1001", '검정': "CL1002", '빨강': "CL1003", '주황': "CL1004", '노랑': "CL1005", '초록': "CL1006",
             '파랑': "CL1007", '브라운': "CL1008", '보라': "CL1009", '기타': "CL1010"}
AreaCode = {'서울': "LCA000", '인천': "LCV000", '대구': "LCR000",
            '경기도': "LCI000", '경상북도': "LCK000", '경상남도': "LCJ000", '전라북도': "LCM000", '전라남도': "LCL000",
            '강원도': "LCH000", '울산': "LCU000", '부산': "LCT000", '광주': "LCQ000",
            '충청남도': "LCN000", '충청북도': "LCO000"}

window = Tk()
window.geometry("760x600+150+50")
fFont = font.Font(window, size=15, weight='bold', family='Consolas')

RFont = font.Font(window, size=11, family='Consolas')


def InitTopText():
    TempFont = font.Font(window, size = 20, weight = 'bold', family = 'Consolas')
    MainText =Label(window, font = TempFont , text = "핸드폰아 어디있니~?")
    MainText.place(x = 280 , y= 0)

def InitSearchAreaBox():

    global AreaEntry
    AreaEntry = Entry(window, font = fFont, width = 13)
    AreaEntry.place(x= 430 , y= 60)

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

def pageUP():
    if queryp['page'] < totalpage:
        queryp['page']  = queryp['page'] +1
        OpenURL(queryp)
        paget = str(queryp['page']) + "/" + str(totalpage)
        PageText.configure(text=paget)


def pageDOWN():
    if queryp['page'] > 1:
        queryp['page']  = queryp['page'] -1
        OpenURL(queryp)
        paget = str(queryp['page']) + "/" + str(totalpage)
        PageText.configure(text=paget)


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

def InitModelName(): #검색버튼
    global ModelEntry
    global SearchButton

    SearchButton = Button(window, command = SearchButton,text =  "검색", width = 10, height = 2 , font = fFont)
    SearchButton.place(x = 630, y = 60)



def OpenDetailURL(qeueryp):
    DetailEntry.delete('1.0', END)
    query = '?' + urlencode({quote_plus('ServiceKey'): key,
                             quote_plus('ATC_ID'): qeueryp['id'],
                             quote_plus('FD_SN'): qeueryp['num']
                             })

    tree = etree.parse(urlopen(urlDetail + query))
    root = tree.getroot()
    body = root[1]
    item = body[0]
    csteSteNm = "보관상태      :" + item.findtext('csteSteNm') + "\n"
    depPlace = "보관장소      : " +  item.findtext('depPlace') + "\n"
    fdPlace = "습득장소      : " +  item.findtext('fdPlace') + "\n"
    model = "모델          : " +  item.findtext('mdcd') + "\n"
    fdYmd = "습득일자      : " +  item.findtext('fdYmd') + "\n"
    tel = "전화번호      : " +  item.findtext('tel') + "\n"
    uniq = item.findtext('uniq')

    totaltext = csteSteNm + depPlace + fdPlace + model + fdYmd + tel + uniq
    DetailEntry.insert(END,totaltext)

def OpenURL(queryp):

    global ResultForDetail
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

    i =0 ;
    ResultForDetail = {}
    ResultList.delete(0, END)
    for item in items:
        #print("관리 ID      : ", item.findtext('atcId'))
        #print("물품분류명    : ", item.findtext('prdtClNm'))
        #print("물품명        : ", item.findtext('fdPrdtNm'))
        #print("모델코드      : ", item.findtext('mdcd'))
        #print("보관장소      : ",item.findtext('depPlace'))
        #print("습득일자      : ", item.findtext('fdYmd'))
        #print("이미지        : ",item.findtext('fdFilePathImg'))
        #print("----------------------------")
        ResultForDetail[i] = {'id':item.findtext('atcId'),'num':item.findtext('fdSn')}#id, 순번
        ResultList.insert(i,item.findtext('fdSbjt'))
        i+=1
    return body.findtext('totalCount')


def InitResultList():
    global ResultList
    global querye
    ResultBoxScrollbar = Scrollbar(window)
    ResultBoxScrollbar.place(x = 365, y = 170,width = 20, height = 370)


    ListBoxHorizon = Scrollbar(window, orient = "horizontal")
    ListBoxHorizon.place(x = 20, y  =540, width = 350, height = 20)

    ResultList = Listbox(window, font = RFont, width = 42, height = 19,
                         yscrollcommand=ResultBoxScrollbar.set,
                         xscrollcommand= ListBoxHorizon.set )
    ResultList.place(x= 20, y = 170)
    ResultList.bind('<<ListboxSelect>>',onselect)

    ResultBoxScrollbar.config(command=ResultList.yview)
    ListBoxHorizon.config(command= ResultList.xview)

def onselect(evt):
    w= evt.widget
    index = int(w.curselection()[0])
    print(ResultForDetail[index])
    OpenDetailURL( ResultForDetail[index])

def InitDetailWindow():
    global DetailEntry
    DFont = font.Font(window, size=10, family='Consolas')
    DetailEntry = Text(window, font = DFont, width = 45, height = 9)
    DetailEntry.place(x= 400 , y= 400)


def initPageButton():
    global leftButton
    global rightButton
    global PageText

    leftButton = Button(window, text = "◁", command = pageDOWN, width= 1, height = 1, font = RFont)
    leftButton.place(x= 100, y = 560)
    rightButton = Button(window, text = "▷",command = pageUP, width= 1, height = 1, font = RFont)
    rightButton.place(x= 240, y = 560)

    PageText =Label(window, font = RFont , text = "0/0")
    PageText.place(x = 165, y = 560)


def InitOtherButton():
    global EmailButton
    global MapButton
    EmailButton = Button(window, text = "E-mail", width= 10, height = 1, font = fFont)
    EmailButton.place(x = 430, y = 550)

    MapButton = Button(window, text = "보관장소 지도",font = fFont )
    MapButton.place(x = 580 , y = 550)


def SearchButton():
    global pageNum
    global totalpage
    global queryp
    brand = SearchBrandBox.get(ACTIVE)
    startymd = StartEntry.get()
    endymd = EndEntry.get()
    area = AreaEntry.get()
    color = SearchColorBox.get(ACTIVE)
    pageNum= 1
    queryp = {'keynum': key, 'Color': ColorCode[color], 'Location': AreaCode[area],
              'start': startymd, 'end': endymd, 'Brand': BrandCode[brand],
              'page': pageNum, 'numOfRows': 20}
    totalnum = int(OpenURL(queryp))
    totalpage = int(totalnum / 20)
    paget = str(pageNum) +"/"+ str(totalpage)
    PageText.configure(text = paget)


with urllib.request.urlopen("https://www.lost112.go.kr/lostnfs/images/sub/img02_no_img.gif") as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

imagelabel = Label(window, image=image, height=200, width=300)
imagelabel.pack()
imagelabel.place(x=410, y=180)


InitOtherButton()
InitSearchAreaBox()
InitResultList()
InitTopText()
InitSearchBrandBox()
InitSearchYMD()
InitSearchColorBox()
InitModelName()
initPageButton()
InitDetailWindow()


window.mainloop()