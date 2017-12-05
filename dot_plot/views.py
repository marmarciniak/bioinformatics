from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotFound

from dot_plot.models import *
from dot_plot.forms import *
import re
# Create your views here.

import matplotlib
matplotlib.use('AGG')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axis as ax
from matplotlib.ticker import MultipleLocator

def home(request):
    aminokwasy = DotPlot()
    form = DotPlotForm(request.POST or None, instance=aminokwasy)
    if form.is_valid():
        aminokwasy = form.save()
        return redirect(main)
    ctx = {'form': form, 'dot_form': DotPlotForm}
    return TemplateResponse(request, 'base.html', ctx)

def main(request):
    # get data from database
    objectslist = DotPlot.objects.all()
    number = len(objectslist) - 1
    first_sequence = str(objectslist[number].first_sequence)
    second_sequence = str(objectslist[number].second_sequence)
    first_sequence = re.sub(r"\s+", "", first_sequence, flags=re.UNICODE)
    second_sequence = re.sub(r"\s+", "", second_sequence, flags=re.UNICODE)
    window = objectslist[number].window
    threshold = objectslist[number].threshold
    recurrence(first_sequence, second_sequence, window, threshold)
    return render(request, "dot_plot.html")

def create_vector_list(sequence, window):
    # windowing
    vector_list = []
    for i in range(len(sequence)-(window-1)):
        win = []
        for j in range(window):
            win.append(sequence[i+j])
        vector_list.append(win)
    return vector_list


def recurrence(f_sequence, s_sequence, window, threshold):

    f_vector_list = create_vector_list(f_sequence, window)
    s_vector_list = create_vector_list(s_sequence, window)

    recurrence_table = []
    for i in range(len(s_sequence)):
        recurrence_table.append(list(np.zeros(len(f_sequence))))

    for i in range(len(s_vector_list)):
        for j in range(len(f_vector_list)):
            counter = 0
            for w in range(window):
                if s_vector_list[i][w] == f_vector_list[j][w]:
                    counter+=1
            if counter >= threshold:
                for w in range(window):
                    recurrence_table[i+w][j+w] = 1



    makeplot_recurrence(len(f_sequence), len(s_sequence), recurrence_table,f_sequence, s_sequence)




def makeplot_recurrence(sequence, sequence2, recurrence_table,f_sequence, s_sequence):

    recurrence_table = np.array(np.reshape(recurrence_table, (sequence2, sequence)).tolist())
    # create list of coordinates for requrence plot
    x_rqa = []
    y_rqa = []
    for y in range(0,2*sequence2,2):
        for x in range(0,2*sequence,2):
            if recurrence_table[int(y/2)][int(x/2)] == 1:
                x_rqa.append(x)
                y_rqa.append((2*sequence2-y-1))

    multi_plot = plt.figure(figsize=(12, 9))
    multi_plot.clear()
    ax = multi_plot.add_subplot(1,1,1)
    # ax1 = plt.subplot2grid((8, 8), (0, 0), colspan=6, rowspan=2)
    # ax1.plot(list(range(len(count_y))), count_y)
    # plt.ylim(0, max(count_y) + 1)
    # plt.xlim(0,len(count_y)-1)
    # ax2 = plt.subplot2grid((8, 8), (2, 0), rowspan=6, colspan=6)
    if sequence > 100 or sequence2 > 100:
        size = 0.5
    else:
        size = 3

    wsp = [[x, y] for x, y in zip(x_rqa, y_rqa)]
    print(wsp)
    if wsp:
        wsp_spr = wsp[0]
        x = []
        y = []
    while len(wsp) > 1:
        wsp.remove(wsp_spr)
        if [wsp_spr[0]+2, wsp_spr[1]-2] in wsp:
            x.append(wsp_spr[0])
            y.append(wsp_spr[1])
            wsp_spr = [wsp_spr[0]+2, wsp_spr[1]-2]
            print(x,y)
        else:
            x.append(wsp_spr[0])
            y.append(wsp_spr[1])

            wsp_spr = wsp[0]
            print(x, y)
            if len(x) == 1:
                ax.plot(x, y, 'ro', markersize=1.5)
            else:
                ax.plot(x, y, 'r')
            x = []
            y = []
    if len(wsp)==1:
        x.append(wsp[0][0])
        y.append(wsp[0][1])
        if len(x) == 1:
            ax.plot(x, y, 'ro', markersize=1.5)
        else:
            ax.plot(x, y, 'r')
        x = []
        y = []





    plt.xlim(-1, (2*sequence)-2)
    plt.ylim(0, 2*sequence2)
    plt.xticks(range(0,2*sequence,2), f_sequence)
    plt.yticks(range(1,2*sequence2+1,2), s_sequence[::-1])
    minorLocator = MultipleLocator(5)
    minor_xticks = np.arange(1, 2*sequence, 2)
    minor_yticks = np.arange(0, 2*sequence2, 2)
    ax.xaxis.tick_top()
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)
    plt.grid(which='minor', alpha=0.5)

    multi_plot.canvas.draw()
    multi_plot.savefig('static/RQA.png')
