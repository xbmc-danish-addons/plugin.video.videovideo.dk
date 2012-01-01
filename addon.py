#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt. If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import sys
import urllib2
import simplejson
import buggalo

import xbmcaddon
import xbmcgui
import xbmcplugin

class VideoVideoHD(object):
    INDEX_URL = 'http://videovideo.dk/index/json/'
    SHOWS_URL = 'http://videovideo.dk/shows/json/'

    def showOverview(self):
        shows = simplejson.loads(self.downloadUrl(self.SHOWS_URL))

        if ADDON.getSetting('show.teasers') == 'true':
            teasers = simplejson.loads(self.downloadUrl(self.INDEX_URL))
        else:
            teasers = None

        for show in shows:
            item = xbmcgui.ListItem(show['title'], iconImage = show['image'])
            item.setInfo(type = 'video', infoLabels = {
                'title' : show['title'],
                'plot' : show['description']
            })
            item.setProperty('Fanart_Image', show['imagefull'])
            url = PATH + '?' + show['url']
            xbmcplugin.addDirectoryItem(HANDLE, url, item, True)

        if teasers is not None:
            for teaser in teasers:
                item = xbmcgui.ListItem(teaser['headline'], iconImage = teaser['image'], thumbnailImage = teaser['image'])
                item.setInfo(type = 'video', infoLabels = {
                    'title' : teaser['headline'],
                    'plot' : teaser['text'],
                    'duration' : teaser['episode']['duration'],
                    'studio' : ADDON.getAddonInfo('name')
                })
                item.setProperty('Fanart_Image', teaser['episode']['imagefull'])
                url = teaser['episode']['distributions']['720']
                xbmcplugin.addDirectoryItem(HANDLE, url, item, False)

        xbmcplugin.endOfDirectory(HANDLE)

    def showShow(self, url):
        items = list()
        episodes = simplejson.loads(self.downloadUrl(url))
        for episode in episodes:
            item = xbmcgui.ListItem(episode['title'], iconImage = episode['image'], thumbnailImage = episode['image'])

            day = episode['timestamp'][8:10]
            month = episode['timestamp'][5:7]
            year = episode['timestamp'][0:4]

            date = '%s.%s.%s' % (day, month, year)
            aired = '%s-%s-%s' % (year, month, day)

            infoLabels = {
                'title' : episode['title'],
                'plot' : episode['shownotes'],
                'date' : date,
                'aired' : aired,
                'year' : int(year),
                'duration' : episode['duration'],
                'studio' : ADDON.getAddonInfo('name')
            }
            item.setInfo('video', infoLabels)
            item.setProperty('Fanart_Image', episode['imagefull'])
            url = episode['distributions']['720']
            items.append((url, item, False))

        xbmcplugin.addDirectoryItems(HANDLE, items)
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(HANDLE)

    def downloadUrl(self, url):
        """
        Retrieves and returns the contents of the provided url.
        Errors are not handled.

        @param self: VideoVideoHD instance
        @param url: the url to retrieve
        @return: the contents of the url
        """
        u = urllib2.urlopen(url)
        response = u.read()
        u.close()

        return response


if __name__ == '__main__':
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    HANDLE = int(sys.argv[1])
    PARAMS = sys.argv[2]

    try:
        vvd = VideoVideoHD()
        if PARAMS != '':
            vvd.showShow(PARAMS[1:]) # remove ?
        else:
            vvd.showOverview()
    except Exception:
        buggalo.onExceptionRaised()

