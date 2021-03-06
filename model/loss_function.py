import torch
import torch.nn as nn
import torch.functional as func
from torch.autograd import Function

class My_Mass_Balance_loss(nn.Module):
    def __init__(self,beta1,beta2):
        super(My_Mass_Balance_loss, self).__init__()
        self.mse_loss=nn.MSELoss()
        self.beta1=beta1
        self.beta2=beta2



    def forward(self,y_pred,y,original_fraction):
        loss1=self.mse_loss(y_pred,y)
        material_num=len(original_fraction[0])

        temp1=y_pred[:,:material_num]*y_pred[:,-2].unsqueeze(1)
        temp2 =y_pred[:,material_num:2*material_num]*y_pred[:,-1].unsqueeze(1)
        temp=temp1+temp2
        massloss=self.mse_loss(temp,original_fraction)
        total_loss=self.beta1*massloss+self.beta2*loss1

        return total_loss





