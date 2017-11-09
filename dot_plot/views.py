from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseNotFound

from dot_plot.models import *
from dot_plot.forms import *
# Create your views here.

import matplotlib
matplotlib.use('AGG')
import numpy as np
import matplotlib.pyplot as plt

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
    first_sequence = first_sequence.replace(' ','')
    second_sequence= second_sequence.replace(' ','')
    window = objectslist[number].window
    minimal_precision = objectslist[number].minimal_precision
    type = str(objectslist[number].type)
    recurrence(first_sequence, second_sequence, window, minimal_precision)
    return render(request, "dot_plot.html")

def create_vector_list(sequence, window):

    vector_list = []
    for i in range(len(sequence)-(window-1)):
        win = []
        for j in range(window):
            win.append(sequence[i+j])
        vector_list.append(win)
    return vector_list


def recurrence(f_sequence, s_sequence, window, r):

    recurrence_table = []

    f_vector_list = create_vector_list(f_sequence, window)
    s_vector_list = create_vector_list(s_sequence, window)



    for s_amino_win in s_vector_list:
        row = []
        for f_amino_win in f_vector_list:
            counter = 0
            copy_f_amino_win = []
            if s_amino_win == f_amino_win:
                row.append(1)
            else:
                row.append(0)
            # for item in f_amino_win:
            #     copy_f_amino_win.append(item)
            # for s_amino in s_amino_win:
            #     if s_amino in copy_f_amino_win:
            #         counter += 1
            #         copy_f_amino_win.remove(s_amino)
            # if counter >= r:
            #     row.append(1)
            # else:
            #     row.append(0)

    # for i in range(len(s_sequence)-window):
    #     row=[]
    #     for j in range(len(f_sequence)-window):
    #         counter = 0
    #         for w in range(window):
    #             try:
    #                 if f_sequence[i + w] == s_sequence[j + w] or f_sequence[i-w] == s_sequence[j-w]:
    #                     counter += 1
    #                 else:
    #                     break
    #             except IndexError:
    #                 if f_sequence[j+w] == s_sequence[i+w]:
    #                     counter += 1
    #                 else:
    #                     break
    #         if counter >= r:
    #             row.append(1)
    #         else:
    #             row.append(0)
    recurrence_table = []
    for i in range(len(s_sequence)):
        recurrence_table.append(list(np.zeros(len(f_sequence))))

    for i in range(len(s_vector_list)):
        for j in range(len(f_vector_list)):
            if s_vector_list[i] == f_vector_list[j]:
                for w in range(window):
                    recurrence_table[i+w][j+w] = 1

            # for item in f_amino_win:
            #     copy_f_amino_win.append(item)
            # for s_amino in s_amino_win:
            #     if s_amino in copy_f_amino_win:
            #         counter += 1
            #         copy_f_amino_win.remove(s_amino)
            # if counter >= r:
            #     row.append(1)
            # else:
            #     row.append(0)

    makeplot_recurrence(len(f_sequence), len(s_sequence), recurrence_table,f_sequence)




def makeplot_recurrence(sequence, sequence2, recurrence_table,f_sequence):

    recurrence_table = np.array(np.reshape(recurrence_table, (sequence2, sequence)).tolist())
    count_x = []
    # for i in range(0, sequence2):
    #     count_x.append(sum(recurrence_table[i]))
    # count_y = []
    # for j in range(sequence):
    #     count_local = 0
    #     for i in range(0, sequence2):
    #         count_local += recurrence_table[i][j]
    #     count_y.append(count_local)
    # y = []
    # for i in range(len(count_x)):
    #     y.append(i)
    # file = open("static/x.txt", "w")
    # file.write(str(count_x))
    # file.close()
    x_rqa = []
    y_rqa = []
    for y in range(sequence2):
        for x in range(sequence):
            if recurrence_table[y][x] == 1:
                x_rqa.append(x)
                y_rqa.append(sequence2-y)

    multi_plot = plt.figure(figsize=(12, 9))
    multi_plot.clear()
    # ax1 = plt.subplot2grid((8, 8), (0, 0), colspan=6, rowspan=2)
    # ax1.plot(list(range(len(count_y))), count_y)
    # plt.ylim(0, max(count_y) + 1)
    # plt.xlim(0,len(count_y)-1)
    # ax2 = plt.subplot2grid((8, 8), (2, 0), rowspan=6, colspan=6)
    if sequence > 100 or sequence2 > 100:
        size = 0.5
    else:
        size = 1
    plt.plot(x_rqa, y_rqa, 'ro', markersize=size)
    plt.xlim(0, sequence+1)
    plt.ylim(0, sequence2+1)
    plt.xticks(range(0,sequence+1))
    plt.yticks(range(0,sequence2+1))
    # plt.grid()
    # ax3 = plt.subplot2grid((8, 8), (2, 6), rowspan=6, colspan=2)
    # ax3.plot(count_x, list(range(len(count_x))))
    # plt.xlim(0, max(count_x) + 1)
    # plt.ylim(0,len(count_x)-1)
    plt.yticks([])
    plt.xticks([])

    multi_plot.canvas.draw()
    multi_plot.savefig('static/RQA.png')
