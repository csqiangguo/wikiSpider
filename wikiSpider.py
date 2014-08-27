#coding:utf-8
import urllib2
import re
from bs4 import BeautifulSoup

class wikiSpider:
    def __init__(self,url):
        self.url=url
        self.contentList=[]
        self.soup=None
        self.unicode_string=''
    def get_soup(self):
        webpage=urllib2.urlopen(self.url)
        html=webpage.read()
        self.soup=BeautifulSoup(html)
    def get_unicode_string(self):
        self.unicode_string=self.soup.get_text()
    def get_contentList(self):
        t='toclevel-'
        s='tocsection-'
        i=1
        tag=self.soup.find(class_=t+str(1)+' '+s+str(i))
        while tag:
            self.contentList.append(tag.a.get('href')[1:])
            i+=1
            tag=self.soup.find(class_=t+str(1)+' '+s+str(i))
            j=i
            while tag==None:
                i+=1
                tag=self.soup.find(class_=t+str(1)+' '+s+str(i))
                if i-j>20:
                    break
        i=0
        for str1 in self.contentList:
            strlist=re.split(r'_',str1)
            temStr=''
            for s in strlist:
                temStr=temStr+' '+s
            temStr=temStr[1:]
            self.contentList[i]=temStr
            i+=1
    def tofile(self,filename):
        f=open(filename,'w')
        for i in range(len(self.contentList)-3):
            f.write(self.contentList[i]+'\n\n')
            reStr=self.contentList[i]+'\[edit\]\n(.*)'+self.contentList[i+1]+'\[edit\]'
            m=re.search(reStr,self.unicode_string,re.S)
            f.write(m.group(1)+'\n\n')
        f.close()
def main():
    url="http://en.wikipedia.org/wiki/Machine_learning"
    filename="result.txt"
    ws=wikiSpider(url)
    ws.get_soup()
    ws.get_unicode_string()
    ws.get_contentList()
    ws.tofile(filename)
main()
if __name__=='__main__':
    main()
