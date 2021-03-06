from data import generate_data
from data.generate_data import genertate_T, genertate_P, genertate_Zs_n,flashdata
# from tool import Py2Cpp as pc
from my_test import test_data_set
import xgboost as xgb
from xgboost import XGBRegressor,XGBClassifier
from thermo import ChemicalConstantsPackage, CEOSGas, CEOSLiquid, SRKMIX, FlashVLN, PropertyCorrelationsPackage, \
    HeatCapacityGas
from torch.utils.data import DataLoader
from model import ArtificialNN
from model.train import DeepNetwork_Train ,check_IDexist
import torch
import torch.nn as nn
import thermo
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.signal import convolve2d, correlate2d
from sklearn.multioutput import MultiOutputRegressor,MultiOutputClassifier
import torch

import random
import os

import csv



dic={}

All_ID = ['Methane','Ethane', 'Propane', 'N-Butane','N-Pentane', 'N-Hexane', 'Heptane']
ID=['Ethane','N-Pentane']
dic["IDs"]=ID
constants, properties = ChemicalConstantsPackage.from_IDs(ID)
dic["Tc"]=constants.Tcs
dic["Pc"]=constants.Pcs
dic["Omega"]=constants.omegas

import matplotlib.pyplot as plt

num=800
zs=[[0.5,0.5] for i in range(num)]
temp=310.59
pressure=50
phase="gas"
index=len(ID)*0 if phase=="liquid" else len(ID)*1
row_data=[list(np.ones(num) *temp),list(np.linspace(0.3,1,num)*pressure*100000)]
# row_data=[list(np.linspace(0.5,1,num)*temp),list(np.ones(num)*pressure*100000)]

test = flashdata(constants, properties, {"T": row_data[0], "P": row_data[1]}, zs, "Vapor_Liquid")

def pr():
    x=[]
    y=[]
    for i in range(len(test)):
            # print(test[i].liquid0,test[i].liquid0.zs)
            # print(test[i].zs)
            # print(hasattr(test[i],"gas"))
            # print(test[i].gas)
            # print(test[i].betas)

            try:
                if test[i].gas is not None and test[i].liquid0 is not None:
                    #test1_ phase fraction of material
                    if phase == "liquid":
                        y.append(np.array(test[i].liquid0.zs)*test[i].LF/(np.array(test[i].liquid0.zs)*test[i].LF+np.array(test[i].gas.zs)*test[i].VF))
                    else:
                        y.append(np.array(test[i].gas.zs) * test[i].VF / (
                                    np.array(test[i].liquid0.zs) * test[i].LF + np.array(test[i].gas.zs) * test[i].VF))
                        print(np.array(test[i].gas.zs) * test[i].VF / (
                                    np.array(test[i].liquid0.zs) * test[i].LF + np.array(test[i].gas.zs) * test[i].VF),
                              np.array(test[i].liquid0.zs)*test[i].LF/(np.array(test[i].liquid0.zs)*test[i].LF+np.array(test[i].gas.zs)*test[i].VF))

                    # test2_ phase fraction of phase
                    # if phase == "gas":
                    #     y.append(test[i].gas.zs)
                    # else:
                    #     y.append(test[i].liquid0.zs)

                    # test2_ phase fraction of phase
                    # if phase == "gas":
                    #     y.append(test[i].VF)
                    # else:
                    #     y.append(test[i].LF)

                    x.append(row_data[1][i])
            except:
                pass
    print(y)


    y=np.array(y)
    print(y)
    print(y.shape)
    plt.plot(x,y[:,0])
    my_y_ticks = np.arange(0, 1.2, 0.2)
    plt.yticks(my_y_ticks)
    plt.title(ID[0]+"-"+ID[1]+str(zs[0])+","+phase+","+str(temp)+"K")
    plt.xlabel("pressure(PA)")
    plt.ylabel("material0 "+phase+" fraction")
    plt.show()
    exit(0)
pr()

