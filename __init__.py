# import aqt.preferences
from PyQt5.QtWidgets import QAction
# from anki import cards
from aqt import mw, deckbrowser
import datetime

delta_time = datetime.timedelta
date_time = datetime.datetime


class Text:
    TOTAL = "Total"
    PAST_WEEK = "Past Week"
    HRS = "hrs"
    MIN = "min"


class Day:
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


# from pytz import timezone
# from aqt import preferences
# mw.col.conf
# mw.col.crt
# TODO: get value from addon config
week_start_day = Day.SUN
# TODO: get value from anki preferences
offset_hour = 6

html_time = """    
        <style>
            .time-studied-header {{
                text-align: center;
                color: darkgray;
                font-size: 1.1em;
                font-weight: normal;
            }}

            .time-studied-row {{
                text-align: center;
                color: white;
                font-size: 1.1em;
                font-weight: normal;
            }}
        </style>
        <table width="60%%" id="time_table" style="margin: 12px;">
            <tr>
                <th class="time-studied-header">{total_label}</th>
                <th class="time-studied-header">{range_label}</th>
            </tr>
            <tr>
                <td class="time-studied-row">{total_value} {total_unit}</td>
                <td class="time-studied-row">{range_value} {range_unit}</td>
            </tr>
        </table>
"""


def build_hooks():
    from aqt import gui_hooks
    gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)


# TODO: add to overview page
# TODO: add to congrats page

def on_deck_browser_will_render_content(deck_browser: deckbrowser.DeckBrowser, content: deckbrowser.DeckBrowserContent):
    total, ranged = get_review_times()

    total_val = round(total, 2)
    total_unit = Text.HRS

    if ranged > 1:
        ranged_value = round(ranged, 2)
        range_unit = Text.HRS
    else:
        ranged_value = round(ranged * 60, 2)
        range_unit = Text.MIN

    content.stats += html_time.format(total_label=Text.TOTAL, range_label=Text.PAST_WEEK,
                                      total_value=total_val, range_value=ranged_value,
                                      total_unit=total_unit, range_unit=range_unit)


def get_review_times() -> (float, float):
    if mw.state == "overview":
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))]
    else:
        dids = mw.col.decks.allIds()

    dids_as_args = "(" + ", ".join(dids) + ")"
    cids_cmd = f'SELECT id FROM cards WHERE did in {dids_as_args}\n'
    cids = mw.col.db.all(cids_cmd)

    formatted_cids = "(" + (str(cids).replace("[", "").replace("]", "")) + ")"
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}'
    rev_log = mw.col.db.all(revlog_cmd)

    days_from_last_start = date_time.today().weekday() - week_start_day + 7
    date_of_last_start = date_time.today() - delta_time(days=days_from_last_start)
    filtered_revlog = filter_revlog(rev_log, after=date_of_last_start)

    all_rev_times_ms = [log[1] for log in rev_log[0:]]
    filtered_rev_times_ms = [log[1] for log in filtered_revlog[0:]]

    return sum(all_rev_times_ms) / 1000 / 60 / 60, sum(filtered_rev_times_ms) / 1000 / 60 / 60


def offset_date_hour(date: date_time, offset: int = offset_hour):
    return date - delta_time(hours=offset)


def filter_revlog(
        rev_logs: [[int, int]], days_ago: int = None, after: date_time = None
) -> [[int, int]]:

    print(f'check against: {offset_date_hour(after)}')

    filtered_logs = []
    for log in rev_logs[0:]:

        log_epoch_seconds = log[0] / 1000
        log_date = offset_date_hour(date_time.fromtimestamp(log_epoch_seconds))

        if days_ago is not None:
            log_days_ago = offset_date_hour(date_time.now()) - log_date
            if log_days_ago.days < days_ago:
                filtered_logs.append(log)

        elif after is not None:
            log_days_after = (log_date - offset_date_hour(after)).days
            if log_days_after >= 0:
                filtered_logs.append(log)

    return filtered_logs


def test_action():
    if mw.state == "overview":
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get("id"))]
    else:
        dids = mw.col.decks.allIds()

    dids_as_args = "(" + ", ".join(dids) + ")"
    cids = mw.col.db.all(f'SELECT id FROM cards WHERE did in {dids_as_args}\n')
    formatted_cids = "(" + (str(cids).replace("[", "").replace("]", "")) + ")"

    # Result: [ [ids(time of study), ...], [time(time elapsed), ...] ]
    rev_logs = mw.col.db.all(f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}')

    names = [mw.col.decks.name(i) for i in dids]
    print(f'dids: {dids_as_args}')
    print(f'dnames: {names}')

    filtered_revlog = filter_revlog(rev_logs, days_ago=7)
    filtered_rev_times_ms = [i[1] for i in filtered_revlog[0:]]

    print(round(sum(filtered_rev_times_ms) / 1000 / 60 / 60, 2))


build_hooks()
action_stats = QAction("Timelog Test", mw)
action_stats.triggered.connect(test_action)
if mw.form.menuTools.actions().__contains__(action_stats):
    mw.form.menuTools.removeAction(action_stats)
mw.form.menuTools.addAction(action_stats)
