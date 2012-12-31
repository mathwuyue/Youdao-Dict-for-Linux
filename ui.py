#!/usr/bin/env python
# coding=utf-8

import gtk
import gobject
import threading
from QueryYoudao import QueryYoudao

class YoudaoMain:
    def __init__(self, api_key, key_from):
        self.queue = queue
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
        self.textviewScroller = gtk.ScrolledWindow()
        
        self.window.set_default_size(220,1)
        self.window.set_keep_above(True)
        self.window.set_title('有道迷你词典')
        self.textview.set_editable(False)
        self.textview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.textviewScroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.entry.connect('activate', self.lookupWord)
        self.window.connect('focus-in-event', self.windowFocus)
        self.window.connect('focus-out-event', self.windowLoseFocus)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.detailButton.connect('clicked', self.mlDetail)

        self.detailButton.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#2E64FE'))
        self.textviewScroller.set_border_width(8)
        self.textviewScroller.set_usize(220,266)
        
        self.hbox.pack_start(self.entry)
        self.vbox.pack_start(self.hbox, False)
        self.textviewScroller.add_with_viewport(self.textview)
        self.vbox.pack_start(self.textviewScroller)
        self.vbox.pack_start(self.detailButton, False)
        self.window.add(self.vbox)
        self.window.show_all()

        
    def lookupWord(self, *args):
        self.textviewScroller.show()
        q_thread = threading.Thread(target=self.queryObj.getBrief, args=(self.entry.get_text(), self.buffer))
        q_thread.start()

        self.detailButton.set_label('More')

        
    def windowLoseFocus(self, *args):
        self.textviewScroller.hide()
        self.detailButton.hide()
        self.window.resize(self.window.get_size()[0],1)

        
    def windowFocus(self, *args):
        self.vbox.show_all()
        self.textviewScroller.set_usize(220,266)
        self.entry.select_region(0, len(self.entry.get_text()))

        
    def mlDetail(self, widget, data=None):
        if self.entry.get_text() == '':
            return 0
        
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
    try:
        configFile = open('config','r')
        configs = configFile.read()

        api_key = configs.split('\n')[0].split('=')[1].strip()
        key_from = configs.split('\n')[1].split('=')[1].strip()

        gobject.threads_init()

        base = YoudaoMain(api_key, key_from)
        base.main()
    except IOError as ioerror:
        print ioerror
        exit()
    except IndexError:
        print 'Wrong configuration file. Abort'
        exit()
