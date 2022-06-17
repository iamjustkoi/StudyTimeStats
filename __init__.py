import aqt.webview
from aqt import mw
from aqt.qt import QAction
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
import datetime
from .config import RTConfigManager
from .consts import Days, Text
from .options_dialog import RTOptionsDialog

delta_time = datetime.timedelta
date_time = datetime.datetime

# TODO: make addon config val
week_start_day = Days.SUNDAY
# TODO: get value from anki profile prefs
offset_hour = 6
# from aqt import preferences
# mw.col.crt

html_shell = '''    
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
        <center>
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
        </center>
'''


def build_hooks():
    from aqt import gui_hooks
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    gui_hooks.webview_did_inject_style_into_page.append(on_webview_did_inject_style_into_page)


def build_actions():
    # TODO: add key shortcut to alt menu (&[t]ime Stats)
    options_action = QAction('Overview Time Stats Options...', mw)
    options_action.triggered.connect(on_options_called)

    # Handle edge cases where toolbar action already exists
    if mw.form.menuTools.actions().__contains__(options_action):
        mw.form.menuTools.removeAction(options_action)

    mw.form.menuTools.addAction(options_action)

    mw.addonManager.setConfigAction(__name__, on_options_called)


def on_webview_will_set_content(content: aqt.webview.WebContent, context: object or None):
    if isinstance(context, (DeckBrowser, Overview)):
        content.body += formatted_html()


def on_webview_did_inject_style_into_page(webview: aqt.webview.AnkiWebView):
    if webview.page().url().path().find('congrats.html') != -1:
        webview.eval(f'if (document.getElementById("time_table") == null) document.body.innerHTML += `{formatted_html()}`')


def on_options_called():
    config_manager = RTConfigManager(mw)
    dialog = RTOptionsDialog(config_manager)
    dialog.exec()


def get_review_times() -> (float, float):
    if mw.state == 'overview':
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
    else:
        dids = mw.col.decks.allIds()

    dids_as_args = '(' + ', '.join(dids) + ')'
    cids_cmd = f'SELECT id FROM cards WHERE did in {dids_as_args}\n'
    cids = mw.col.db.all(cids_cmd)

    formatted_cids = '(' + (str(cids).replace('[', '').replace(']', '')) + ')'
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}'
    rev_log = mw.col.db.all(revlog_cmd)

    days_from_last_start = date_time.today().weekday() - week_start_day + 7
    date_of_last_start = date_time.today() - delta_time(days=days_from_last_start)
    filtered_revlog = filter_revlog(rev_log, after=date_of_last_start)

    all_rev_times_ms = [log[1] for log in rev_log[0:]]
    filtered_rev_times_ms = [log[1] for log in filtered_revlog[0:]]

    return sum(all_rev_times_ms) / 1000 / 60 / 60, sum(filtered_rev_times_ms) / 1000 / 60 / 60


def formatted_html():
    total_hrs, ranged_hrs = get_review_times()

    total_val = round(total_hrs, 2) if total_hrs > 1 else round(total_hrs * 60, 2)
    range_val = round(ranged_hrs, 2) if ranged_hrs > 1 else round(ranged_hrs * 60, 2)
    total_unit = Text.HRS if total_hrs > 1 else Text.MIN
    range_unit = Text.HRS if ranged_hrs > 1 else Text.MIN

    return html_shell.format(total_label=Text.TOTAL, range_label=Text.PAST_WEEK,
                             total_value=total_val, range_value=range_val,
                             total_unit=total_unit, range_unit=range_unit)


def offset_date(date: date_time, hours: int = offset_hour):
    return date - delta_time(hours=hours)


def filter_revlog(
        rev_logs: [[int, int]],
        days_ago: int = None,
        after: date_time = None
) -> [[int, int]]:
    print(f'check against: {offset_date(after)}')

    filtered_logs = []
    for log in rev_logs[0:]:

        log_epoch_seconds = log[0] / 1000
        log_date = offset_date(date_time.fromtimestamp(log_epoch_seconds))

        if days_ago is not None:
            log_days_ago = offset_date(date_time.now()) - log_date
            if log_days_ago.days < days_ago:
                filtered_logs.append(log)

        elif after is not None:
            log_days_after = (log_date - offset_date(after)).days
            if log_days_after >= 0:
                filtered_logs.append(log)

    return filtered_logs


def test_action():
    from aqt.utils import tooltip
    tooltip("Test")


build_hooks()
build_actions()