#
# collector=generate_data.collector()
# collector.set_collect_method(collector._collect_material0)
# collector.set_output_type(torch.tensor)
# test_loader = DataLoader(test, shuffle=False,batch_size=10, collate_fn=collector)
# result=[]
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
# criterian=torch.nn.MSELoss()
# model=ArtificialNN.ANN(10,1).to(device)
# opt=torch.optim.SGD(model.parameters(),lr=0.01)
# result_x=[]
#
# #
# #
# def train(model,test_loader,criterian,opt):
#     model.train()
#     for x,y in test_loader:
#         x, y = x.to(device), y[:,0].to(device)
#         opt.zero_grad()
#         ypred=model(x)
#         loss=criterian(y,ypred)
#         print(loss)
#         loss.backward()
#         opt.step()
# for i in range(100):
#     train(model,test_loader,criterian,opt)
#
#
#
#
# result=np.array(result)
# print(result)
#
# plt.plot(result_x,result)
# my_y_ticks = np.arange(0, 1.2, 0.2)
# plt.yticks(my_y_ticks)
# plt.title(ID[0]+"-"+ID[1]+str(zs[0])+","+phase+","+str(temp)+"K")
# plt.xlabel("pressure(PA)")
# plt.ylabel("material0 "+phase+" fraction")
# plt.show()


# print(test[0].liquids)
# i=0
# for x,y in test_loader:
#
#     if len(test[i].liquids)>0:
#         if(test[i].gas!=None):
#             print(True)
#
#
#     i+=1

# print(T_list)
# print(P_list)
# print(Zs_list)
#
# print(test[0])

#


# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import cross_val_score
# from bayes_opt import BayesianOptimization
# # print(check_IDexist("('Ethane', 'Propane', 'N-Butane', 'N-Pentane', 'Heptane')",".\\result_of_cleaned_data\\XGBregressor\\"))
#
# a=generate_data.multicsv_data_generater()
# X_train, y_train, X_test, y_test, material_ID=a[10]
# from sklearn.metrics import mean_squared_error
# def rf_cv(**kwargs):
#     n_estimators=kwargs["n_estimators"] if "n_estimators" in kwargs.keys() else 150
#     min_samples_split=kwargs["min_samples_split"] if "min_samples_split" in kwargs.keys() else 150
#     max_features=kwargs["min_samples_split"] if "min_samples_split" in kwargs.keys() else 0.999
#     max_depth=kwargs["min_samples_split"] if "min_samples_split" in kwargs.keys() else 12
#     rf = RandomForestRegressor(n_estimators=int(n_estimators),
#             min_samples_split=int(min_samples_split),
#             max_features=min(max_features, 0.999), # float
#             max_depth=int(max_depth),
#             random_state=2,
#             n_jobs=8
#         ).fit(X_train, y_train)


    # return -mean_squared_error(rf.predict(X_test), y_test)
#
# rf_bo = BayesianOptimization(
#         rf_cv,
#         {'n_estimators': (10, 250),
#         'min_samples_split': (2, 25),
#         'max_features': (0.1, 0.999),
#         'max_depth': (5, 15)}
#     )
#
# a=rf_bo.maximize(n_iter=10)
#
# print(a)

# print(rf_bo.maximize())
#
# import multiprocessing
# from mpi4py import MPI
# from itertools import combinations
# # from multiprocessing import Pool
# def f(ID):
#     i=len(ID)
#     root_path = "."+os.sep+"mini_cleaned_data"+os.sep +"train_3000" + os.sep + "mix_" + str(i) + os.sep
#
#     constants, properties = ChemicalConstantsPackage.from_IDs(ID)
#     generate_data.generate_good_TPZ(3000,constants, properties,root_path+str(ID)+"_train",comment=str(ID))
#
#     return 0
#
# IDs=[]
# if __name__ == '__main__':
#     comm=MPI.COMM_WORLD
#     rank=comm.Get_rank()
#     size=comm.Get_size()
#     #
    # for i in range(1,8):
    #     for com in combinations(All_ID,i):
    #         IDs.append(com)
    # for i in range(rank,len(IDs),size):
    #     f(IDs[i])






