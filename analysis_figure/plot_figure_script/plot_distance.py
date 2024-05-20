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
    
    return x,y,y_smooth


def plot_pdf(ligand,ligand_name,resid,resid_name):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['svg.fonttype'] = 'none'
    
    ligand1 = ligand
    ligand2 = ligand + '2'
    ligand3 = ligand + '3'
    
    x1,y1,y1_smooth = data_smooth(ligand1,resid)
    x2,y2,y2_smooth = data_smooth(ligand2,resid)
    x3,y3,y3_smooth = data_smooth(ligand3,resid)
    
    # stat
    y_mean,y_var,y_std = data_stat(ligand,resid, y1, y2, y3)
    
    # plot
    plt.figure(figsize=(10,5)) # facecolor='none'
    ax = plt.gca()
    
    plt.plot(x1,y1_smooth,color='steelblue',linewidth=2.5) # ,linestyle='--',alpha=1
    plt.plot(x2,y2_smooth,color='darkorange',linewidth=2.5) # ,linestyle='--',alpha=1
    plt.plot(x3,y3_smooth,color='forestgreen',linewidth=2.5) # ,linestyle='--',alpha=1
    # plt.title('Mindist between resid %s and %s'%(ligand,resid),fontfamily='Arial',fontsize=28)
    
    # xlabel
    plt.xlabel('Simulation Time (ns)',fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='x',width=2,labelsize=22)
    ax.xaxis.set_major_locator(plt.MultipleLocator(100))
    plt.xlim(0,500)
    
    # ylabel
    plt.ylabel('%s-%s\n(%s±%s Å)'%(ligand_name,resid_name,y_mean,y_std),fontfamily='Arial',fontsize=24)
    plt.tick_params(axis='y',width=2,labelsize=22)
    ax.yaxis.set_major_locator(plt.MultipleLocator(5))
    plt.ylim(0,10)
    
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
    return y1,y2,y3


def data_stat(ligand,resid, y1, y2, y3):
    # mean,var,std
    f = open('%s_stat.txt'%ligand,'a+')
    # f.writelines('mean,var,std\n')
    f.writelines('%s\n'%resid)
    f.writelines('%s %s %s\n'%(round(np.mean(y1), 2), round(np.var(y1), 2), round(np.std(y1), 2)))
    f.writelines('%s %s %s\n'%(round(np.mean(y2), 2), round(np.var(y2), 2), round(np.std(y2), 2)))
    f.writelines('%s %s %s\n'%(round(np.mean(y3), 2), round(np.var(y3), 2), round(np.std(y3), 2)))
    y = np.array(list(y1) + list(y2) + list(y3))
    f.writelines('%s %s %s\n'%(round(np.mean(y), 2), round(np.var(y), 2), round(np.std(y), 2)))
    f.writelines('\n')
    f.closed
    return round(np.mean(y), 1),round(np.var(y), 1), round(np.std(y), 1)

if __name__ == '__main__':
    resid_list = ['29','30','31','32','33','235','238','240','243','304','307','318','319','320','322','324']
    # resid_list_xx = ['Y29','K30','N31','G32','G33','A235','H238','D240','R243','F304','L307','I318','E319','D320','A322','E324']
    resid_name_list = ['Y87','K88','N89','G90','G91','A293','H296','D298','R301','F362','L365','I376','E377','D378','A380','E382']

    ligand = 'LDP'  # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Dopamine'
    for resid in resid_list:
        resid_name = resid_name_list[resid_list.index(resid)]
        plot_pdf(ligand,ligand_name,resid,resid_name)
    
    ligand = 'LNR'  # LDP-Dopamine,LNR-Norepinephrine
    ligand_name = 'Norepinephrine'
    for resid in resid_list:
        resid_name = resid_name_list[resid_list.index(resid)]
        plot_pdf(ligand,ligand_name,resid,resid_name)