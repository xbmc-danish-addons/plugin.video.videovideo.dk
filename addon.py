import sys
import urllib2

import xbmcgui
import xbmcplugin

import simplejson

INDEX_URL = 'http://videovideo.dk/index/json/'
SHOWS_URL = 'http://videovideo.dk/shows/json/'

class VideoVideoHD(object):
    def showOverview(self):
        shows = simplejson.loads(self.downloadUrl(SHOWS_URL))
        teasers = simplejson.loads(self.downloadUrl(INDEX_URL))

        for show in shows:
            item = xbmcgui.ListItem(show['title'], iconImage = show['image'])
            item.setInfo(type = 'video', infoLabels = {
                'title' : show['title'],
                'plot' : show['description']
            })
            item.setProperty('Fanart_Image', show['imagefull'])
            url = PATH + '?' + show['url']
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        for teaser in teasers:
            item = xbmcgui.ListItem(teaser['headline'], iconImage = teaser['image'])
            item.setInfo(type = 'video', infoLabels = {
                'title' : teaser['headline'],
                'plot' : teaser['text'],
                'duration' : teaser['episode']['duration']
            })
            item.setProperty('Fanart_Image', teaser['episode']['imagefull'])
            url = PATH + '?' + teaser['episode']['distributions']['720']
            xbmcplugin.addDirectoryItem(HANDLE, url, item, False)


        xbmcplugin.endOfDirectory(HANDLE)

    def showShow(self, url):
        episodes = simplejson.loads(self.downloadUrl(url))
        for episode in episodes:
            item = xbmcgui.ListItem(episode['title'], iconImage = episode['image'])

            date = '%s.%s.%s' % (episode['timestamp'][8:10], episode['timestamp'][5:7], episode['timestamp'][0:4])

            infoLabels = {
                'title' : episode['title'],
                'plot' : episode['shownotes'],
                'date' : date,
                'aired' : episode['timestamp'][0:11],
                'year' : int(episode['timestamp'][0:4]),
                'duration' : episode['duration']
            }
            item.setInfo('video', infoLabels)
            item.setProperty('Fanart_Image', episode['imagefull'])
            xbmcplugin.addDirectoryItem(HANDLE, episode['distributions']['720'], item, False)

        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(HANDLE)

    def downloadUrl(self, url):
        u = urllib2.urlopen(url)
        response = u.read()
        u.close()

        return response


if __name__ == '__main__':
    vvd = VideoVideoHD()

    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = sys.argv[2]

    if PARAMS != '':
        vvd.showShow(PARAMS[1:]) # remove ?
    else:
        vvd.showOverview()

