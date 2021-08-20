import matplotlib.pyplot as plt
import seaborn as sns
import audplot
from util import Util 
import ast
import numpy as np
import glob_conf
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from result import Result

class Reporter:

    def __init__(self, truths, preds):
        self.util = Util()
        self.truths = truths
        self.preds = preds

    def continuous_to_categorical(self):
        bins = ast.literal_eval(glob_conf.config['DATA']['bins'])
        self.truths = np.digitize(self.truths, bins)-1
        self.preds = np.digitize(self.preds, bins)-1

    def plot_confmatrix(self, plot_name): 
        if not self.util.exp_is_classification:
            self.continuous_to_categorical()

        fig_dir = self.util.get_path('fig_dir')
        labels = ast.literal_eval(glob_conf.config['DATA']['labels'])
        plt.figure()  # figsize=[5, 5]
        cm = confusion_matrix(self.truths, self.preds,  normalize = None) #normalize must be one of {'true', 'pred', 'all', None}
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels).plot(cmap='Blues')
        print(f'plotting conf matrix to {fig_dir+plot_name}')
        plt.title('Confusion Matrix')
        plt.savefig(fig_dir+plot_name)
        plt.close()


    def plot_confmatrix_old(self, plot_name): 
        fig_dir = self.util.get_path('fig_dir')
        sns.set()  # get prettier plots
        labels = ast.literal_eval(glob_conf.config['DATA']['labels'])
        plt.figure()  # figsize=[5, 5]
        plt.title('Confusion Matrix')
        plt.ylabel('UAR')
        audplot.confusion_matrix(self.truths, self.preds)
        # replace labels
        locs, _ = plt.xticks()
        plt.xticks(locs, labels)
        plt.yticks(locs, labels)
        plt.tight_layout()
        print(f'plotting conf matrix to {fig_dir+plot_name}')
        plt.savefig(fig_dir+plot_name)
        plt.close()
        print('truths')
        print(self.truths.values)
        print('preds')
        print(self.preds)
        print('labels')
        print(labels)

    def result(self):
        if self.util.exp_is_classification:
            uar = recall_score(self.truths, self.preds, average='macro')
            loss = 1 - accuracy_score(self.truths, self.preds)
            self.result = Result(uar, -1, loss)
        else:
            # regression experiment
            pcc = pearsonr(self.truths, self.preds)[0]
            loss = mean_squared_error(self.truths, self.preds)
            self.result = Result(pcc, -1, loss)
        return self.result