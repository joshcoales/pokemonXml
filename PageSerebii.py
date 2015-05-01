from Commons import Commons
from Page import Page

class PageSerebii(Page):
    '''
    serebii page object. For retrieving information from a serebii page
    '''
    mDexNum = None  #(National) Pokedex number of pokemon
    mLink = None    #Page link
    mCode = None    #Code of page


    def __init__(self,dexNum,link=None):
        '''
        Constructor
        '''
        self.mDexNum = dexNum
        if(link is None):
            link = self.findLink(dexNum)
        self.mLink = link
        try:
            cacheFile = open("cache/serebii/"+format(dexNum,'03')+".html","rb")
            self.mCode = cacheFile.read()
        except:
            self.mCode = Commons.downloadPage(link)
            open("cache/serebii/"+format(dexNum,'03')+".html","wb").write(self.mCode)

    @staticmethod
    def findLink(dexNum):
        'Finds the serebii page link for this dex number'
        return "http://www.serebii.net/pokedex-xy/"+format(dexNum,'03')+".shtml"