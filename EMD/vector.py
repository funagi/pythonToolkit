import math
class vector:
    def __init__(self, x_ = 0, y_ = 0, z_ = 0): #构造函数
        self.x = x_
        self.y = y_
        self.z = z_
    def __add__(self, obj): #重载+作为加号
        return vector(self.x+obj.x, self.y+obj.y, self.z+obj.z)
    def __sub__(self, obj): #重载-作为减号
        return vector(self.x-obj.x, self.y-obj.y, self.z-obj.z)
    def __mul__(self, obj): #重载*作为点乘
        if isinstance(obj,vector):
            return self.x*obj.x+self.y*obj.y+self.z*obj.z
        elif isinstance(obj,int) or isinstance(obj,float):
            return vector(self.x * obj, self.y * obj, self.z * obj)
    def __pow__(self, obj): #重载**作为叉乘。不好，偏离了常理上的意义，可以考虑重载其他符号，或者直接写函数。
        return vector(self.y*obj.z-obj.y*self.z, self.z*obj.x-self.x*obj.z, self.x*obj.y-obj.x*self.y)
    def __str__(self): #供print打印的字符串
        return str(self.x)+','+str(self.y)+','+str(self.z)
    def __getitem__(self,key):
        if key==0:
            return self.x
        if key==1:
            return self.y
        if key==2:
            return self.z
    def length(self):
        return math.sqrt((self.x*self.x)+(self.y*self.y)+(self.z*self.z))
    def normalize(self):
        l = vector.length(self)
        return vector(self.x/l,self.y/l,self.z/l)
