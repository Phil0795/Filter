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