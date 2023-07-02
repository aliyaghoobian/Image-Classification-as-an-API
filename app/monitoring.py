import json


class monitoring():

    def __init__(self):
        # self.acc_list = list()
        self.number_of_sec_req_inference = 0
        self.number_of_fail_req_inference = 0
        self.number_per_label =  {'airplane': 0, 'automobile': 0, 'bird': 0, 'cat':0 ,'deer':0, 'dog':0, 'frog':0, 'horse':0, 'ship':0, 'truck':0 }
        self.acc_per_label =  {'airplane': [], 'automobile': [], 'bird': [], 'cat':[] ,'deer':[], 'dog':[], 'frog':[], 'horse':[], 'ship':[], 'truck':[] }
   
    # def add_acc_inference(self,new_acc):
    #     self.acc_list.append(new_acc)
    
    # def get_acc_inference(self):
    #     list_of_acc = self.acc_list
    #     self.acc_list = list() # clear acc list
    #     return list_of_acc
    
    def add_label(self, label):
        self.number_per_label[label] = self.number_per_label[label] +1 

    def get_numbel_label(self):
        return self.number_per_label
    
    def add_acc_per_label(self, acc, label):
        self.acc_per_label[label].append(acc)

    def get_acc_per_label(self):
        temp_acc_per_label = self.acc_per_label
        self.acc_per_label =  {'airplane': [], 'automobile': [], 'bird': [], 'cat':[] ,'deer':[], 'dog':[], 'frog':[], 'horse':[], 'ship':[], 'truck':[] }
        return temp_acc_per_label

    def add_number_of_suc_req_inference(self,acc,label):
        self.number_of_sec_req_inference = self.number_of_sec_req_inference +1
        self.add_label(label)
        self.add_acc_per_label(acc,label)

    def add_number_of_fail_req_inference(self):
        self.number_of_fail_req_inference = self.number_of_fail_req_inference + 1
    
    def get_number_of_suc_req_inference(self):
        succ_req_inf = self.number_of_sec_req_inference
        self.number_of_sec_req_inference = 0
        return succ_req_inf

    def get_number_of_fail_req_inference(self):
        fail_req_inf = self.number_of_fail_req_inference
        self.number_of_fail_req_inference = 0
        return fail_req_inf
    
    def status_inference(self):
        stat ={
            "suc_requests": (self.get_number_of_suc_req_inference()),
            "failed_requests": (self.get_number_of_fail_req_inference()),
            "num_labels": (self.get_numbel_label()),
            "acc_per_label": (self.get_acc_per_label())
        }
        return stat