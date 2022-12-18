#!/usr/bin/env python3

## Analytical model,
##

import os, sys, random
import numpy as np
import gc

import pymetamodels
import damped_model as model_obj

class analysis(object):

    """

    .. _model_damped_oscillator_metamodel:

    **Synopsis:**
        * Analysis framework with pymetamodels
        * Damped oscillator tutorial

    """

    def __init__(self):
        
        ## Initial variables
        self.name = "damped_oscillator"
        self.folder_script = os.path.dirname(os.path.realpath(__file__))

        self.folder_path_inputs = self.folder_script

        self.folder_path_outputs = os.path.join(os.path.join(os.path.join(self.folder_script, os.pardir), "_examples_raw"),self.name + "_out")
        if not os.path.exists(self.folder_path_outputs): os.makedirs(self.folder_path_outputs)

        self.file_name_inputs = r"configuration_spreadsheet"
        self.file_name_outputs = r"outputs"

        ## Initialise 
        self.mita = pymetamodels.load()
        self.mita.logging_start(self.folder_path_outputs)          

    def run_model(self):

        ## Inputs load
        folder_path = self.folder_path_inputs
        file_name = self.file_name_inputs
        self.mita.read_xls_case(folder_path, file_name, sheet="cases", col_start = 0, row_start = 1, tit_row = 0 )

        ## Sampling
        for case in self.mita.keys():

            ## Run samplimg cases
            self.mita.run_sampling_routine(case)

            ## Run / Load model
            self.model_iteration(case, model_obj)

            ## Sensitivity analysis
            self.mita.run_sensitivity_analisis(case)

            ## Metamodeling construction
            #self.mita.run_metamodel_construction(case, scheme = "general")
            self.mita.run_metamodel_construction(case, scheme = "general_fast")

        ##
        self.mita.run_sensitivity_normalization()

        ## Ploting and others
        for case in self.mita.keys():

            ## Plots cross varible relation in the sensitivity analysis
            self.mita.output_plts_sensitivity(self.folder_path_outputs, case)

            ## Plots showing the model DOEX and DOEY variables relationship 2D XY
            self.mita.output_plts_models_XY(self.folder_path_outputs, case)

            ## Residual values plots
            self.mita.output_plts_models_residuals_plot(self.folder_path_outputs, case)

            ## Plots showing the model DOEX and DOEY variables relationship 3D XYZ
            self.mita.output_plts_models_XYZ(self.folder_path_outputs, case, scatter = False)

        ## Output variables save
        folder_path = self.folder_path_outputs
        file_name = self.file_name_outputs
        out_path = self.mita.output_xls(folder_path, file_name, col_start = 0, tit_row = 0)

    def model_iteration(self, case, _model_obj):

        ## Model iteration to generate Y doe output values
        doeX = self.mita.doeX(case)
        doeY = self.mita.doeY(case)
        vars_in = self.mita.vars_parameter_matrix(case)
        case_dict = self.mita.case[case]
        samples = len(doeX[list(doeX.keys())[0]])

        for ii in range(0, samples):

            obj_model = _model_obj.model_obj()

            # initialize dictionaries
            obj_model.doeX = doeX
            obj_model.doeY = doeY
            obj_model.case_dict = case_dict
            obj_model.ii = ii
            obj_model.vars_in = vars_in

            # add variables as atributes
            for key in obj_model.doeX.keys():
                setattr(obj_model, key, obj_model.doeX[key][obj_model.ii])

            # run the model for ii sample
            obj_model.run_model()

if __name__ == "__main__":

    analysis = analysis()

    analysis.run_model()
