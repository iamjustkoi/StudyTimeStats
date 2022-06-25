import aqt.webview
from aqt import mw
from aqt.qt import QAction
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from datetime import timedelta, datetime, date
from .config import TimeStatsConfigManager
from .consts import Days, Text, Range
from .options import TimeStatsOptionsDialog

# Dynamic Vars
Week_Start_Day = Days.SATURDAY
Range_Type = Range.WEEK
Use_Calendar_Range = True
Range_Days = Range.TOTAL_DAYS[Range_Type]
Primary_Color = "darkgray"
Secondary_Color = "white"
Total_Label = Text.TOTAL
Range_Label = Text.PAST_WEEK
Custom_Days = 12
Deckbrowser_Enabled = True
Overview_Enabled = True
Congrats_Enabled = True
Excluded_DIDs = ['1']


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
    if (isinstance(context, DeckBrowser) and Deckbrowser_Enabled) or \
            (isinstance(context, Overview) and Overview_Enabled and should_display_on_current_screen()):
        content.body += formatted_html()


def on_webview_did_inject_style_into_page(webview: aqt.webview.AnkiWebView):
    if mw.col is None:
        print(f'--mw was NoneType')
        return
    if webview.page().url().path().find('congrats.html') != -1 and Congrats_Enabled:
        if should_display_on_current_screen():
            webview.eval(f'''
                if (document.getElementById("time_table") == null) document.body.innerHTML += `{formatted_html()}`''')


def on_options_called():
    dialog = TimeStatsOptionsDialog(TimeStatsConfigManager(mw))
    dialog.exec()


def should_display_on_current_screen():
    return str(mw.col.decks.current().get('id')) not in Excluded_DIDs


def get_review_times() -> (float, float):
    print(f'mw state: {mw.state}')
    if mw.state == 'overview':
        dids = [str(i) for i in mw.col.decks.deck_and_child_ids(mw.col.decks.current().get('id'))]
    else:
        dids = mw.col.decks.all_ids()

    for excluded_did in Excluded_DIDs:
        if excluded_did in dids:
            dids.remove(str(excluded_did))

    print(f'checking dids: {[mw.col.decks.name(i) for i in dids]}')

    dids_as_args = '(' + ', '.join(dids) + ')'
    cids_cmd = f'SELECT id FROM cards WHERE did in {dids_as_args}\n'
    cids = mw.col.db.all(cids_cmd)
    formatted_cids = '(' + (str(cids).replace('[', '').replace(']', '')) + ')'
    revlog_cmd = f'SELECT id, time FROM revlog WHERE cid in {formatted_cids}'

    rev_log = mw.col.db.all(revlog_cmd)

    # if date.today().weekday() >= Week_Start_Day:
    #     print(f'was greater than start day')
    #     date_at_range = date.today() - timedelta(days=Range_Days - Range.WEEK)
    # else:
    #     print(f'was less than start day')
    #     date_at_range = date.today() - timedelta(days=Range_Days)
    #
    # if Use_Week_Start:
    #     days_since_week_start = Range_Days + (date_at_range.weekday() - Week_Start_Day)
    #
    #     print(f'({date_at_range.strftime("%A")} - day({Week_Start_Day})): ({date_at_range.weekday()} -'
    #           f' {Week_Start_Day}) '
    #           f'= {(date_at_range.weekday() - Week_Start_Day)}')
    #
    #     print(f'since_input: {days_since_week_start}')
    #     filtered_revlog = filter_revlog(rev_log, days_ago=days_since_week_start)
    #
    # else:
    #     print(f'ago_input: {Range_Days}')

    days_ago = Range_Days

    if Use_Calendar_Range:
        if Range_Type == Range.WEEK:
            today = date.today()
            if today.weekday() >= Week_Start_Day:
                days_ago = (today.weekday() - Week_Start_Day)
            else:
                days_ago = (today.weekday() - Week_Start_Day) + Range.TOTAL_DAYS[Range.WEEK]
        elif Range_Type == Range.TWO_WEEKS:
            week_ago = date.today() - timedelta(days=Range.TOTAL_DAYS[Range.WEEK])
            print(f'week_ago: {week_ago.ctime()}')
            if week_ago.weekday() >= Week_Start_Day:
                print(f' Using week only: ({week_ago.weekday()} - {Week_Start_Day}) + {Range.TOTAL_DAYS[Range.WEEK]}')
                days_ago = (week_ago.weekday() - Week_Start_Day) + Range.TOTAL_DAYS[Range.WEEK]
            else:
                print(f' Using two weeks: ({week_ago.weekday()} - {Week_Start_Day}) + {Range.TOTAL_DAYS[Range.TWO_WEEKS]}')
                days_ago = (week_ago.weekday() - Week_Start_Day) + Range.TOTAL_DAYS[Range.TWO_WEEKS]
        elif Range_Type == Range.MONTH:
            pass
        elif Range_Type == Range.YEAR:
            pass
        elif Range_Type == Range.CUSTOM:
            pass

    filtered_revlog = filter_revlog(rev_log, days_ago=days_ago)

    all_rev_times_ms = [log[1] for log in rev_log[0:]]
    filtered_rev_times_ms = [log[1] for log in filtered_revlog[0:]]

    return sum(all_rev_times_ms) / 1000 / 60 / 60, sum(filtered_rev_times_ms) / 1000 / 60 / 60


def formatted_html():
    total_hrs, ranged_hrs = get_review_times()

    total_val = round(total_hrs, 2) if total_hrs > 1 else round(total_hrs * 60, 2)
    range_val = round(ranged_hrs, 2) if ranged_hrs > 1 else round(ranged_hrs * 60, 2)
    total_unit = Text.HRS if total_hrs > 1 else Text.MIN
    range_unit = Text.HRS if ranged_hrs > 1 else Text.MIN

    return html_shell.format(total_label=Total_Label, range_label=Range_Label,
                             total_value=total_val, range_value=range_val,
                             total_unit=total_unit, range_unit=range_unit,
                             primary_color=Primary_Color, secondary_color=Secondary_Color)


def offset_date(dt: datetime, hours: int = 0):
    return dt + timedelta(hours=hours)


def filter_revlog(rev_logs: [[int, int]], days_ago: int = None) -> [[int, int]]:
    offset_hour = mw.col.get_preferences().scheduling.rollover

    current_date = date.today()
    prev_start_date = current_date - timedelta(days=days_ago)
    prev_start_datetime = datetime(prev_start_date.year, prev_start_date.month, prev_start_date.day)
    date_ago = offset_date(prev_start_datetime, offset_hour)
    print(f'check against: {date_ago}, on: {date_ago.strftime("%a")}, days ago: {days_ago}')

    filtered_logs = []
    for log in rev_logs[0:]:
        log_epoch_seconds = log[0] / 1000
        log_date = datetime.fromtimestamp(log_epoch_seconds)

        log_days_ago = offset_date(datetime.now(), offset_hour) - log_date
        if log_days_ago.days <= days_ago:
            filtered_logs.append(log)

        # if days_ago is not None:
        #     log_days_ago = offset_date(datetime.now(), offset_hour) - log_date
        #     if log_days_ago.days < days_ago:
        #         filtered_logs.append(log)
        # elif after is not None:
        #     log_days_after = (log_date - offset_date(after, offset_hour)).days
        #     if log_days_after >= 0:
        #         filtered_logs.append(log)

    return filtered_logs


build_hooks()
build_actions()