# def create_data(i):
#         root_path=".\\cleaned_data\\"+"mix_"+str(i)+"\\"
#         for id in combinations(All_ID, i):
#             print(id)
#             constants, properties = ChemicalConstantsPackage.from_IDs(id)
#             generate_data.generate_good_TPZ(50000,constants, properties,root_path+str(id),comment=str(id))
#
# for i in range(2,8):
#     create_data(i)


# constants, properties = ChemicalConstantsPackage.from_IDs(ID)
#
# dic = pd.DataFrame(columns=["epoch", "loss"])
# dic2 = pd.DataFrame([[1, 2], [3, 4]])
# dic2.rename(columns={0: "epoch", 1: "loss"}, inplace=True)
# print(str(ID))
# xgbReg = xgb.XGBRegressor(n_estimators=200)
# xgbReg.score()
# #
# row_data=generate_data.generate_good_TPZ(10000,constants, properties,"good_TPZ_test",comment=str(ID))
#

# T_set=genertate_T(2,50,200)
# P_set=genertate_P(2,1e5,2e5)
# Zs_set=genertate_Zs_n(2,3)
# data = pd.read_csv("good_TPZ_train.csv", comment='#')
#
# T_set_train, P_set_train, Zs_set_train = generate_data.read_good_TPZ_from_csv("good_TPZ_train.csv")
# T_set_test, P_set_test, Zs_set_test = generate_data.read_good_TPZ_from_csv("good_TPZ_test.csv")


# train_set = generate_data.flashdata(constants, properties, {"T": T_set_train, "P": P_set_train}, Zs_set_train, "Vapor_Liquid")
# test_set = generate_data.flashdata(constants, properties, {"T": T_set_test, "P": P_set_test}, Zs_set_test, "Vapor_Liquid")
# #
# #
# train_loader = DataLoader(train_set, shuffle=False,
#                           batch_size=train_set.__len__(), collate_fn=generate_data.collate_VL_NParray)
# test_loader = DataLoader(test_set, shuffle=False,
#                           batch_size=test_set.__len__(), collate_fn=generate_data.collate_VL_NParray)




##ANN

# from torch.autograd.gradcheck import gradcheck

# moduleConv = ArtificialNN.My_MSE_loss()
#
# y1 = torch.randn(20, 20, dtype=torch.double, requires_grad=True)
# y2 = torch.randn(20, 20, dtype=torch.double, requires_grad=True)
# test = gradcheck(moduleConv, [y1,y2], eps=1e-6, atol=1e-4)
# print("Are the gradients correct: ", test)



# model = ArtificialNN.simple_ANN()
#
# criterion = ArtificialNN.My_MSE_loss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
#
# ANN_train = DeepNetwork_Train(model, criterion, optimizer, train_loader)
# ANN_train.Train(epoch=10)


###XGboost
# params = {
#     'booster': 'gbtree',
#     'objective': 'multi:softmax',
#     'num_class': 3,
#     'gamma': 0.1,
#     'max_depth': 6,
#     'lambda': 2,
#     'subsample': 0.7,
#     'colsample_bytree': 0.7,
#     'min_child_weight': 3,
#     'eta': 0.1,
#     'seed': 1000,
#     'nthread': 4,
# }
#
# X,y =next(iter(train_loader))
# print(X.shape)
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234565)
#
#
# # X_train = np.random.rand(500, 9)  # 500 entities, each contains 100 features
# # y_train = np.random.random(size=(500,6))
# print(X_train.shape,y_train.shape)
# xgb_multi = xgb.XGBRegressor()
#
# xgb_multi.fit(X_train, y_train)
# val_pred = xgb_multi.predict(X_train)
#
# cnt = 0
# for i in range(val_pred.shape[0]):
#     print(val_pred[i],y_train[i])
#     if np.allclose(val_pred[i],y_train[i]):
#         cnt += 1
#         print("True")
# print(cnt/val_pred.shape[0])


# multiXGB=MultiOutputRegressor(xgb.XGBRegressor(**params)).fit(X_train,y_train)
# check=multiXGB.predict(X_test)
# cnt=0
# for i in range(y_test.shape[0]):
#     print(check[i],y_test[i])
#     if np.allclose(check[i],y_test[i].detach().numpy()):
#         cnt+=1
#
# print(cnt/y_test.shape[0])


