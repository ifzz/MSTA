from generic_algo import gen_algo
from data import to_class
import pandas as pd
import numpy as np

class HM(gen_algo):
    """ Historical mean algorithm
    This algorithm will just take the historical mean as a prediction
    It includes arithmetic and geometric mean and allows for a non maximum window size
    It will be used as a benchmark for prediction as it represents the random walk hypothesis
    """

    def __init__(self, global_hyperparams, hp_grid=None, mean_type="arithmetic", window_size=None):
        gen_algo.__init__(self, global_hyperparams, hp_grid) # allow to run the init of the gen_algo class, and define all default arguments
        self.name="Historical Mean"
        self.algo_type="BA" # By convention
        self.mean_type=mean_type
        if window_size is not None:  # It is possible to define a window size different from the global rolling window size, but it has to be less or equal
            self.window_size=window_size
        else:
            self.window_size=self.global_hyperparams["rolling_window_size"]
            
    
    def predict(self, X_test, pred_index=None):
        w = self.window_size
        if self.mean_type=="arithmetic":
            predicted_values=X_test.iloc[:,:w].mean(axis=1,skipna=None)
        elif self.mean_type=="geometric":
        # Let us note that the geometric mean should be optimized using numpy vectorized operations
            predicted_values=1
            for col in X_test.iloc[:,:w].columns:
                predicted_values=predicted_values*(1+X_test.iloc[:,col])
            predicted_values=np.power(predicted_values,1/w)-1
            
        # The output will be different in case of a regression or classification, no need to change the output for a regression
        if self.global_hyperparams["output_type"]=="C":
            threshold=self.global_hyperparams["threshold"]
            predicted_values=to_class(predicted_values, threshold)

        if pred_index is not None:
            self._store_predicted_values(pred_index,predicted_values)
        return predicted_values # here we have a redundency in the return and the side effect of the method, this is used to simplify coding

## testing code
#import matplotlib.pyplot as pyplt
#import data

#dataset=data.dataset_building(n_max=1000)
#data_test=dataset[["EURUSD Curncy"]]
#hm=HM(100)
#hm2=HM(100,mean_type="geometric")
#res=hm.predict(data_test)
#res2=hm2.predict(data_test)
#pyplt.plot(data_test)
#pyplt.plot(res)
#pyplt.plot(res2)
#pyplt.show()
## end of testing code
    