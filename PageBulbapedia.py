from Commons import Commons
import re
from Page import Page
import os

class PageBulbapedia(Page):
    '''
    bulbapedia page object. For retrieving information from a bulbapedia page
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
        cacheFileName = "cache/bulbapedia/"+format(dexNum,'03')+".html"
        self.mCode = Commons.loadPage(cacheFileName,link)

    @staticmethod
    def findLink(dexNum):
        'Finds the bulbapedia link for this dex number'
        listPage = "http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
        listCode = Commons.loadPage("cache/bulbapedia_list_page.html",listPage)
        linkRegex = re.compile(format(dexNum,'03').encode()+b"[\s]</td>[\s]<td>[\s]<a href=\"([^\"]*)")
        linkMatch = linkRegex.search(listCode)
        if(linkMatch is None):
            raise Exception("cannot find link")
        linkLink = "http://bulbapedia.bulbagarden.net"+linkMatch.group(1).decode()
        return linkLink
        
    def getAnimeDexEntries(self):
        'Returns a list of dictionaries representing anime Pokedex entries.'
        animeDexRegex = re.compile('<h3><span[^>]*>[^<]*dex entries</span></h3>(.*?)<h3>',re.DOTALL|re.IGNORECASE)
        animeDexEntryRegex = re.compile('<td> *<a[^>]*>([A-Z]+[0-9]+)</a>[^<]*</td>[^<]*<td> *<strong class="selflink">[^<]*</strong>[^<]*</td>[^<]*<td>[^<]*</td>[^<]*<td>(.*?)</td>',re.DOTALL|re.IGNORECASE)
        tagRegex = Commons.tagRegex
        animeDexSearch = re.search(animeDexRegex,self.mCode)
        if(animeDexSearch is None):
            print("no anime dex section")
            return
        animeDexCode = animeDexSearch.group(1)
        outputList = []
        for animeDexEntrySearch in re.finditer(animeDexEntryRegex,animeDexCode):
            animeDexDict = {}
            animeDexDict['episode'] = animeDexEntrySearch.group(1)
            animeDexDict['entry'] = tagRegex.sub('',animeDexEntrySearch.group(2)).strip()
            outputList.append(animeDexDict)
        return outputList
