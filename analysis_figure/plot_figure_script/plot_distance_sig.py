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
            y = float(line.split()[3])
            data.append([x,y])
    return np.array(data)


def data_smooth(ligand,resid):
    data = read_data('./%s/mindist_%s-561.out' % (ligand, resid))
    x = data[:, 0]
    y = data[:, 1]
    
    # savitzky-Golay smooth
    y_smooth = scipy.signal.savgol_filter(y, 25, 2)
    
    return x, y, y_smooth


def plot_pdf(ligand,ligand_name,resid,resid_name,color):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['svg.fonttype'] = 'none'

    x, y, y_smooth = data_smooth(ligand, resid)
    
    # stat
    y_mean,y_var,y_std = data_stat(ligand,resid, y)
    
    # plot
    plt.figure(figsize=(10,3)) # facecolor='none'
    ax = plt.gca()
    
    plt.plot(x,y_smooth,color=color,linewidth=2.5) # ,linestyle='--',alpha=1
    # plt.title('Mindist between resid %s and %s'%(ligand,resid),fontfamily='Arial',fontsize=28)
    
    # xlabel
    plt.xlabel('Simulation Time (ns)',fontfamily='Arial',fontsize=20)
    plt.tick_params(axis='x',width=2,labelsize=18)
    plt.xlim(0,500)
    x_major_locator=plt.MultipleLocator(100)
    ax.xaxis.set_major_locator(x_major_locator)
    
    # ylabel
    plt.ylabel('%s-%s\n(%s±%s Å)'%(ligand_name,resid_name,y_mean,y_std),fontfamily='Arial',fontsize=20)
    plt.tick_params(axis='y',width=2,labelsize=18)
    plt.ylim(0,10)
    y_major_locator=plt.MultipleLocator(5)
    ax.yaxis.set_major_locator(y_major_locator)
    
    plt.hlines(5,0,500,color='black',ls='--',lw=2)
    # plt.vlines(5,0,10,color='black',ls='--',lw=2)
    # plt.legend()
    
    # borders
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    # show or save
    # plt.show()
    plt.savefig('mindist_%s_%s.pdf'%(ligand,resid),format='pdf',dpi=300,transparent=True,bbox_inches='tight') # ,transparent=True
    
    return True


def data_stat(ligand,resid, y):
    # mean,var,std
    return round(np.mean(y), 1),round(np.var(y), 1), round(np.std(y), 1)

if __name__ == '__main__':
    resid_list = ['29','30','31','32','33','235','238','240','243','304','307','318','319','320','322','324']
    # resid_list_xx = ['Y29','K30','N31','G32','G33','A235','H238','D240','R243','F304','L307','I318','E319','D320','A322','E324']
    resid_name_list = ['Y87','K88','N89','G90','G91','A293','H296','D298','R301','F362','L365','I376','E377','D378','A380','E382']
    
    ligand = 'LDP' # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Dopamine'
    for resid in resid_list:
        resid_name = resid_name_list[resid_list.index(resid)]
        ligand1 = ligand
        ligand2 = ligand + '2'
        ligand3 = ligand + '3'
        plot_pdf(ligand1,ligand_name,resid,resid_name,'steelblue')
        plot_pdf(ligand2,ligand_name,resid,resid_name,'darkorange')
        plot_pdf(ligand3,ligand_name,resid,resid_name,'forestgreen')
        
    ligand = 'LNR' # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Norepinephrine'
    for resid in resid_list:
        resid_name = resid_name_list[resid_list.index(resid)]
        ligand1 = ligand
        ligand2 = ligand + '2'
        ligand3 = ligand + '3'
        plot_pdf(ligand1,ligand_name,resid,resid_name,'steelblue')
        plot_pdf(ligand2,ligand_name,resid,resid_name,'darkorange')
        plot_pdf(ligand3,ligand_name,resid,resid_name,'forestgreen')