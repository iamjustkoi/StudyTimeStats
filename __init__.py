import aqt.webview
from aqt import mw
from aqt.qt import QAction
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from datetime import timedelta, datetime, date
from .config import TimeStatsConfigManager
from .consts import Days, Text
from .options import TimeStatsOptionsDialog

# Dynamic Vars
week_start_day = Days.MONDAY
primary_color = "darkgray"
secondary_color = "white"
total_label = Text.TOTAL
range_label = Text.PAST_WEEK
# range_type = Range.WEEK
# range_days = Range.DAYS[Range.WEEK]
deckbrowser_enabled = True
overview_enabled = True
congrats_enabled = True
excluded_dids = ['1']


html_shell = '''    
        <style>
            .time-studied-header {{
                text-align: center;
                color: {primary_color};
                font-size: 1.1em;
                font-weight: normal;
            }}

            .time-studied-row {{
                text-align: center;
                color: {secondary_color};
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
    options_action = QAction(Text.OPTIONS_ACTION, mw)
    options_action.triggered.connect(on_options_called)
    # Handle edge case where toolbar action already exists
    if options_action in mw.form.menuTools.actions():
        mw.form.menuTools.removeAction(options_action)

    mw.form.menuTools.addAction(options_action)

    mw.addonManager.setConfigAction(__name__, on_options_called)


def on_webview_will_set_content(content: aqt.webview.WebContent, context: object or None):
    if mw.col is None:
        print(f'--mw was NoneType')
        return
    if (isinstance(context, DeckBrowser) and deckbrowser_enabled) or \
            (isinstance(context, Overview) and overview_enabled and should_display_on_current_screen()):
        content.body += formatted_html()


def on_webview_did_inject_style_into_page(webview: aqt.webview.AnkiWebView):
    if mw.col is None:
        print(f'--mw was NoneType')
        return
    if webview.page().url().path().find('congrats.html') != -1 and congrats_enabled:
        if should_display_on_current_screen():
            webview.eval(f'''
                if (document.getElementById("time_table") == null) document.body.innerHTML += `{formatted_html()}`''')


def on_options_called():
    dialog = TimeStatsOptionsDialog(TimeStatsConfigManager(mw))
    dialog.exec()


def should_display_on_current_screen():
    return str(mw.col.decks.current().get('id')) not in excluded_dids


def get_review_times() -> (float, float):
    print(f'mw state: {mw.state}')
    if mw.state == 'overview':
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
    else:
        dids = mw.col.decks.all_ids()

    for excluded_did in excluded_dids:
        if excluded_did in dids:
            dids.remove(str(excluded_did))

    print(f'checking dids: {[mw.col.decks.name(i) for i in dids]}')

    dids_as_args = '(' + ', '.join(dids) + ')'
    cids_cmd = f'SELECT id FROM cards WHERE did in {dids_as_args}\n'
    cids = mw.col.db.all(cids_cmd)

    formatted_cids = '(' + (str(cids).replace('[', '').replace(']', '')) + ')'
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}'
    rev_log = mw.col.db.all(revlog_cmd)

    current_date = date.today()
    if current_date.weekday() >= week_start_day:
        days_since_week_start = (current_date.weekday() - week_start_day)
    else:
        days_since_week_start = (current_date.weekday() - week_start_day) + 7

    prev_start_date = current_date - timedelta(days=days_since_week_start)
    prev_start_datetime = datetime(prev_start_date.year, prev_start_date.month, prev_start_date.day)
    filtered_revlog = filter_revlog(rev_log, after=prev_start_datetime)

    all_rev_times_ms = [log[1] for log in rev_log[0:]]
    filtered_rev_times_ms = [log[1] for log in filtered_revlog[0:]]

    return sum(all_rev_times_ms) / 1000 / 60 / 60, sum(filtered_rev_times_ms) / 1000 / 60 / 60


def formatted_html():
    total_hrs, ranged_hrs = get_review_times()

    total_val = round(total_hrs, 2) if total_hrs > 1 else round(total_hrs * 60, 2)
    range_val = round(ranged_hrs, 2) if ranged_hrs > 1 else round(ranged_hrs * 60, 2)
    total_unit = Text.HRS if total_hrs > 1 else Text.MIN
    range_unit = Text.HRS if ranged_hrs > 1 else Text.MIN

    return html_shell.format(total_label=total_label, range_label=range_label,
                             total_value=total_val, range_value=range_val,
                             total_unit=total_unit, range_unit=range_unit,
                             primary_color=primary_color, secondary_color=secondary_color)


def offset_date(dt: datetime, hours: int = 0):
    return dt + timedelta(hours=hours)


def filter_revlog(rev_logs: [[int, int]], days_ago: int = None, after: datetime = None) -> [[int, int]]:
    offset_hour = mw.col.get_preferences().scheduling.rollover
    print(f'check against: {offset_date(after, offset_hour)}')

    filtered_logs = []
    for log in rev_logs[0:]:
        log_epoch_seconds = log[0] / 1000
        log_date = datetime.fromtimestamp(log_epoch_seconds)

        if days_ago is not None:
            log_days_ago = offset_date(datetime.now(), offset_hour) - log_date
            if log_days_ago.days < days_ago:
                filtered_logs.append(log)
        elif after is not None:
            log_days_after = (log_date - offset_date(after, offset_hour)).days
            if log_days_after >= 0:
                filtered_logs.append(log)

    return filtered_logs


build_hooks()
build_actions()
