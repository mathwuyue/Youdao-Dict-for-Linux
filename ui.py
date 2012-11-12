#!/usr/bin/env python
# coding=utf-8

import gtk
from QueryYoudao import QueryYoudao

class YoudaoMain:
    def __init__(self, api_key, key_from):
        self.api_key = api_key
        self.key_from = key_from
        self.queryObj = QueryYoudao(api_key, key_from)
        
        self.window = gtk.Window()
        self.vbox = gtk.VBox()
        self.hbox = gtk.HBox()
        self.entry = gtk.Entry()
        self.textview = gtk.TextView()
        self.buffer = self.textview.get_buffer()
        self.detailButton = gtk.Button('More')
        self.buttonBox = gtk.VBox()
        
        self.window.set_default_size(220,1)
        self.window.set_keep_above(True)
        self.window.set_title('有道迷你词典')
        self.textview.set_editable(False)
        self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        
        self.entry.connect('activate', self.lookupWord)
        self.window.connect('focus-in-event', self.windowFocus)
        self.window.connect('focus-out-event', self.windowLoseFocus)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.detailButton.connect('clicked', self.mlDetail)
        
        self.hbox.add(self.entry)
        self.vbox.add(self.hbox)
        self.vbox.add(self.textview)
        self.buttonBox.add(self.detailButton)
        self.vbox.add(self.buttonBox)
        self.window.add(self.vbox)
        self.window.show_all()

        
    def lookupWord(self, *args):
        self.window.resize(220,1)
        self.textview.show()
        text = self.queryObj.getBrief(self.entry.get_text())
        self.buffer.set_text(text)

        self.detailButton.set_label('More')

        
    def windowLoseFocus(self, *args):
        self.textview.hide()
        self.buttonBox.hide()
        self.window.resize(220,1)

        
    def windowFocus(self, *args):
        self.textview.show()
        self.buttonBox.show()
        self.entry.select_region(0, len(self.entry.get_text()))

        
    def mlDetail(self, widget, data=None):
        if self.detailButton.get_label() == 'More':
            bounds = self.buffer.get_bounds()
            word = self.entry.get_text()
            text = '\n\n' + self.queryObj.getDetail(word)
            self.buffer.insert(bounds[1], text)
            self.detailButton.set_label('Less')
        else:
            self.detailButton.set_label('More')
            self.lookupWord()

            
    def delete_event(self, widget, event, data=None):
        return False

    
    def destroy(self, widget, data=None):
        gtk.main_quit()

        
    def main(self):
        gtk.main()


        
if __name__ == "__main__":
    configFile = open('config','r')
    configs = configFile.read()

    try:
        api_key = configs.split('\n')[0].split('=')[1].strip()
        key_from = configs.split('\n')[1].split('=')[1].strip()
        base = YoudaoMain(api_key, key_from)
        base.main()
    except:
        print 'Wrong configuration file. Abort'
        exit()
