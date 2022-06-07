from PyQt5.QtWidgets import QAction
# from anki import cards
from aqt import mw, deckbrowser

html_time = """    
        <style>
            .time-studied-header {{
                text-align: center;
                color: darkgray;
                font-size: .8em;
                font-weight: normal;
            }}

            .time-studied-row {{
                text-align: center;
                color: white;
                font-size: .8em;
                font-weight: normal;
            }}
        </style>
        <table width="70%">
            <tr>
                <th class="time-studied-header">Total Hours</th>
                <th class="time-studied-header">Past Week</th>
            </tr>
            <tr>
                <td class="time-studied-row">{}</td>
                <td class="time-studied-row">{}</td>
            </tr>
        </table>
"""


def build_hooks():
    from aqt import gui_hooks
    gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)


def on_deck_browser_will_render_content(deck_browser: deckbrowser.DeckBrowser, content: deckbrowser.DeckBrowserContent):
    total, ranged = get_deck_time_spent()
    content.stats += html_time.format(total, ranged)


def get_deck_time_spent() -> (float, float):
    if mw.state == "deckBrowser":
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))]
    else:
        dids = mw.col.decks.allIds()

    dids_as_args = "(" + ", ".join(dids) + ")"
    cids = mw.col.db.all(f'''SELECT id FROM cards WHERE did in {dids_as_args}\n''')
    formatted_cids = "(" + (str(cids).replace("[", "").replace("]", "")) + ")"

    cmd_all = f'''SELECT cid, time FROM revlog WHERE cid in {formatted_cids}'''
    rev_stats_all = mw.col.db.all(cmd_all)

    # cmd_ranged = f'''SELECT cid, time FROM revlog WHERE day >= '''
    # rev_stats_range = mw.col.db.all(cmd_ranged)

    # rev_ids_all = [i[0] for i in rev_stats_all[0:]]
    rev_times_all_ms = [i[1] for i in rev_stats_all[0:]]

    return round(sum(rev_times_all_ms) / 1000 / 60, 2), 0.0

def get_time_action():
    if mw.state == "deckBrowser":
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))]
    else:
        dids = mw.col.decks.allIds()

    dids_as_args = "(" + ", ".join(dids) + ")"
    cids = mw.col.db.all(f'''SELECT id FROM cards WHERE did in {dids_as_args}\n''')
    formatted_cids = "(" + (str(cids).replace("[", "").replace("]", "")) + ")"

    rev_stats = mw.col.db.all(f'''SELECT cid, time FROM revlog WHERE cid in {formatted_cids}''')
    rev_ids = [i[0] for i in rev_stats[0:]]
    rev_times_ms = [i[1] for i in rev_stats[0:]]

    print(f"id 1:\n {rev_ids[0]}")
    # format_id_time = time.struct_time('%Y-%m-%d %H:%M:%S', time.localtime(rev_ids[0]))

    import datetime
    format_id_time = datetime.datetime.fromtimestamp(rev_ids[-0] / 1000).strftime('%c')
    # format_id_time = datetime.datetime.fromtimestamp(1654620763302 / 1000).strftime('%c')

    print(f"today id to time: {format_id_time}")
    # tooltip(f"total: {len(rev_ids)} time (hr): {sum(rev_times_ms) / 1000 / 60}", period=6000, x_offset=50)


build_hooks()
action_stats = QAction("Get Time", mw)
action_stats.triggered.connect(get_time_action)
if mw.form.menuTools.actions().__contains__(action_stats):
    mw.form.menuTools.removeAction(action_stats)
mw.form.menuTools.addAction(action_stats)
