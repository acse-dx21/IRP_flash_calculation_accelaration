import sys

sys.path.append("..")
from data import generate_data
import pandas as pd
from mpi4py import MPI
import itertools
from sklearn.model_selection import GridSearchCV
from model import ArtificialNN
import time
import os
from pytorch_tabnet.tab_model import TabNetRegressor
import torch.optim as optim

data_set_index = [0,1 ,2, 3, 4, 5]
mix_index = "all"
device = "cuda"
data_root = "." + os.sep + "mini_cleaned_data" + os.sep
save_model = False
save_data = True
from torch.optim.lr_scheduler import ReduceLROnPlateau


def get_related_path(Material_ID):
    print(Material_ID)
    print(type(Material_ID))
    if isinstance(Material_ID, list):
        return "mix_" + str(len(Material_ID[0])) + os.sep + "mixture.csv"
    else:
        return "mix_" + str(len(Material_ID)) + os.sep + str(Material_ID) + ".csv"
    print("func:get_related_path  problem")
    raise RuntimeError


def get_range(mix_index):
    """
    use to fine target mixture
    :param mix_index: "all" or int range from 1-7
    :return:
    """
    if (mix_index == "all"):
        return 0, 127
    assert mix_index > 0
    start = 0
    end = comb(7, 1)

    for i in range(1, mix_index):
        start += comb(7, i)
        end += comb(7, i + 1)

    return int(start), int(end)


param_grid = [
    # try combinations of hyperparameters
    {'subsample': [0.2, 0.6, 1.0],
     'learning_rate': [0.01, 0.05, 0.1],
     'n_estimators': [300, 400, 500],
     'max_depth': [3, 5, 10],
     'colsample_bytree': [0.6],
     'reg_lambda': [10]}
]


# @Misc{,
#     author = {Fernando Nogueira},
#     title = {{Bayesian Optimization}: Open source constrained global optimization tool for {Python}},
#     year = {2014--},
#     url = " https://github.com/fmfn/BayesianOptimization"
# }
# import os
#
# data_path = ".." + os.sep + "cleaned_data" + os.sep
# result_path = "." + os.sep + "result_data" + os.sep
#
#

from bayes_opt import BayesianOptimization
from sklearn.metrics import mean_squared_error

#

data_record = {"trainning_time_consume(s)": [], "test_time_consume(s)": []}

import argparse
# print(a)
from mpi4py import MPI


model_kwargs={}

def model_cv(**kwargs):
    model_kwargs["hidden_size"] =2**int(kwargs["hidden_size_pow"])
    model_kwargs["num_features"]=10
    model_kwargs["num_targets"]=6

    print(model_kwargs["hidden_size"])

    start_train = time.time()
    model_instance = ArtificialNN.Neural_Model_Sklearn_style(ArtificialNN.OneD_CNN,model_kwargs)
    model_instance.fit(X_train, y_train)

    train_time = time.time() - start_train
    if save_model:
        model_instance.save_model(model_save_path + get_related_path(Material_ID).replace(".csv", ".json"))
    start_pred = time.time()
    pred = model_instance.predict(X_test)
    test_time = time.time() - start_pred

    data_record["trainning_time_consume(s)"].append(train_time)
    data_record["test_time_consume(s)"].append(test_time)

    return -mean_squared_error(pred, y_test)


def run_bayes_optimize(num_of_iteration=10, data_index=2):

    global X_train, y_train, X_test, y_test, Material_ID
    X_train, y_train, X_test, y_test, Material_ID = relate_data[data_index]

    print(model_save_path + get_related_path(Material_ID).replace(".csv", ".json"))

    rf_bo = BayesianOptimization(
        model_cv,
        {
            "hidden_size_pow": [10, 13],
        }
    )

    rf_bo.maximize(n_iter=num_of_iteration)
    result_data_root = "." + os.sep + "BO_result_data" + os.sep
    routing_data_root = "." + os.sep + "BO_training_routing" + os.sep
    pd.DataFrame(data_record)
    routing_data_root + get_related_path(Material_ID)
    if save_data:
        pd.DataFrame(data_record).to_csv(saved_root + routing_data_root + get_related_path(Material_ID))
        pd.DataFrame(rf_bo.res).to_csv(saved_root + result_data_root + get_related_path(Material_ID))

    data_record["trainning_time_consume(s)"].clear()
    data_record["test_time_consume(s)"].clear()


def run_Grid_search(num_of_iteration):
    print(num_of_iteration)


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start, end = get_range(mix_index)

    product_index = list(itertools.product(data_set_index, list(range(start, end))))
    print(product_index)
    print("total size", len(product_index))
    for index in range(rank, len(data_set_index), size):
        data_index = data_set_index[index]
        print(data_index)

        model_save_path = "." + os.sep + "saved_model" + os.sep + "mini_dataset_mixture" + os.sep + f"mini_data_{data_index}" + os.sep
        mini_data_path = ".." + os.sep + "data" + os.sep + data_root + f"mini_data_{data_index}" + os.sep
        saved_root = "." + os.sep + "mini_cleaned_data_mixture" + os.sep + f"mini_data_{data_index}" + os.sep
        All_ID = ['Methane', 'Ethane', 'Propane', 'N-Butane', 'N-Pentane', 'N-Hexane', 'Heptane']
        relate_data = generate_data.mixture_generater(mini_data_path)
        # collector=generate_data.collector()
        # collector.set_collect_method("VF")
        # relate_data.set_collector(collector)
        relate_data.set_batch_size(128)
        relate_data.set_collector("VF")
        run_bayes_optimize(10, 2)
