import json


class monitoring():

    def __init__(self):

        self.number_of_sec_req_inference = 0
        self.number_of_fail_req_inference = 0
        self.number_per_label =  {'airplane': 0, 'automobile': 0, 'bird': 0, 'cat':0 ,'deer':0, 'dog':0, 'frog':0, 'horse':0, 'ship':0, 'truck':0 }
        self.acc_per_label =  {'airplane': [], 'automobile': [], 'bird': [], 'cat':[] ,'deer':[], 'dog':[], 'frog':[], 'horse':[], 'ship':[], 'truck':[] }
        self.request_duration = []

    def add_label(self, label):
        self.number_per_label[label] = self.number_per_label[label] +1 

    def get_number_label(self):
        temp = self.number_per_label.copy()
        self.number_per_label =  {'airplane': 0, 'automobile': 0, 'bird': 0, 'cat':0 ,'deer':0, 'dog':0, 'frog':0, 'horse':0, 'ship':0, 'truck':0 }
        return temp
    
    def add_acc_per_label(self, acc, label):
        self.acc_per_label[label].append(acc)

    def get_acc_per_label(self):
        temp_acc_per_label = self.acc_per_label.copy()
        self.acc_per_label =  {'airplane': [], 'automobile': [], 'bird': [], 'cat':[] ,'deer':[], 'dog':[], 'frog':[], 'horse':[], 'ship':[], 'truck':[] }
        return temp_acc_per_label

    def add_duration(self,duration):
        self.request_duration.append(duration) 

    def get_duration(self):
        tem_req_dur = self.request_duration.copy()
        self.request_duration = []
        return tem_req_dur

    def add_number_of_suc_req_inference(self,acc,label,duration):
        acc = float(acc)
        self.number_of_sec_req_inference = self.number_of_sec_req_inference +1
        self.add_duration(duration)
        self.add_label(label)
        self.add_acc_per_label(acc,label)

    def add_number_of_fail_req_inference(self):
        self.number_of_fail_req_inference = self.number_of_fail_req_inference + 1
    
    def get_number_of_suc_req_inference(self):
        temp_suc_req = self.number_of_sec_req_inference
        self.number_of_sec_req_inference = 0 
        return temp_suc_req

    def get_number_of_fail_req_inference(self):
        temp_fail_req = self.number_of_fail_req_inference
        self.number_of_fail_req_inference = 0 
        return temp_fail_req
    
    def status_inference(self):
        stat ={
            "suc_requests": self.get_number_of_suc_req_inference(),
            "failed_requests": self.get_number_of_fail_req_inference(),
            "num_labels": self.get_number_label(),
            "acc_per_label": self.get_acc_per_label(),
            "time_dur": self.get_duration()
        }
        return stat