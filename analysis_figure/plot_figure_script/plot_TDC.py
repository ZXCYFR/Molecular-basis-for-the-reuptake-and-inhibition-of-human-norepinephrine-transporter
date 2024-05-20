import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.signal
from scipy.interpolate import make_interp_spline

def read_data(file):
    # resid_list = [26,27,28,29,30,32,146,235,236,240,243,246,252,304,317,318,319,320,322,323,324,415,483,488]
    resid_list = [29,30,31,32,33,146,235,238,240,243,304,307,318,319,324]

    f = open(file,'r')
    data = []
    PB = False
    DELTAS = False
    Total = False
    for line in f.readlines():
        if 'Poisson Boltzmann model' in line:
            PB = True
        if PB == True:
            if 'DELTAS' in line:
                DELTAS = True
            if DELTAS == True:
                if 'Total Energy Decomposition' in line: # Sidechain Energy Decomposition Backbone Energy Decomposition
                    Total = True
                if Total == True:
                    if '::' in line:
                        resid_name = line.split(',')[0].split(':')[-2]
                        resid_id = int(line.split(',')[0].split(':')[-1])
                        if resid_id in resid_list:
                            TDC = float(line.split(',')[-3])
                            TDC_stde = float(line.split(',')[-1])
                            data.append([resid_id,TDC,TDC_stde])
                    if ':561,' in line:
                        break
    return np.array(data)

def data_smooth(ligand):
    data = read_data('./%s/mmpbsa/FINAL_DECOMP_MMPBSA.dat'%ligand)
    resid_id = data[:, 0]
    TDC = data[:, 1]
    TDC_stde = data[:, 2]
    
    resid_id = [str(i).split('.')[0] for i in resid_id]
    # savitzky-Golay smooth
    # y_smooth = scipy.signal.savgol_filter(y, 9, 2)
    
    return resid_id,TDC,TDC_stde


def plot_pdf(ligand):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['svg.fonttype'] = 'none'

    matplotlib.font_manager._rebuild()

    resid_list = ['Y87','K88','N89','G90','G91','K204','A293','H296','D298','R301','F362','L365','I376','E377','E382']
    bar_width = 0.2

    ligand1 = ligand
    ligand2 = ligand + '2'
    ligand3 = ligand + '3'

    resid_id1,TDC1,TDC_stde1 = data_smooth(ligand1)
    resid_id2,TDC2,TDC_stde2 = data_smooth(ligand2)
    resid_id3,TDC3,TDC_stde3 = data_smooth(ligand3)
     
    x1 = np.arange(len(resid_id1))
    x2 = [x + bar_width for x in x1]
    x3 = [x + bar_width for x in x2]


    # plot
    fig = plt.figure(figsize=(10,4)) # facecolor='none'
    ax = plt.gca()
    
    plt.bar(x1,TDC1,color='steelblue',width=bar_width,yerr=TDC_stde1) # ,linestyle='--',alpha=1,label='Repeat1'
    plt.bar(x2,TDC2,color='darkorange',width=bar_width,yerr=TDC_stde2) # ,linestyle='--',alpha=1
    plt.bar(x3,TDC3,color='forestgreen',width=bar_width,yerr=TDC_stde3) # ,linestyle='--',alpha=1
    plt.title('Total Energy Decomposition',fontfamily='Arial',fontsize=28)

    # xlabel
    plt.xlabel('Residue Number',fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='x', width=2, labelsize=22)
    plt.xticks([x+bar_width for x in x1],resid_list,rotation=45)
    # ax.xaxis.set_major_locator(plt.MultipleLocator(100))
    plt.xlim(-0.5,15)
    
    # ylabel
    plt.ylabel('Energy (kcal/mol)',fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='y', width=2, labelsize=22)
    ax.yaxis.set_major_locator(plt.MultipleLocator(25))
    plt.ylim(-50,30)
    ax.invert_yaxis()

    plt.hlines(-10,-0.5,15,color='black',ls='--',lw=1)
    # plt.vlines(5,0,10,color='black',ls='--',lw=2)
    # plt.legend()
    
    # for i,v in enumerate(TDC1):
        # plt.text(x1[i],v+0.5,str(v),ha='center',va='bottom')
    # for i,v in enumerate(TDC2):
        # plt.text(x1[i],v+0.5,str(v),ha='center',va='bottom')
    # for i,v in enumerate(TDC2):
        # plt.text(x1[i],v+0.5,str(v),ha='center',va='bottom')

    # borders
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    # show or save
    # plt.show()
    plt.savefig('%s_TDC.pdf'%(ligand),format='pdf',dpi=300,transparent=True,bbox_inches='tight') # ,transparent=True

if __name__ == '__main__':
    ligand = 'LDP'  # LDP-Dopamine,LNR-Norepinephrine
    plot_pdf(ligand)

    ligand = 'LNR'  # LDP-Dopamine,LNR-Norepinephrine
    plot_pdf(ligand)

