from flask import Blueprint, request, Response, jsonify
import gspread
import threading
import json
from oauth2client.service_account import ServiceAccountCredentials

module = Blueprint('schedule', __name__, url_prefix='/api/schedule')
t = {}

def FromBadToGoodWord(str1):
    return str1.split("'")[1]


def GetTimeTable():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('1.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1yI8crMmfMbCFQMx5PdqBreCjTNK5r-aJeqgU9pWN85c/edit#gid=1539915031')
    g = wks.worksheet('расписание')
    cls = {'5C': 'C', '6C': 'D', '7C': 'E', '7T': 'F', '7L': 'G', '9C': 'H'}
    cell_list = g.range(cls[cl] + '2:' + cls[cl] + '72')
    ans_list = {'5C' : [[], [], [], [], [], []], '6C' : [[], [], [], [], [], []], '7C' : [[], [], [], [], [], []], '7T' : [[], [], [], [], [], []], '7L' : [[], [], [], [], [], []], '9C' : [[], [], [], [], [], []]}
    for cl in cls:
        for i in range(2, 71):
            if i < 14:
                ans_list[cl][0].append(FromBadToGoodWord(str(cell_list[i])))
            if i > 13 and i < 25:
                ans_list[cl][1].append(FromBadToGoodWord(str(cell_list[i])))
            if i > 24 and i < 38:
                ans_list[cl][2].append(FromBadToGoodWord(str(cell_list[i])))
            if i > 37 and i < 49:
                ans_list[cl][3].append(FromBadToGoodWord(str(cell_list[i])))
            if i > 48 and i < 62:
                ans_list[cl][4].append(FromBadToGoodWord(str(cell_list[i])))
            if i > 61:
                ans_list[cl][5].append(FromBadToGoodWord(str(cell_list[i])))
    return ans_list

@module.route('/get_schedule/<cl>', methods=['GET'])
def GetTimeTableOfCertainClass(cl):
    return json.dumps({'ans': t[cl]})
def GetWholeTimeTable():
    print("Hey! I'm working")
    t = GetTimeTable()
#threading.Timer(1, GetWholeTimeTable).start
#return json.dumps({'ans': ans_list})
