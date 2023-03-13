# old plotupdate funcitons

        elif self.toplot == "Peaks over time":
            self.xtext = "Peak #"
            self.ytext = "Change in Resistance"
            self.xunit = ""
            self.yunit = "(%)"
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0

            for t in range(len(self.timestamp)):
                self.color = self.colors[counter % 6]
                # get the list up to but not including the next keyword
                temp_stepcount1 = self.stepcount[:self.stepcount.index(keyword)]
                temp_R11 = self.R1[:self.R1.index(keyword)]
                temp_R21 = self.R2[:self.R2.index(keyword)]
                temp_stepcount = []
                temp_R1 = []
                temp_R2 = []
                now_R1 = []
                now_R2 = []
                switch = 1
                runningnumber = 1
                self.cycle = self.ui.spinBox_cycle.value()
                # find the highest and lowest values in the list temp_stepcount with an accepted difference of 4
                # this code then saves these peaks into a new list which is plotted. 
                # the switch is needed so only one peak in each cycle is counted
                # this code can also count the minimum peaks, this should be done seperately though, for better readability
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                for i in range(len(temp_stepcount1)):
                    if runningnumber > self.cycle:
                        break
                    else:
                        if switch == 1:
                            if (max_step-temp_stepcount1[i]) <= 4:
                                temp_stepcount.append(runningnumber)
                                temp_R1.append(temp_R11[i])
                                temp_R2.append(temp_R21[i])
                                switch = 0
                        else:
                            if (temp_stepcount1[i] <= 4):
                                temp_R1.append(temp_R11[i])
                                temp_R2.append(temp_R21[i])
                                runningnumber += 1
                                switch = 1    
                            elif (i == len(temp_stepcount1)-1):
                                temp_R1.append(temp_R11[i])
                                temp_R2.append(temp_R21[i])
                                runningnumber += 1
                                switch = 1
                                break
                for c in range(len(temp_stepcount)):
                    now_R1.append(abs(temp_R1[2*c]-temp_R1[2*c+1])/temp_R1[2*c+1]*100)
                    now_R2.append(abs(temp_R2[2*c]-temp_R2[2*c+1])/temp_R2[2*c+1]*100)
                self.graphWidget.plotline(temp_stepcount, now_R1, self.findbytimestamp(self.timestamp[t]), self.color)
                self.graphWidget2.plotline(temp_stepcount, now_R2, self.findbytimestamp(self.timestamp[t]), self.color)
                # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                counter += 1
                
        elif self.toplot == "2":
            self.xtext = "Sample #"
            self.ytext = "MAE in Hysteresis _ Each Cycle"
            self.xunit = ""
            self.yunit = ""
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                counter = 0
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=4:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 4:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    error1 = np.mean(np.abs(pu_r1 - pd_r1))
                    error2 = np.mean(np.abs(pu_r2 - pd_r2))
                    stamp = [t]
                    err_r1 = [error1]
                    err_r2 = [error2]

                    self.graphWidget.plotnew(stamp, err_r1, self.findbytimestamp(self.timestamp[t]), self.color, error1*10)
                    self.graphWidget2.plotnew(stamp, err_r2, self.findbytimestamp(self.timestamp[t]), self.color, error2*10)
                    counter+=1
                    self.color = self.colors[counter % 6]

                    # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]

        elif self.toplot == "3":
            self.xtext = "Sample #"
            self.ytext = "MAE in Hysteresis _ Each Cycle"
            self.xunit = ""
            self.yunit = "(%)"
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                counter = 0
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                margin = 5
                datacursor.execute("SELECT speed FROM database WHERE timestamp = ?", (self.timestamp[t],))
                speed = datacursor.fetchall()[0]
                datacursor.execute("SELECT samplerate FROM database WHERE timestamp = ?", (self.timestamp[t],))
                samplerate = datacursor.fetchall()[0]
                margin = int(2*speed/(samplerate*100))
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=margin:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= margin:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    div1 = np.abs(max(pu_r1)-min(pu_r1))
                    div2 = np.abs(max(pu_r2)-min(pu_r2))
                    error1 = np.mean(np.abs(pu_r1 - pd_r1)/div1)
                    error2 = np.mean(np.abs(pu_r2 - pd_r2)/div2)
                    stamp = [t]
                    err_r1 = [error1]
                    err_r2 = [error2]

                    self.graphWidget.plotnew(stamp, err_r1, self.findbytimestamp(self.timestamp[t]), self.color, error1*100)
                    self.graphWidget2.plotnew(stamp, err_r2, self.findbytimestamp(self.timestamp[t]), self.color, error2*100)
                    counter+=1
                    self.color = self.colors[counter % 6]

                    # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]

        elif self.toplot == "4":
            self.xtext = "Sample #"
            self.ytext = "MAE in Hysteresis _ Each Cycle"
            self.xunit = ""
            self.yunit = "(%)"
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            nextcolor = 0
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                counter = 0
                self.color = self.colors[nextcolor % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=15:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= 15:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-1:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False

                #function to interpolate the data 
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    div1 = np.abs(max(pu_r1)-min(pu_r1))
                    div2 = np.abs(max(pu_r2)-min(pu_r2))
                    error1 = np.mean(np.abs(pu_r1 - pd_r1)/div1)
                    error2 = np.mean(np.abs(pu_r2 - pd_r2)/div2)
                    stamp = [t]
                    err_r1 = [error1*100]
                    err_r2 = [error2*100]

                    self.graphWidget.plotnew(counter, err_r1, self.findbytimestamp(self.timestamp[t]), self.color, error1*100)
                    self.graphWidget2.plotnew(counter, err_r2, self.findbytimestamp(self.timestamp[t]), self.color, error2*100)
                    counter+=1

                    # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]
                nextcolor += 1

        elif self.toplot == "5":
            self.xtext = "Sample #"
            self.ytext = "Mean Absolute Error"
            self.xunit = ""
            self.yunit = "(%)"
            self.graphWidget.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            self.graphWidget2.refresh(self.xtext, self.xunit, self.ytext, self.yunit)
            counter = 0
            precision = 4
            maxstepreached = False
            cyclebreaks = [0]
            halfcyclebreaks = [0]
            

            for t in range(len(self.timestamp)):
                datacursor.execute("SELECT steps FROM database WHERE timestamp = ?", (self.timestamp[t],))
                max_step = datacursor.fetchall()[0]
                counter = 0
                self.color = self.colors[counter % 6]
                halfcyclebreaks = [0]
                cyclebreaks = [0]
                # get the list up to but not including the next keyword
                temp_stepcount = self.stepcount[:self.stepcount.index(keyword)]
                temp_R1 = self.R1[:self.R1.index(keyword)]
                temp_R2 = self.R2[:self.R2.index(keyword)]
                for i in range(len(temp_stepcount)):
                    if  maxstepreached == False and max_step-temp_stepcount[i] <=precision:
                        halfcyclebreaks.append(i)
                        maxstepreached = True
                    if maxstepreached == True and temp_stepcount[i] <= precision:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                    elif maxstepreached == True and i == len(temp_stepcount)-precision:
                        cyclebreaks.append(i)
                        halfcyclebreaks.append(i)
                        maxstepreached = False
                listofmae1 = []
                listofmae2 = []
                #function to interpolate the data 
                iternum = self.ui.spinBox_cycleEnd.value() - self.ui.spinBox_cycle.value() + 1
                for iter in range(iternum):
                    lowercycle = self.ui.spinBox_cycle.value()+iter
                    upwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]                
                    downwardssteps = temp_stepcount[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR1 = temp_R1[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    upwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-2]:halfcyclebreaks[2*lowercycle-1]]
                    downwardsR2 = temp_R2[halfcyclebreaks[2*lowercycle-1]:halfcyclebreaks[2*lowercycle]]
                    #find indices of duplicates
                    seen = set()
                    indices = [i for i, x in enumerate(upwardssteps) if upwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    #delete duplicates
                    if indices:
                        for index in reversed(indices):
                            del upwardssteps[index]
                            del upwardsR1[index]
                            del upwardsR2[index]
                    seen = set()
                    indices = [i for i, x in enumerate(downwardssteps) if downwardssteps.count(x) > 1 and x not in seen and not seen.add(x)]
                    if indices:
                        for index in reversed(indices):
                            del downwardssteps[index]
                            del downwardsR1[index]
                            del downwardsR2[index]
                    mykind = 'cubic'
                    predictupwards_r1 = interp1d(upwardssteps, upwardsR1, kind=mykind, bounds_error=False, fill_value=(upwardsR1[0], upwardsR1[-1]))
                    predictdownwards_r1 = interp1d(downwardssteps, downwardsR1, kind=mykind, bounds_error=False, fill_value=(downwardsR1[-1], downwardsR1[0]))
                    predictupwards_r2 = interp1d(upwardssteps, upwardsR2, kind=mykind, bounds_error=False, fill_value=(upwardsR2[0], upwardsR2[-1]))
                    predictdownwards_r2 = interp1d(downwardssteps, downwardsR2, kind=mykind, bounds_error=False, fill_value=(downwardsR2[-1], downwardsR2[0]))
                    stepcount_detail = list(range(0, max_step+1))
                    pu_r1 = ndimage.gaussian_filter1d(predictupwards_r1(stepcount_detail), 5)
                    pd_r1 = ndimage.gaussian_filter1d(predictdownwards_r1(stepcount_detail), 5)
                    pu_r2 = ndimage.gaussian_filter1d(predictupwards_r2(stepcount_detail), 5)
                    pd_r2 = ndimage.gaussian_filter1d(predictdownwards_r2(stepcount_detail), 5)
                    div1 = np.abs(max(pu_r1)-min(pu_r1))
                    div2 = np.abs(max(pu_r2)-min(pu_r2))
                    error1 = np.mean(np.abs(pu_r1 - pd_r1)/div1)
                    error2 = np.mean(np.abs(pu_r2 - pd_r2)/div2)
                    stamp = [t]
                    err_r1 = [error1*100]
                    err_r2 = [error2*100]
                    listofmae1.append(round(error1*100,2))
                    listofmae2.append(round(error2*100,2))
                    size = 5
                    for mae in listofmae1:
                        if round(err_r1[0],2) == mae:
                            size += 10
                    self.graphWidget.plotnew(stamp, err_r1, self.findbytimestamp(self.timestamp[t]), self.color, size)
                    size = 5
                    for mae in listofmae2:
                        if round(err_r2[0],2) == mae:
                            size += 10
                    self.graphWidget2.plotnew(stamp, err_r2, self.findbytimestamp(self.timestamp[t]), self.color, size)
                    counter+=1
                    self.color = self.colors[counter % 6]

                    # delete the list up to the next keyword
                del self.stepcount[:self.stepcount.index(keyword)+1]
                del self.R1[:self.R1.index(keyword)+1]
                del self.R2[:self.R2.index(keyword)+1]



# Add the parsed data to the combox widget
        ExistingProjects = [self.ui.comboBox_project.itemText(i) for i in range(self.ui.comboBox_project.count())]
        for i in ExistingProjects:
            if projectdata[0] == i:
                check = True
        if check == False:
            self.ui.comboBox_project.addItems(projectdata)
        else:
            check = False

        # Add checkboxes based on the parsed data
        for y in self.ui.scrollAreaWidgetContents_design.findChildren(QCheckBox):
            if y.text() == designdata[0]:
                check=True
        if check == False:
            self.addCheckbox(designdata[0], self.ui.scrollAreaWidgetContents_design)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_sample.findChildren(QCheckBox):
            if y.text() == sampledata[0]:
                check=True
        if check == False:
            self.addCheckbox(sampledata[0], self.ui.scrollAreaWidgetContents_sample)
        else:
            check = False
        
        for y in self.ui.scrollAreaWidgetContents_material.findChildren(QCheckBox):
            if y.text() == materialdata[0]:
                check=True
        if check == False:
            self.addCheckbox(materialdata[0], self.ui.scrollAreaWidgetContents_material)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_print.findChildren(QCheckBox):
            if y.text() == printdata[0]:
                check=True
        if check == False:
            self.addCheckbox(printdata[0], self.ui.scrollAreaWidgetContents_print)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_orientation.findChildren(QCheckBox):
            if y.text() == orientationdata[0]:
                check=True
        if check == False:
            self.addCheckbox(orientationdata[0], self.ui.scrollAreaWidgetContents_orientation)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_A.findChildren(QCheckBox):
            if y.text() == adata[0]:
                check=True
        if check == False:
            if adata[0] != None:
                self.addCheckbox(adata[0], self.ui.scrollAreaWidgetContents_A)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_B.findChildren(QCheckBox):
            if y.text() == bdata[0]:
                check=True
        if check == False:
            if bdata[0] != None:
                self.addCheckbox(bdata[0], self.ui.scrollAreaWidgetContents_B)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_G.findChildren(QCheckBox):
            if y.text() == gdata[0]:
                check=True
        if check == False:
            if gdata[0] != None:
                self.addCheckbox(gdata[0], self.ui.scrollAreaWidgetContents_G)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_F.findChildren(QCheckBox):
            if y.text() == fdata[0]:
                check=True
        if check == False:
            if fdata[0] != None:
                self.addCheckbox(fdata[0], self.ui.scrollAreaWidgetContents_F)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_speed.findChildren(QCheckBox):
            if y.text() == speeddata[0]:
                check=True
        if check == False:
            self.addCheckbox(speeddata[0], self.ui.scrollAreaWidgetContents_speed)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_cycles.findChildren(QCheckBox):
            if y.text() == cyclesdata[0]:
                check=True
        if check == False:
            self.addCheckbox(cyclesdata[0], self.ui.scrollAreaWidgetContents_cycles)
        else:
            check = False

        for y in self.ui.scrollAreaWidgetContents_steps.findChildren(QCheckBox):
            if y.text() == stepsdata[0]:
                check=True
        if check == False:
            self.addCheckbox(stepsdata[0], self.ui.scrollAreaWidgetContents_steps)
        else:
            check = False