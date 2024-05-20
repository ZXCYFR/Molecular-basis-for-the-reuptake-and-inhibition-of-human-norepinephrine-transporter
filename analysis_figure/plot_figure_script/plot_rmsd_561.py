import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import scipy.signal


def read_data(file):
    f = open(file,'r')
    data = []
    for line in f.readlines():
        if '#' not in line and '@' not in line:
            x = float(line.split()[0])/10
            y = float(line.split()[1])
            data.append([x,y])
    return np.array(data)


def data_smooth(ligand, system):
    data = read_data('./%s/rmsd_%s_ref.out'%(ligand,system))
    x = data[:, 0]
    y = data[:, 1]
    
    # savitzky-Golay smooth
    y_smooth = scipy.signal.savgol_filter(y, 9, 2)
    
    return x, y, y_smooth

def plot_pdf(ligand,ligand_name,system):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['svg.fonttype'] = 'none'
    
    ligand1 = ligand
    ligand2 = ligand + '2'
    ligand3 = ligand + '3'

    x1, y1, y1_smooth = data_smooth(ligand1, system)
    x2, y2, y2_smooth = data_smooth(ligand2, system)
    x3, y3, y3_smooth = data_smooth(ligand3, system)

    # plot
    fig = plt.figure(figsize=(10,4)) # facecolor='none'
    ax = plt.gca()
    
    plt.plot(x1,y1_smooth,color='steelblue',linewidth=2.5) # ,linestyle='--',alpha=1
    plt.plot(x2,y2_smooth,color='darkorange',linewidth=2.5) # ,linestyle='--',alpha=1
    plt.plot(x3,y3_smooth,color='forestgreen',linewidth=2.5) # ,linestyle='--',alpha=1
    plt.title('RMSD for %s Heavy Atoms'%ligand_name,fontfamily='Arial',fontsize=28)
    
    # xlabel
    plt.xlabel('Simulation Time (ns)',fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='x', width=2, labelsize=22)
    ax.xaxis.set_major_locator(plt.MultipleLocator(100))
    plt.xlim(0,500)
    
    # ylabel
    plt.ylabel('RMSD (Å)',fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='y', width=2, labelsize=22)
    ax.yaxis.set_major_locator(plt.MultipleLocator(2))
    plt.ylim(0,6)
    
    # plt.hlines(5,0,500,color='black',ls='--',lw=2)
    # plt.vlines(5,0,10,color='black',ls='--',lw=2)
    # plt.legend()
    
    # borders
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    # show or save
    # plt.show()
    plt.savefig('%s_%s_RMSD.pdf'%(ligand,system),format='pdf',dpi=300,transparent=True,bbox_inches='tight') # ,transparent=True

if __name__ == '__main__':
    ligand = 'LDP'  # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Dopamine'
    system = '561'  # BD,561
    plot_pdf(ligand,ligand_name,system)
    
    ligand = 'LNR'  # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Norepinephrine'
    system = '561'  # BD,561
    plot_pdf(ligand,ligand_name,system)