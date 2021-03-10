import tqdm
from itertools import product as iterprod 
from pytearcat.Tensor.misc import new_ten,reload_all
from pytearcat.Tensor.core import config
from pytearcat.Tensor.tensor_class import construct, tensor_series
from .riemann import calculate_riemann
from .ricci import calculate_ricci, calculate_ricci_scalar
from pytearcat.Tensor.core.core import core_calc,display_IP,Latex_IP

if core_calc == 'sp':

    from pytearcat.Tensor.core.core import diff, Rational, sympify, factor

elif core_calc == 'gp':

    from pytearcat.Tensor.core.core import diff, divide, simplify

def calculate_einstein(All = False):

    global Einstein

    dim = config.dim

    g = config.g.tensor

    if config.G is None:

        Einstein = new_ten('Einstein',2)

        config.G = Einstein


    else:

        Einstein = config.G

    if config.ricci is None:

        Ricci_local = calculate_ricci()

    else: 

        Ricci_local = config.ricci
    
    if config.ricciS is None:

        R = calculate_ricci_scalar()
    
    else:

        R = config.ricciS

        
    #---

    if Einstein.indexes[0] == False:

        Einstein_list = construct('False',dim,2)

        display_IP(Latex_IP(r'Einstein Tensor $G_{\alpha \beta}$'))

        for p in tqdm.tqdm_notebook(iterprod(range(config.dim),repeat=2),total=config.dim**2):

            m = p[0]
            n = p[1]

            if Einstein_list[m][n] == False:

                if core_calc == 'sp':

                    EinstTemp = Ricci_local.tensor[0][m][n] - Rational(1,2)*(g[0][m][n])*R.tensor

                elif core_calc == 'gp':

                    EinstTemp = Ricci_local.tensor[0][m][n] - divide(1,2)[0]*(g[0][m][n])*R.tensor

                if config.ord_status == True:

                    Einstein.tensor[0][m][n] = tensor_series(EinstTemp)

                else:

                    if core_calc == 'sp':

                        Einstein.tensor[0][m][n] = sympify(factor(EinstTemp))

                    elif core_calc == 'gp':

                        Einstein.tensor[0][m][n] = simplify(EinstTemp)

                Einstein_list[m][n] = True

                # Simmetry

                Einstein.tensor[0][n][m] = Einstein.tensor[0][m][n]

                Einstein_list[n][m] = True

        Einstein.indexes[0] = True

    else:

        display_IP(Latex_IP(r"Einstein Tensor $G_{\alpha \beta}$ already calculated"))

    if All == True:

        Einstein.indexcomb('_,_')

    Einstein.space()

    return Einstein