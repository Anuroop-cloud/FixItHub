import numpy as np

arr2D = np.array([[1,2,3],
                  [4,5,6],
                  [7,8,9]])
#indexing
print(arr2D[2,1])   #R3,C2

#slicing
print(arr2D[1,:])  #[4 5 6]
print(arr2D[:,2])  #[3 6 9]


#indexing in 3D

arr = np.array([[[10,20],[30,40]],[[50,60],[70,80]]])
#how would you print 80?
print(arr[1])       #[[50,60],[70,80]]]
print(arr[1,1])     #[70,80]
print(arr[1,1,1])   #80 
