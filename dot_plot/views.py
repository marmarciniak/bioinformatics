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
    objectslist = DotPlot.objects.all()
    number = len(objectslist) - 1
    first_sequence = str(objectslist[number].first_sequence)
    second_sequence = str(objectslist[number].second_sequence)
    first_sequence = re.sub(r"\s+", "", first_sequence, flags=re.UNICODE)
    second_sequence = re.sub(r"\s+", "", second_sequence, flags=re.UNICODE)
    # first_sequence = first_sequence.replace(' ','')
    # second_sequence= second_sequence.replace(' ','')
    window = objectslist[number].window
    threshold = round(((objectslist[number].threshold)/100 * window),0)
    recurrence(first_sequence, second_sequence, window, threshold)
    return render(request, "dot_plot.html")

def create_vector_list(sequence, window):

    vector_list = []
    for i in range(len(sequence)-(window-1)):
        win = []
        for j in range(window):
            win.append(sequence[i+j])
        vector_list.append(win)
    return vector_list


def recurrence(f_sequence, s_sequence, window, threshold):

    recurrence_table = []

    f_vector_list = create_vector_list(f_sequence, window)
    s_vector_list = create_vector_list(s_sequence, window)



    # for s_amino_win in s_vector_list:
    #     row = []
    #     for f_amino_win in f_vector_list:
    #         counter = 0
    #         copy_f_amino_win = []
    #         if s_amino_win == f_amino_win:
    #             row.append(1)
    #         else:
    #             row.append(0)

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

    print(x_rqa)
    print(y_rqa)
    i=0
    while i <(len(x_rqa)-1):
        x=[]
        y=[]

        if (x_rqa[i]==x_rqa[i+1]-2) and (y_rqa[i]==y_rqa[i+1]+2):
            print(i)
            while(x_rqa[i]==x_rqa[i+1]-2) and (y_rqa[i]==y_rqa[i+1]+2):
                x.append(x_rqa[i])
                y.append(y_rqa[i])
                i+=1
            x.append(x_rqa[i])
            y.append(y_rqa[i])
            plt.plot(x,y)
        else:
            plt.plot([x_rqa[i]],[y_rqa[i]], 'ro')
            i+=1
        i+=1


    #plt.plot(x_rqa, y_rqa, 'ro', markersize=size)
    plt.xlim(-1, (2*sequence)-2)
    plt.ylim(0, 2*sequence2 )
    plt.xticks(range(0,2*sequence,2), f_sequence)
    plt.yticks(range(1,2*sequence2+1,2), s_sequence[::-1])
    # plt.set_xticks(range(1,2*sequence+1,2), minor=True)
    # plt.yticks(range(0,2*sequence2,2), minor=True)
    minorLocator = MultipleLocator(5)
    minor_xticks = np.arange(1, 2*sequence, 2)
    minor_yticks = np.arange(0, 2*sequence2, 2)
    ax.xaxis.tick_top()
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)
    plt.grid(which='minor', alpha=0.5)

    # ax3 = plt.subplot2grid((8, 8), (2, 6), rowspan=6, colspan=2)
    # ax3.plot(count_x, list(range(len(count_x))))
    # plt.xlim(0, max(count_x) + 1)
    # plt.ylim(0,len(count_x)-1)
    # plt.yticks([])
    # plt.xticks([])
    multi_plot.canvas.draw()
    multi_plot.savefig('static/RQA.png')
