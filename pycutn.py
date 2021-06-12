#!/usr/bin/python
import curses
from curses.textpad import rectangle, Textbox
import shelve

sh_name = '.curses_tags_notes'

def add_tag (a_tag):
    db = shelve.open (sh_name)
    klist = list (db.keys ())
    klist.sort ()
    last = '0001'
    if len (klist) > 0:
        last = '{:0>4}'.format (int (klist[len (klist)-1])+1)
    if len (a_tag) > 0:
        db[last] = [a_tag]
    db.close ()

def get_tags ():
    o = []
    db = shelve.open (sh_name)
    klist = list (db.keys ())
    klist.sort (reverse=True)
    for k in klist:
        o.append ([k, db[k][0]])
    db.close ()
    return o

def get_notes (a_tag):
    o = []
    db = shelve.open (sh_name)
    o = db[a_tag][1:]
    db.close ()
    return o[::-1]

def add_note (a_tag, nt):
    db = shelve.open (sh_name, writeback=True)
    if len (nt) > 0:
        db[a_tag].append (nt)
    db.close ()
    return 0

def run (stdscr):
    message = " Notes Started = Success "
    selnote = True
    stdscr.clear ()
    stdscr.refresh ()
    curses.start_color ()
    curses.init_pair (1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair (2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair (3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set (0)
    
    tg_y = 1
    tg_x = 0
    tg_l = curses.LINES - 2
    tg_c = 40

    mn_y = 1
    mn_x = tg_c + 1
    mn_l = tg_l
    mn_c = curses.COLS - 1

    ew_w_t = 42
    ew_w_n = curses.COLS - ew_w_t - 5
    ew_h = 1
    ew_x_t = (mn_c - ew_w_t) // 2
    ew_x_n = (mn_c - ew_w_n) // 2
    ew_y = (tg_l - ew_h) // 2

    looping = True
    conf_del = False
    input_list = 'hHjJkKlLnNeEdDqQ'
    k = 0
    update_screen = False
    sti = 0
    sni = 0
    cti = 0
    cni = 0
    cwnl = False

    while True:
        update_screen = False
        # Try to cancel quit with any key after 'Q'
        if chr (k).upper () != 'Q' and not looping:
            update_screen = True
            message = " No Input "
            looping = True
        # Try to cancel delete with any key after 'D'
        if chr (k).upper () != 'D' and conf_del:
            update_screen = True
            message = " No Input "
            conf_del = False
        if chr (k) in input_list:
            if chr (k).upper () == 'H' or chr (k).upper () == 'L':
                update_screen = True
                selnote = not selnote
            elif chr (k).upper () == 'J':
                update_screen = True
                if not selnote:
                    sni = 0
                    cni = 0
                    if cti < len (tags_list) - 1:
                        cti += 1
                    elif sti < len (get_tags ()) - tg_l + 2:
                        sti += 1
                else:
                    if cni < len (notes_list) - 1:
                        cni += 1
                    elif sni < len (get_notes (ct)) - tg_l + 2:
                        sni += 1
            elif chr (k).upper () == 'K':
                update_screen = True
                if not selnote:
                    sni = 0
                    cni = 0
                    if cti > 0:
                        cti -= 1
                    elif sti > 0:
                        sti -= 1
                else:
                    if cni > 0:
                        cni -= 1
                    elif sni > 0:
                        sni -= 1
            elif chr (k).upper () == 'Q':
                update_screen = True
                if looping:
                    looping = False
                    message = " Press q/Q again to quit. Any key to cancel "
                else:
                    break
            elif chr (k).upper () == 'N':
                update_screen = True
                if (selnote and cwnl) or not selnote:
                    if selnote:
                        top_bar = 'Edit Mode: (Press Ctrl+G to save and close)' + ' '*(1+ew_w_n-ew_w_t)
                        stdscr.addstr (ew_y-2, ew_x_n, top_bar, curses.A_REVERSE)
                        editwin = curses.newwin (ew_h, ew_w_n, ew_y, ew_x_n)
                        rectangle (stdscr, ew_y-1, ew_x_n-1, ew_y+ew_h, ew_x_n+ew_w_n+1)
                    else:
                        top_bar = 'Edit Mode: (Press Ctrl+G to save and close)'
                        stdscr.addstr (ew_y-2, ew_x_t, top_bar, curses.A_REVERSE)
                        editwin = curses.newwin (ew_h, ew_w_t, ew_y, ew_x_t)
                        rectangle (stdscr, ew_y-1, ew_x_t-1, ew_y+ew_h, ew_x_t+ew_w_t+1)
                    stdscr.refresh ()
                    box = Textbox (editwin)
                    curses.curs_set (1)
                    box.edit ()
                    curses.curs_set (0)
                    if not selnote:
                        add_tag (box.gather ().strip ())
                        cti = 0
                    else:
                        add_note (ct, box.gather ().strip ())
                        cni = 0
            elif chr (k).upper () == 'E':
                update_screen = True
                if (selnote and cwnl and len (notes_list)>0) or (len (tags_list)>0 and not selnote):
                    db = shelve.open (sh_name)
                    if selnote:
                        old_tn = db[ct][cni+1]
                    else:
                        old_tn = db[ct][0]
                    db.close ()
                    if selnote:
                        top_bar = 'Editing : (press Ctrl+G to save and close)' + ' '*(1+ew_w_n-ew_w_t)
                        stdscr.addstr (ew_y-2, ew_x_n, top_bar, curses.A_REVERSE)
                        editwin = curses.newwin (ew_h, ew_w_n, ew_y, ew_x_n)
                        rectangle (stdscr, ew_y-1, ew_x_n-1, ew_y+ew_h, ew_x_n+ew_w_n+1)
                    else:
                        top_bar = 'Editing : (press Ctrl+G to save and close)'
                        stdscr.addstr (ew_y-2, ew_x_t, top_bar, curses.A_REVERSE)
                        editwin = curses.newwin (ew_h, ew_w_t, ew_y, ew_x_t)
                        rectangle (stdscr, ew_y-1, ew_x_t-1, ew_y+ew_h, ew_x_t+ew_w_t+1)
                    stdscr.refresh ()
                    editwin.addstr (0, 0, old_tn)
                    box = Textbox (editwin)
                    curses.curs_set (1)
                    box.edit ()
                    curses.curs_set (0)
                    db = shelve.open (sh_name, writeback=True)
                    if selnote:
                        db[ct][cni+1] = box.gather ().strip ()
                    else:
                        db[ct][0] = box.gather ().strip ()
                    db.close ()
            elif chr (k).upper () == 'D':
                update_screen = True
                db = shelve.open (sh_name)
                if selnote and cwnl:
                    if len (db[ct]) > 1:
                        if not conf_del:
                            conf_del = True
                            message = " Press d/D again to confirm "
                        else:
                            tmp_list = db[ct]
                            tmp_list.pop (len (tmp_list) - cni - 1)
                            db[ct] = tmp_list
                            cni = 0
                            conf_del = False
                            message = " Note deleted successfully "
                else:
                    if len (db.keys ()) > 0:
                        if not conf_del:
                            conf_del = True
                            message = " Press d/D again to confirm "
                        else:
                            del db[ct]
                            cti = 0
                            conf_del = False
                            message = " Tag deleted successfully "
                db.close ()
        if k == 0 or update_screen:
            stdscr.clear ()
            if selnote:
                if chr (k).upper () == 'H' or chr (k).upper () == 'L':
                    message = " TAG Notes "
                rectangle (stdscr, tg_y, tg_x, tg_l, tg_c)
                stdscr.attron (curses.color_pair (2))
                rectangle (stdscr, mn_y, mn_x, mn_l, mn_c)
                stdscr.attroff (curses.color_pair (2))
            else:
                if chr (k).upper () == 'H' or chr (k).upper () == 'L':
                    message = " TAGS "
                stdscr.attron (curses.color_pair (2))
                rectangle (stdscr, tg_y, tg_x, tg_l, tg_c)
                stdscr.attroff (curses.color_pair (2))
                rectangle (stdscr, mn_y, mn_x, mn_l, mn_c)

            # Append Tags List
            i = 0
            cwnl = False
            tags_list = get_tags ()[sti:sti+tg_l-2]
            if len (tags_list) > 0:
                ct = tags_list[cti][0]
                cwnl = True
                for t in tags_list:
                    i += 1
                    if ct == t[0]:
                        stdscr.attron (curses.color_pair (2))
                        stdscr.attron (curses.A_BOLD)
                        stdscr.addstr (i+1, 2, "{: >4} : {}".format (t[0], t[1][0:tg_c-10]))
                        stdscr.attroff (curses.A_BOLD)
                        stdscr.attroff (curses.color_pair (2))
                    else:
                        stdscr.addstr (i+1, 2, "{: >4} : {}".format (t[0], t[1][0:tg_c-10]), curses.color_pair (1))

            # Append Current Tag's Notes List
            i = 0
            notes_list = []
            if cwnl:
                notes_list = get_notes (ct)[sni:sni+tg_l-2]
            if len (notes_list) > 0:
                for n in notes_list:
                    i += 1
                    if cni == i-1:
                        stdscr.addstr (i+1, tg_c+3, "-> "+n)
                    else:
                        stdscr.addstr (i+1, tg_c+3, "-  "+n)

            topbarstr = " n:new | e:edit | d:delete | h,j,k,l:move around | q:quit "
            stdscr.attron (curses.color_pair (3))
            stdscr.addstr (0, 1, topbarstr)
            stdscr.addstr (0, len (topbarstr), " " * (mn_c - len (topbarstr)))
            stdscr.attroff (curses.color_pair (3))
            statusbarstr = " {} ".format (message)
            stdscr.attron (curses.color_pair (3))
            stdscr.addstr (tg_l+1, 1, statusbarstr)
            stdscr.addstr (tg_l+1, len (statusbarstr), " " * (mn_c - len (statusbarstr)))
            stdscr.attroff (curses.color_pair (3))
            stdscr.refresh ()

        #get new keyboard press
        k = stdscr.getch ()

def main ():
    curses.wrapper (run)

if __name__ == '__main__':
    main ()
